# Requirements Evaluation Agent

A multi-agent framework designed to automatically evaluate software requirements documents for quality and completeness. This project uses LangGraph to create a parallel pipeline of specialized LLM agents, each evaluating requirements against a specific quality metric (correctness, completeness, edge cases, redundancy, and testability). The framework combines automated AI evaluation with human-in-the-loop verification, enabling comprehensive assessment of requirements while maintaining human oversight and approval at critical gates.

---

## Architecture

```
[coordinator_node]
       │
       │  Send() × 5 — parallel fan-out
       ├──────────────────────────────────────────────┐
       ▼              ▼             ▼          ▼       ▼
[correctness]  [completeness]  [edge_cases] [redundancy] [testability]
       │              │             │          │       │
       └──────────────┴─────────────┴──────────┴───────┘
                                   │  fan-in (operator.add)
                            [aggregator_node]
                                   │
                            [human_review_node]  ← interrupt() here
                                   │  graph pauses, CLI collects verdicts
                                   │  graph.update_state() + stream(None) resumes
                              [report_node]
                                   │
                                 [END]
```

### Nodes

| Node           | Role                                                                     |
| -------------- | ------------------------------------------------------------------------ |
| `coordinator`  | Validates input, triggers fan-out via `Send()`                           |
| `metric_agent` | One instance per metric — calls LLM with a metric-specific system prompt |
| `aggregator`   | Merges all parallel results, computes avg/min/max/distribution           |
| `human_review` | Calls `interrupt()` — pauses graph for human approval                    |
| `report`       | Merges agent scores with human verdicts, writes final report             |

### State keys

| Key                   | Type                            | Description                          |
| --------------------- | ------------------------------- | ------------------------------------ |
| `system_description`  | `str`                           | The system the requirements describe |
| `requirements`        | `list[Requirement]`             | Parsed list of `{id, text}` dicts    |
| `metric_results`      | `Annotated[list, operator.add]` | Parallel agents append here safely   |
| `human_verifications` | `list[HumanVerification]`       | Injected after interrupt resumes     |
| `final_report`        | `dict`                          | Final merged report with all scores  |

---

## Project structure

```
├── main.py                  # CLI entry point
├── requirements.txt
├── .env                     # API credentials (GROQ_API_KEY, GROQ_MODEL)
├── src/
│   ├── __init__.py
│   ├── state.py             # TypedDicts: AgentState, WorkerInput, MetricResult, etc.
│   ├── prompts.py           # System prompts for all 5 metric agents
│   ├── agents.py            # Node functions (coordinator, agents, aggregator, report)
│   └── graph.py             # StateGraph definition + Send fan-out + MemorySaver
└── reports/                 # Generated evaluation reports
```

---

## Setup

### 1. Get a Groq API Key

Sign up at [console.groq.com](https://console.groq.com) to get a free API key.

### 2. Clone/copy the project

```bash
cd /path/to/project
```

### 3. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create or update `.env` with your Groq credentials:

```bash
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

### 6. Run

**Demo mode** (uses built-in system description + 8 requirements):

```bash
python main.py --demo
```

**Interactive mode** (paste your own inputs):

```bash
python main.py
```

---

## Example session

```
Requirements Evaluation Agent
Powered by LangGraph + LLM

Step 1 — System Description
> An online bookstore where users browse and purchase books...
>                          ← blank line to finish

Step 2 — Requirements
> R1: The system shall allow users to register using email and password.
> R2: Users should be able to log in.
>                          ← blank line to finish

✓ 2 requirements loaded.
✓ Dispatching 5 metric agents in parallel...

  [CORRECTNESS agent]  Evaluating 2 requirements...
  [COMPLETENESS agent] Evaluating 2 requirements...
  [EDGE_CASES agent]   Evaluating 2 requirements...
  [REDUNDANCY agent]   Evaluating 2 requirements...
  [TESTABILITY agent]  Evaluating 2 requirements...

Agent Evaluation Results

CORRECTNESS — avg: 4.5/5
  R1  5/5  Accurately reflects registration described in the spec.
  R2  4/5  Correct but vague on authentication method.

═══════════════════════════════════
Human Review Phase
═══════════════════════════════════
  R1 scored 5/5  Accurately reflects registration...
    Verdict [approved/rejected/skip]: approved
  R2 scored 4/5  Correct but vague on authentication...
    Verdict [approved/rejected/skip]: rejected
    Comment: Score should be 3 — no mention of session handling.

✓ Verifications recorded. Resuming graph...

═══ Final Report ═══
Metric         Avg   Min  Max  Distribution
correctness    4.5   4    5    1×0  2×0  3×0  4×1  5×1
...

Full report saved to evaluation_report.json
```

---

## Swapping the checkpointer for production

`MemorySaver` stores state in RAM — it resets when the process restarts.
For production, use a persistent checkpointer:

````python
# SQLite (single-file, great for local / dev)
from langgraph.checkpoint.sqlite import SqliteSaver
checkpointer = SqliteSaver.from_conn_string("evaluations.db")

# PostgreSQL (production)

**Export report**
The JSON report at `evaluation_report.json` can be fed into any reporting tool.
The structure is:

```json
{
  "summary": { "correctness": { "average": 4.1, "min": 2, "max": 5, "distribution": {...} }, ... },
  "metrics": {
    "correctness": [
      { "req_id": "R1", "score": 5, "reason": "...", "human_verdict": "approved", "human_comment": "" },
      ...
    ]
  },
  "requirements_count": 8,
  "metrics_evaluated": 5
}
````
