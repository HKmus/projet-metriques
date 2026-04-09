from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Send

from .state import AgentState, WorkerInput
from .agents import (
    coordinator_node,
    metric_agent_node,
    aggregator_node,
    human_review_node,
    report_node,
)
from .prompts import METRICS


# ─────────────────────────────────────────────
# Fan-out edge: coordinator → one Send per metric
# LangGraph calls this function on the coordinator's
# output and spawns a parallel worker for each Send.
# ─────────────────────────────────────────────

def dispatch_to_agents(state: AgentState) -> list[Send]:
    return [
        Send(
            "metric_agent",           # target node name
            WorkerInput(
                system_description=state["system_description"],
                requirements=state["requirements"],
                metric=metric,
            ),
        )
        for metric in METRICS
    ]


# ─────────────────────────────────────────────
# Graph assembly
# ─────────────────────────────────────────────

def build_graph() -> StateGraph:
    builder = StateGraph(AgentState)

    # Register nodes
    builder.add_node("coordinator",   coordinator_node)
    builder.add_node("metric_agent",  metric_agent_node)
    builder.add_node("aggregator",    aggregator_node)
    builder.add_node("human_review",  human_review_node)
    builder.add_node("report",        report_node)

    # Entry point
    builder.set_entry_point("coordinator")

    # coordinator → parallel metric agents (fan-out via Send)
    builder.add_conditional_edges(
        "coordinator",
        dispatch_to_agents,
        # No explicit target map needed — Send() carries the target node name
    )

    # All parallel metric_agent instances → aggregator (fan-in is automatic)
    builder.add_edge("metric_agent", "aggregator")

    # aggregator → human review (interrupt lives inside this node)
    builder.add_edge("aggregator", "human_review")

    # human review → final report
    builder.add_edge("human_review", "report")

    # End
    builder.add_edge("report", END)

    # MemorySaver persists state across the interrupt/resume cycle.
    # Swap for SqliteSaver or PostgresSaver in production.
    checkpointer = MemorySaver()

    return builder.compile(checkpointer=checkpointer)


# Singleton — import this in main.py
graph = build_graph()
