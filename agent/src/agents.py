import json
import os
import re
import time
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from .state import AgentState, WorkerInput, MetricResult, HumanVerification
from .prompts import get_metric_prompt, METRICS

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL   = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")


def _get_llm() -> ChatGroq:
    """Return a ChatGroq instance configured for fast inference."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0,          # deterministic scoring
    )


def _invoke_llm_with_retry(llm: ChatGroq, messages: list, max_retries: int = 3) -> str:
    """Invoke LLM with exponential backoff retry on rate limit errors."""
    from groq import RateLimitError
    
    for attempt in range(max_retries):
        try:
            response = llm.invoke(messages)
            return response.content
        except RateLimitError as e:
            if attempt < max_retries - 1:
                # Extract wait time from error message if available
                error_msg = str(e)
                wait_time = 30  # default wait time
                
                # Try to extract the "Please try again in X.XXXs" from error message
                if "Please try again in" in error_msg:
                    import re as regex_module
                    match = regex_module.search(r"Please try again in ([\d.]+)s", error_msg)
                    if match:
                        wait_time = float(match.group(1)) + 2  # Add buffer
                
                print(f"  [RATE LIMIT] Waiting {wait_time:.1f}s before retry (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise  # Re-raise on final attempt
    
    raise RuntimeError("Failed to get LLM response after retries")


# ─────────────────────────────────────────────

def _format_requirements(requirements: list) -> str:
    return "\n".join(f"{r['id']}: {r['text']}" for r in requirements)


def _parse_json_response(raw: str, metric: str = None) -> dict:
    """Strip markdown fences and parse JSON robustly, handling malformed responses."""
    # Remove markdown code fences
    clean = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()
    
    # Try to parse as-is first
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON object (handle partially truncated responses)
    # Find the last closing brace and truncate there
    try:
        # Find first { and last }
        start_idx = clean.find('{')
        end_idx = clean.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = clean[start_idx:end_idx + 1]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # If still failing, try to fix common issues (unterminated strings, trailing commas)
    try:
        # Fix unterminated strings by closing them
        fixed = re.sub(r'(["\'])\s*(["\']|\})', r'\1\2', clean)
        # Remove trailing commas before closing braces/brackets
        fixed = re.sub(r',(\s*[}\]])', r'\1', fixed)
        return json.loads(fixed)
    except json.JSONDecodeError as e:
        print(f"  [WARNING] Failed to parse JSON response: {e}")
        print(f"  [DEBUG] Raw response:\n{clean[:500]}...")
        # Return default response with correct metric
        return {
            "metric": metric if metric else "unknown",
            "evaluations": []
        }


# ─────────────────────────────────────────────
# Node 1 — Coordinator
# Validates input, returns unchanged state.
# The graph uses this node to fan-out via Send().
# ─────────────────────────────────────────────

def coordinator_node(state: AgentState) -> dict:
    selected_metrics = state.get("selected_metrics", METRICS)
    print(f"\n[Coordinator] Model : {GROQ_MODEL} (Groq)")
    print(f"[Coordinator] Received {len(state['requirements'])} requirements.")
    print(f"[Coordinator] Dispatching {len(selected_metrics)} metric agents in parallel...\n")

    if not state["system_description"]:
        raise ValueError("system_description is required.")
    if not state["requirements"]:
        raise ValueError("requirements list is empty.")

    return {}


# ─────────────────────────────────────────────
# Node 2 — Metric evaluation worker
# One instance runs per metric (via Send).
# ─────────────────────────────────────────────

def metric_agent_node(worker_input: WorkerInput) -> dict:
    metric     = worker_input["metric"]
    include_reason = worker_input.get("include_reason", False)
    system_prompt = get_metric_prompt(metric, include_reason)
    req_text   = _format_requirements(worker_input["requirements"])

    user_content = (
        f"System Description:\n{worker_input['system_description']}\n\n"
        f"Requirements:\n{req_text}"
    )

    print(f"  [{metric.upper()} agent] Evaluating {len(worker_input['requirements'])} requirements...")

    llm = _get_llm()
    response_content = _invoke_llm_with_retry(llm, [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content),
    ])

    parsed: MetricResult = _parse_json_response(response_content, metric=metric)
    print(f"  [{metric.upper()} agent] Done. Scored {len(parsed['evaluations'])} requirements.")

    return {"metric_results": [parsed]}


# ─────────────────────────────────────────────
# Node 3 — Aggregator
# Collects all metric results and computes summary stats.
# ─────────────────────────────────────────────

def aggregator_node(state: AgentState) -> dict:
    print("\n[Aggregator] All agents finished. Computing summary stats...")

    summary: dict = {}
    for result in state["metric_results"]:
        metric = result["metric"]
        scores = [e["score"] for e in result["evaluations"]]
        summary[metric] = {
            "average": round(sum(scores) / len(scores), 2) if scores else 0,
            "min": min(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "distribution": {str(i): scores.count(i) for i in range(1, 6)},
        }

    print("[Aggregator] Summary computed. Passing to human review.\n")
    return {"final_report": {"summary": summary}}


# ─────────────────────────────────────────────
# Node 4 — Human review  (interrupt point)
# The graph pauses here. The CLI resumes it
# by injecting human_verifications into the state.
# ─────────────────────────────────────────────

def human_review_node(state: AgentState) -> dict:
    from langgraph.types import interrupt

    print("\n" + "═" * 60)
    print("  HUMAN REVIEW — Evaluation paused")
    print("  The graph will resume once you submit your verifications.")
    print("═" * 60 + "\n")

    # interrupt() suspends the graph and surfaces the payload to the caller.
    # The caller (main.py) resumes the graph by passing human_verifications back.
    verifications = interrupt({
        "message": "Please review the metric scores and return your verifications.",
        "metric_results": state["metric_results"],
    })

    return {"human_verifications": verifications}


# ─────────────────────────────────────────────
# Node 5 — Final report builder
# Merges agent scores with human verifications
# and produces the final structured report.
# ─────────────────────────────────────────────

def report_node(state: AgentState) -> dict:
    print("\n[Report] Building final report...")

    # Index human verifications for fast lookup
    verif_index: dict[tuple, HumanVerification] = {}
    for v in (state.get("human_verifications") or []):
        verif_index[(v["metric"], v["req_id"])] = v

    report_metrics: dict = {}
    for result in state["metric_results"]:
        metric = result["metric"]
        enriched = []
        for ev in result["evaluations"]:
            verif = verif_index.get((metric, ev["req_id"]))
            enriched.append({
                **ev,
                "human_verdict": verif["verdict"] if verif else "pending",
                "human_comment": verif.get("comment", "") if verif else "",
            })
        report_metrics[metric] = enriched

    final_report = {
        **state.get("final_report", {}),
        "metrics": report_metrics,
        "requirements_count": len(state["requirements"]),
        "metrics_evaluated": len(METRICS),
    }

    print("[Report] Final report ready.\n")
    return {"final_report": final_report}
