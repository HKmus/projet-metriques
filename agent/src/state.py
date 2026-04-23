from typing import Annotated, Any
from typing_extensions import TypedDict
import operator


class Requirement(TypedDict):
    id: str
    text: str


class MetricScore(TypedDict, total=False):
    req_id: str
    score: int          # 1–5
    reason: str


class MetricResult(TypedDict):
    metric: str
    evaluations: list[MetricScore]


class HumanVerification(TypedDict):
    metric: str
    req_id: str
    verdict: str        # "approved" | "rejected" | "pending"
    comment: str


# operator.add lets multiple parallel agents append to the same list
class AgentState(TypedDict, total=False):
    system_description: str
    requirements: list[Requirement]
    selected_metrics: list[str]  # which metrics to run
    include_reason: bool         # flag to include reasoning
    
    # parallel agents write here — operator.add merges lists safely
    metric_results: Annotated[list[MetricResult], operator.add]

    # human review fills this in after interrupt()
    human_verifications: list[HumanVerification]

    # final synthesised report
    final_report: dict[str, Any]


# Sub-state each parallel worker receives via Send()
class WorkerInput(TypedDict, total=False):
    system_description: str
    requirements: list[Requirement]
    metric: str         # which metric this worker handles
    include_reason: bool
