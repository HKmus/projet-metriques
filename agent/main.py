"""
Requirements Evaluation Agent — CLI entry point

Run:
    python main.py
    python main.py --demo          # uses built-in demo inputs
    python main.py --hitl          # enables human-in-the-loop review (default: auto-complete)
    python main.py --demo --hitl   # demo mode with human review
"""

import json
import sys
import uuid
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

load_dotenv()

from src.graph import graph
from src.state import AgentState, Requirement, HumanVerification
from src.prompts import METRICS

console = Console()

# ─────────────────────────────────────────────
# Demo data (used with --demo flag)
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
# Input collection
# ─────────────────────────────────────────────

def collect_inputs() -> tuple[str, list[Requirement]]:
    console.print(Panel.fit(
        "[bold]Requirements Evaluation Agent[/bold]\n"
        "Powered by LangGraph + LLM",
        border_style="blue"
    ))

    console.print("\n[bold]Step 1 — System Description[/bold]")
    console.print("[dim]Paste your system description. Enter a blank line when done.[/dim]\n")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    system_desc = "\n".join(lines).strip()

    console.print("\n[bold]Step 2 — Requirements[/bold]")
    console.print("[dim]Paste requirements one per line (format: R1: text). Enter a blank line when done.[/dim]\n")

    requirements: list[Requirement] = []
    idx = 1
    while True:
        line = input().strip()
        if line == "":
            break
        # Try to parse "R1: ..." or "R1 - ..." format
        import re
        match = re.match(r'^(R\d+)[:\-\s]+(.+)$', line, re.IGNORECASE)
        if match:
            requirements.append({"id": match.group(1).upper(), "text": match.group(2).strip()})
        else:
            requirements.append({"id": f"R{idx}", "text": line})
        idx += 1

    return system_desc, requirements


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
        table.add_column("ID",     style="bold", width=6)
        table.add_column("Score",  width=8)
        table.add_column("Reason", style="dim")

        for ev in result["evaluations"]:
            table.add_row(ev["req_id"], score_style(ev["score"]), ev["reason"])

        console.print(table)


def print_summary(final_report: dict) -> None:
    summary = final_report.get("summary", {})
    table = Table(title="Final Summary — all metrics", box=box.ROUNDED)
    table.add_column("Metric",       style="bold")
    table.add_column("Avg score",    justify="center")
    table.add_column("Min",          justify="center")
    table.add_column("Max",          justify="center")
    table.add_column("Distribution 1→5")

    for metric in METRICS:
        s = summary.get(metric, {})
        dist = s.get("distribution", {})
        dist_str = "  ".join(f"{i}×{dist.get(str(i),0)}" for i in range(1, 6))
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
# Human review loop
# ─────────────────────────────────────────────

def collect_human_verifications(metric_results: list) -> list[HumanVerification]:
    console.print("\n[bold yellow]Human Review Phase[/bold yellow]")
    console.print("For each requirement in each metric, approve or reject the agent score.\n")

    verifications: list[HumanVerification] = []

    for result in metric_results:
        metric = result["metric"]
        console.print(f"\n[bold]── {metric.upper()} ──[/bold]")

        for ev in result["evaluations"]:
            console.print(
                f"  [bold]{ev['req_id']}[/bold] scored {score_style(ev['score'])}  "
                f"[dim]{ev['reason']}[/dim]"
            )
            verdict = Prompt.ask(
                "    Verdict",
                choices=["approved", "rejected", "skip"],
                default="approved",
            )
            if verdict == "skip":
                verdict = "pending"

            comment = ""
            if verdict == "rejected":
                comment = Prompt.ask("    Comment (optional)", default="")

            verifications.append(HumanVerification(
                metric=metric,
                req_id=ev["req_id"],
                verdict=verdict,
                comment=comment,
            ))

    return verifications


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    demo_mode = "--demo" in sys.argv
    hitl_mode = "--hitl" in sys.argv

    if demo_mode:
        console.print("[dim]Running in demo mode with built-in inputs...[/dim]\n")
        system_desc = DEMO_SYSTEM_DESC
        requirements = DEMO_REQUIREMENTS
    else:
        system_desc, requirements = collect_inputs()

    if not system_desc or not requirements:
        console.print("[red]Error:[/red] System description and requirements are required.")
        sys.exit(1)

    console.print(f"\n[green]✓[/green] {len(requirements)} requirements loaded.")
    console.print(f"[green]✓[/green] Dispatching 5 metric agents in parallel...\n")

    # Thread ID used by MemorySaver to persist state across the interrupt
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state: AgentState = {
        "system_description": system_desc,
        "requirements": requirements,
        "metric_results": [],
        "human_verifications": [],
        "final_report": {},
    }

    # ── First run: coordinator → agents → aggregator → interrupt at human_review ──
    for event in graph.stream(initial_state, config=config, stream_mode="values"):
        pass  # state updates stream here; we act after the interrupt

    # After stream ends at interrupt(), inspect what paused
    current_state = graph.get_state(config)

    # LangGraph signals an interrupt via next nodes list
    if current_state.next and hitl_mode:
        # We are paused at human_review — show results then collect verdicts
        metric_results = current_state.values.get("metric_results", [])

        console.print("\n[bold]Agent Evaluation Results[/bold]\n")
        print_metric_results(metric_results)

        # Collect human verdicts
        verifications = collect_human_verifications(metric_results)

        console.print("\n[green]✓[/green] Verifications recorded. Resuming graph...\n")

        # ── Resume: pass human verifications back into the graph ──
        graph.update_state(
            config,
            {"human_verifications": verifications},
            as_node="human_review",
        )

        for event in graph.stream(None, config=config, stream_mode="values"):
            pass

    elif current_state.next and not hitl_mode:
        # Skip human review and auto-approve all evaluations
        console.print("[dim]Skipping human review (--hitl flag not provided). Completing automatically...[/dim]\n")

        metric_results = current_state.values.get("metric_results", [])
        
        # Auto-approve all evaluations
        verifications: list[HumanVerification] = []
        for result in metric_results:
            metric = result["metric"]
            for ev in result["evaluations"]:
                verifications.append(HumanVerification(
                    metric=metric,
                    req_id=ev["req_id"],
                    verdict="approved",
                    comment="",
                ))

        graph.update_state(
            config,
            {"human_verifications": verifications},
            as_node="human_review",
        )

        for event in graph.stream(None, config=config, stream_mode="values"):
            pass

    # ── Retrieve and display final report ──
    final_state = graph.get_state(config)
    final_report = final_state.values.get("final_report", {})

    console.print("\n[bold]═══ Final Report ═══[/bold]\n")
    print_summary(final_report)

    # Save JSON report
    report_path = "evaluation_report.json"
    with open(report_path, "w") as f:
        json.dump(final_report, f, indent=2)
    console.print(f"\n[dim]Full report saved to {report_path}[/dim]")


if __name__ == "__main__":
    main()
