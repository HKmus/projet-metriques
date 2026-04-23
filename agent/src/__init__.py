"""
Requirements Evaluation Agent — src package

Modules:
- state: Core data structures (AgentState, Requirement, etc.)
- agents: Agent node implementations
- graph: LangGraph workflow orchestration
- prompts: Evaluation metrics and prompts
"""

from .state import (
    AgentState,
    Requirement,
    MetricScore,
    MetricResult,
    HumanVerification,
    WorkerInput,
)
from .agents import (
    coordinator_node,
    metric_agent_node,
    aggregator_node,
    human_review_node,
    report_node,
)
from .graph import graph
from .prompts import METRICS, get_metric_prompt

__all__ = [
    # State types
    "AgentState",
    "Requirement",
    "MetricScore",
    "MetricResult",
    "HumanVerification",
    "WorkerInput",
    # Agent nodes
    "coordinator_node",
    "metric_agent_node",
    "aggregator_node",
    "human_review_node",
    "report_node",
    # Graph
    "graph",
    # Prompts
    "METRICS",
    "get_metric_prompt",
]
