"""
Batch evaluation script for multiple prompt versions and iterations.
Evaluates each prompt version + iteration combination separately and generates individual reports.

Run:
    python evaluate_all.py                    # interactive mode
    python evaluate_all.py --demo             # demo mode (uses built-in data)
    python evaluate_all.py --skipgen          # skip generation, evaluate from JSON
    python evaluate_all.py --hitl             # enable human-in-the-loop for each evaluation
"""

import json
import sys
import uuid
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
# Load system description
# ─────────────────────────────────────────────

def load_system_description() -> str:
    """Load system description from sys_description.txt"""
    try:
        with open("sys_description.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        console.print("[red]Error:[/red] sys_description.txt not found")
        sys.exit(1)


def load_requirements_from_json(json_file: str = "srs_history_groq.json") -> list:
    """Load all requirements from the JSON history file"""
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
            table.add_row(ev["req_id"], score_style(ev["score"]), ev["reason"])

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


# ─────────────────────────────────────────────
# Evaluation function
# ─────────────────────────────────────────────

def evaluate_requirements(
    system_desc: str,
    requirements: list,
    prompt_version: int,
    iteration: int,
    hitl_mode: bool = False,
) -> dict:
    """
    Run evaluation for a single set of requirements
    Returns the final report
    """
    console.print(
        f"\n[bold cyan]Evaluating Prompt v{prompt_version} — Iteration {iteration}[/bold cyan]"
    )
    console.print(f"[dim]{len(requirements)} requirements[/dim]\n")

    # Thread ID for MemorySaver
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state: AgentState = {
        "system_description": system_desc,
        "requirements": requirements,
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

    # Add metadata
    final_report["metadata"] = {
        "prompt_version": prompt_version,
        "iteration": iteration,
        "num_requirements": len(requirements),
    }

    return final_report


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    skipgen = "--skipgen" in sys.argv
    hitl_mode = "--hitl" in sys.argv

    # Load system description
    system_desc = load_system_description()
    console.print(
        Panel.fit(
            "[bold]Batch Evaluation Agent[/bold]\n"
            "Powered by LangGraph + LLM",
            border_style="blue",
        )
    )
    console.print(f"[green]✓[/green] System description loaded ({len(system_desc)} chars)\n")

    # Load all requirements from JSON
    all_data = load_requirements_from_json()
    console.print(f"[green]✓[/green] {len(all_data)} requirement sets loaded from JSON\n")

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

    console.print(f"[cyan]Found {len(evaluations)} requirement sets to evaluate:[/cyan]")
    for v, i, reqs in evaluations:
        console.print(f"  • Prompt v{v}, Iteration {i}: {len(reqs)} requirements")
    console.print()

    # Run evaluations
    reports = []

    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Evaluating...", total=len(evaluations)
        )

        for idx, (prompt_version, iteration, requirements) in enumerate(evaluations):
            # Add delay between evaluations to avoid rate limits (except first one)
            if idx > 0:
                import time
                wait_time = 5  # Wait 5 seconds between evaluations
                console.print(f"[dim]Waiting {wait_time}s before next evaluation...[/dim]")
                time.sleep(wait_time)
            
            final_report = evaluate_requirements(
                system_desc, requirements, prompt_version, iteration, hitl_mode
            )
            reports.append((prompt_version, iteration, final_report))
            progress.advance(task)

    # Save individual reports
    console.print("\n[bold]═══ Saving Reports ═══[/bold]\n")
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    for prompt_version, iteration, final_report in reports:
        report_path = report_dir / f"report_v{prompt_version}_iter{iteration}.json"
        with open(report_path, "w") as f:
            json.dump(final_report, f, indent=2)
        console.print(f"[green]✓[/green] {report_path}")

    # Save combined summary
    summary_data = {
        "system_description": system_desc,
        "timestamp": str(Path("sys_description.txt").stat().st_mtime),
        "evaluations": [
            {
                "prompt_version": v,
                "iteration": i,
                "num_requirements": len(final_report.get("requirements", [])),
                "summary": final_report.get("summary", {}),
                "report_file": f"report_v{v}_iter{i}.json",
            }
            for v, i, final_report in reports
        ],
    }

    summary_path = report_dir / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=2)

    console.print(f"[green]✓[/green] {summary_path}")
    console.print(f"\n[bold]All reports saved to [cyan]{report_dir}/[/cyan][/bold]")


if __name__ == "__main__":
    main()
