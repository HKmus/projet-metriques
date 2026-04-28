"""
Requirements Evaluation Agent — CLI entry point

Supports single evaluation or batch evaluation with metric selection flags.

Run:
    python main.py                          # Load from sys_description.txt + srs_history_groq.json
    python main.py --demo                   # Demo mode with built-in data
    python main.py --sys <file> --json <file>  # Custom description and requirements files
    python main.py --correctness             # Run only correctness metric
    python main.py --completeness --testability  # Multiple specific metrics
    python main.py --all --hitl              # All metrics with human review
"""

import json
import sys
import uuid
import argparse
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import Progress

load_dotenv()

from src.graph import graph
from src.state import AgentState, Requirement, HumanVerification
from src.prompts import METRICS

console = Console()

# ─────────────────────────────────────────────
# Demo data
# ─────────────────────────────────────────────

DEMO_SYSTEM_DESC = """
An online bookstore platform where users can browse, search, and purchase books.
The system supports user registration and login, a shopping cart, order management,
payment processing via credit card, and email notifications for order confirmations.
Administrators can manage inventory, update book listings, and view sales reports.
"""

DEMO_REQUIREMENTS = [
    {"id": "R1", "text": "The system shall allow users to register using their email and password."},
    {"id": "R2", "text": "Users should be able to log in."},
    {"id": "R3", "text": "The system shall send a confirmation email after a successful purchase."},
    {"id": "R4", "text": "The system shall allow users to add books to a shopping cart."},
    {"id": "R5", "text": "Users can pay for their orders using credit cards."},
    {"id": "R6", "text": "The system shall allow users to register with email and password."},
    {"id": "R7", "text": "Administrators shall be able to add, edit, and delete book listings including title, author, price, and stock quantity."},
    {"id": "R8", "text": "The system shall be fast and user-friendly."},
]


# ─────────────────────────────────────────────
# CLI argument parsing
# ─────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Requirements Evaluation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo                    # Demo mode, all metrics
  python main.py --demo --correctness      # Demo mode, correctness only
  python main.py --demo --completeness --testability  # Multiple metrics
  python main.py --sys custom.txt --json reqs.json --redundancy  # Custom files
  python main.py --all --hitl              # All metrics with human review
        """
    )
    
    # Input mode
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Use built-in demo data instead of loading from files"
    )
    parser.add_argument(
        "--sys",
        type=str,
        default="sys_description.txt",
        help="Path to system description file (default: sys_description.txt)"
    )
    parser.add_argument(
        "--json",
        type=str,
        default="srs.json",
        help="Path to requirements JSON file (default: srs.json)"
    )
    
    # Evaluation mode
    parser.add_argument(
        "--hitl",
        action="store_true",
        help="Enable human-in-the-loop review (default: auto-complete)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all metrics (default if no specific metrics selected)"
    )
    
    # Individual metric flags
    parser.add_argument(
        "--correctness",
        action="store_true",
        help="Run correctness metric evaluation"
    )
    parser.add_argument(
        "--completeness",
        action="store_true",
        help="Run completeness metric evaluation"
    )
    parser.add_argument(
        "--redundancy",
        action="store_true",
        help="Run redundancy metric evaluation"
    )
    parser.add_argument(
        "--testability",
        action="store_true",
        help="Run testability metric evaluation"
    )
    
    parser.add_argument(
        "--reason",
        action="store_true",
        help="Include reasoning for the scores in the generated evaluations"
    )
    
    return parser.parse_args()


def get_selected_metrics(args) -> list[str]:
    """Determine which metrics to run based on CLI args."""
    # If --all is specified, run all metrics
    if args.all:
        return METRICS
    
    # Collect explicitly specified metrics
    selected = []
    metric_flags = ["correctness", "completeness", "redundancy", "testability"]
    
    for metric in metric_flags:
        if getattr(args, metric, False):
            selected.append(metric)
    
    # If no specific metrics selected, default to all
    if not selected:
        return METRICS
    
    return selected


# ─────────────────────────────────────────────
# File loading
# ─────────────────────────────────────────────

def load_system_description(file_path: str = "sys_description.txt") -> str:
    """Load system description from file"""
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] {file_path} not found")
        sys.exit(1)


def load_requirements_from_json(json_file: str = "srs_history_groq.json") -> list:
    """Load requirements from JSON file"""
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] {json_file} not found")
        sys.exit(1)


# ─────────────────────────────────────────────
# Display helpers
# ─────────────────────────────────────────────

SCORE_COLORS = {1: "red", 2: "dark_orange", 3: "yellow", 4: "cyan", 5: "green"}


def score_style(score: int) -> str:
    return f"[{SCORE_COLORS.get(score, 'white')}]{score}/5[/]"


def print_metric_results(metric_results: list) -> None:
    for result in metric_results:
        metric = result["metric"]
        scores = [e["score"] for e in result["evaluations"]]
        avg = round(sum(scores) / len(scores), 2) if scores else 0

        table = Table(
            title=f"{metric.upper()} — avg: {avg}/5",
            box=box.SIMPLE_HEAD,
            show_lines=True,
        )
        table.add_column("ID", style="bold", width=6)
        table.add_column("Score", width=8)
        table.add_column("Reason", style="dim")

        for ev in result["evaluations"]:
            table.add_row(ev["req_id"], score_style(ev["score"]), ev.get("reason", ""))

        console.print(table)


def print_summary(final_report: dict) -> None:
    summary = final_report.get("summary", {})
    table = Table(title="Final Summary — all metrics", box=box.ROUNDED)
    table.add_column("Metric", style="bold")
    table.add_column("Avg score", justify="center")
    table.add_column("Min", justify="center")
    table.add_column("Max", justify="center")
    table.add_column("Distribution 1→5")

    for metric in METRICS:
        s = summary.get(metric, {})
        dist = s.get("distribution", {})
        dist_str = "  ".join(f"{i}×{dist.get(str(i), 0)}" for i in range(1, 6))
        avg = s.get("average", 0)
        avg_style = SCORE_COLORS.get(round(avg), "white")
        table.add_row(
            metric,
            f"[{avg_style}]{avg}[/]",
            str(s.get("min", "—")),
            str(s.get("max", "—")),
            dist_str,
        )
    console.print(table)


def save_reports(final_report: dict, iteration: int = 1) -> None:
    """Save individual metric reports with iteration-based structure (no summary.json)."""
    import os
    from pathlib import Path
    
    # Create reports directory structure with iteration folder
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    iteration_dir = reports_dir / f"iter{iteration}"
    iteration_dir.mkdir(exist_ok=True)
    
    # Save individual metric reports with metric suffix
    metrics = final_report.get("metrics", {})
    for metric, evaluations in metrics.items():
        metric_report = {
            "metric": metric,
            "evaluations": evaluations,
            "requirements_count": final_report.get("requirements_count", 0),
            "summary": final_report.get("summary", {}).get(metric, {}),
        }
        metric_file = iteration_dir / f"report_iter{iteration}_{metric}.json"
        with open(metric_file, "w") as f:
            json.dump(metric_report, f, indent=2)
        console.print(f"[green]✓[/green] {metric.title()} report saved to {metric_file}")


# ─────────────────────────────────────────────
# Evaluation function
# ─────────────────────────────────────────────

def evaluate_requirements(
    system_desc: str,
    requirements: list,
    selected_metrics: list[str],
    hitl_mode: bool = False,
    batch_label: str = "",
    include_reason: bool = False,
) -> dict:
    """
    Run evaluation for a set of requirements
    Returns the final report
    """
    if batch_label:
        console.print(f"\n[bold cyan]{batch_label}[/bold cyan]")
    console.print(f"[dim]{len(requirements)} requirements | metrics: {', '.join(selected_metrics)}[/dim]\n")

    # Thread ID for MemorySaver
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state: AgentState = {
        "system_description": system_desc,
        "requirements": requirements,
        "selected_metrics": selected_metrics,
        "include_reason": include_reason,
        "metric_results": [],
        "human_verifications": [],
        "final_report": {},
    }

    # First run: coordinator → agents → aggregator → interrupt at human_review
    for event in graph.stream(initial_state, config=config, stream_mode="values"):
        pass

    # After stream ends at interrupt(), inspect what paused
    current_state = graph.get_state(config)

    # Handle human review phase
    if current_state.next and hitl_mode:
        # Show results and collect verdicts
        metric_results = current_state.values.get("metric_results", [])
        print_metric_results(metric_results)

        # For batch mode, auto-approve (not interactive)
        verifications: list[HumanVerification] = []
        for result in metric_results:
            metric = result["metric"]
            for ev in result["evaluations"]:
                verifications.append(
                    HumanVerification(
                        metric=metric,
                        req_id=ev["req_id"],
                        verdict="approved",
                        comment="",
                    )
                )

        graph.update_state(
            config,
            {"human_verifications": verifications},
            as_node="human_review",
        )

        for event in graph.stream(None, config=config, stream_mode="values"):
            pass

    elif current_state.next and not hitl_mode:
        # Auto-approve without display
        metric_results = current_state.values.get("metric_results", [])

        verifications: list[HumanVerification] = []
        for result in metric_results:
            metric = result["metric"]
            for ev in result["evaluations"]:
                verifications.append(
                    HumanVerification(
                        metric=metric,
                        req_id=ev["req_id"],
                        verdict="approved",
                        comment="",
                    )
                )

        graph.update_state(
            config,
            {"human_verifications": verifications},
            as_node="human_review",
        )

        for event in graph.stream(None, config=config, stream_mode="values"):
            pass

    # Retrieve final report
    final_state = graph.get_state(config)
    final_report = final_state.values.get("final_report", {})

    return final_report


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    args = parse_args()
    demo_mode = args.demo
    hitl_mode = args.hitl
    selected_metrics = get_selected_metrics(args)

    console.print(
        Panel.fit(
            "[bold]Requirements Evaluation Agent[/bold]\n"
            "Powered by LangGraph + LLM",
            border_style="blue",
        )
    )

    # Load inputs
    if demo_mode:
        console.print("[dim]Running in demo mode with built-in inputs...[/dim]\n")
        system_desc = DEMO_SYSTEM_DESC
        all_data = DEMO_REQUIREMENTS
        is_batch = False
    else:
        # Load system description
        system_desc = load_system_description(args.sys)
        console.print(f"[green]✓[/green] System description loaded from {args.sys}\n")

        # Load requirements from JSON
        all_data = load_requirements_from_json(args.json)
        console.print(f"[green]✓[/green] Loaded from {args.json}\n")

        # Detect if it's batch format (with prompt_version and generation_number) 
        is_batch = (
            isinstance(all_data, list) 
            and len(all_data) > 0 
            and isinstance(all_data[0], dict)
            and "prompt_version" in all_data[0] 
            and "generation_number" in all_data[0]
        )

    # Handle batch evaluation
    if is_batch and not demo_mode:
        console.print(f"[cyan]Batch mode detected: {len(all_data)} requirement sets[/cyan]\n")
        
        # Group by prompt version and iteration
        by_version = defaultdict(lambda: defaultdict(dict))
        for item in all_data:
            version = item["prompt_version"]
            iteration = item["generation_number"]
            by_version[version][iteration] = item["requirements"]

        # Generate list of evaluations to run
        evaluations = []
        for version in sorted(by_version.keys()):
            for iteration in sorted(by_version[version].keys()):
                evaluations.append((version, iteration, by_version[version][iteration]))

        console.print(f"Found {len(evaluations)} requirement sets:\n")
        for v, i, reqs in evaluations:
            console.print(f"  • Prompt v{v}, Iteration {i}: {len(reqs)} requirements")
        console.print()

        # Run batch evaluations
        reports = []
        with Progress() as progress:
            task = progress.add_task("[cyan]Evaluating...", total=len(evaluations))

            for idx, (prompt_version, iteration, requirements) in enumerate(evaluations):
                
                final_report = evaluate_requirements(
                    system_desc,
                    requirements,
                    selected_metrics,
                    hitl_mode,
                    batch_label=f"Evaluating Prompt v{prompt_version} — Iteration {iteration}",
                    include_reason=args.reason,
                )
                final_report["metadata"] = {
                    "prompt_version": prompt_version,
                    "iteration": iteration,
                    "num_requirements": len(requirements),
                }
                reports.append((prompt_version, iteration, final_report))
                progress.advance(task)

        # Save batch reports
        console.print("\n[bold]═══ Saving Reports ═══[/bold]\n")
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)

        for prompt_version, iteration, final_report in reports:
            iteration_dir = report_dir / f"iter{iteration}"
            iteration_dir.mkdir(exist_ok=True)
            
            for metric, evaluations in final_report.get("metrics", {}).items():
                metric_report = {
                    "metric": metric,
                    "evaluations": evaluations,
                    "requirements_count": final_report.get("requirements_count", 0),
                    "summary": final_report.get("summary", {}).get(metric, {}),
                    "metadata": final_report.get("metadata", {}),
                }
                report_path = iteration_dir / f"report_v{prompt_version}_iter{iteration}_{metric}.json"
                with open(report_path, "w") as f:
                    json.dump(metric_report, f, indent=2)
                console.print(f"[green]✓[/green] {report_path}")
        
        console.print()

    # Handle single evaluation
    else:
        if isinstance(all_data, list) and len(all_data) > 0 and "prompt_version" not in all_data[0]:
            requirements = all_data
        else:
            requirements = all_data if isinstance(all_data, list) else []

        console.print(f"[green]✓[/green] {len(requirements)} requirements loaded")
        console.print(f"[green]✓[/green] Running metrics: {', '.join(selected_metrics)}")
        console.print(f"[green]✓[/green] Dispatching metric agents in parallel...\n")

        # Run 10 iterations on the single SRS example
        console.print(f"\n[bold cyan]Running 10 iterations on single SRS example[/bold cyan]\n")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Evaluating...", total=10)

            for iteration in range(1, 11):
                final_report = evaluate_requirements(
                    system_desc,
                    requirements,
                    selected_metrics,
                    hitl_mode,
                    batch_label=f"Iteration {iteration}/10",
                    include_reason=args.reason,
                )

                # Save reports for this iteration
                save_reports(final_report, iteration=iteration)
                progress.advance(task)

        console.print("\n[bold]═══ All 10 iterations completed ═══[/bold]\n")


if __name__ == "__main__":
    main()