# Requirements Evaluation Agent

## **Overview**

The **Requirements Evaluation Agent** is an automated, Multi-Agent System (MAS) designed to evaluate Software Requirements Specifications (SRS). Built on top of **LangGraph** and Large Language Models (LLMs), the system provides quantifiable quality assessments of requirements against a canonical system description.

The pipeline is purposefully designed for empirical research, dataset validation, and iterative prompt engineering tests. It offers reliable, structural evaluation across multiple generations of requirements, allowing researchers to track requirement evolution and degradation.

---

## **Architectural Design**

The core architecture follows a parallel **Map-Reduce state graph** implemented via LangGraph. This ensures that every evaluation metric is assessed independently, eliminating bias between different types of metrics (e.g., a poor completeness score won't bias a testability evaluation).

### **1. State Management (`AgentState`)**

The entire pipeline revolves around a unified state dictionary that maintains context, tracks asynchronous worker outputs, and manages human review verdicts across the graph execution. Elements include the system description, requirement list, selected metrics, and aggregated reports.

### **2. Graph Nodes & Workflow**

The evaluation workflow progresses through several defined nodes in the state graph:

- **Coordinator Node**
  - **Role:** Acts as the entry point and dispatcher.
  - **Function:** Reads the canonical system description and the generated requirements. It applies a "fan-out" mechanism, dispatching independent sub-tasks (`Send`) for every metric specified via the CLI (Correctness, Completeness, Testability, Redundancy).
- **Metric Agent Nodes (Parallel Workers)**
  - **Role:** The core evaluation engine.
  - **Function:** Spawns concurrent LLM-driven worker agents for each assigned metric. Each agent performs localized evaluations, strictly scoring requirements on a 1-5 scale. They provide detailed qualitative reasoning for each quantitative score, reducing the "black box" effect of LLM evaluations.
- **Aggregator Node**
  - **Role:** The "fan-in" synchronization step.
  - **Function:** Collects the asynchronous evaluations from all active Metric Agents and synthesizes them back into the main state, preparing the data for human review or final reporting.

- **Human-In-The-Loop (HITL) Node**
  - **Role:** Quality Assurance & Expert Review.
  - **Function:** Serves as a graph interrupt mechanism. If the `--hitl` flag is active, the graph pauses execution, storing the current state via LangGraph's `MemorySaver`. It presents the evaluations to an expert reviewer who can validate, override, or approve the scores, ensuring dataset ground-truth validity.

- **Report Generation Node**
  - **Role:** Data synthesis and compilation.
  - **Function:** Compiles the approved metrics into highly structured, actionable JSON outputs. It computes statistical distributions, averages, min/max scores per metric, and metadata for batch runs.

---

## **Evaluation Capabilities & Modes**

### **Batch Evaluation Engine**

The architecture natively supports the evaluation of programmatic iterations (e.g., historical tracking of different LLM prompts from `srs_history_groq.json`).

- It parses data grouped by `prompt_version` and `generation_number`.
- Automatically generates isolated reports for each iteration and version.
- Compiles aggregate summaries detailing the progression/regression of SRS quality over different models or prompts.

### **Component-Level Metric Selection**

A highly modular CLI allows researchers to isolate evaluations:

- Run all metrics simultaneously (`--all`).
- Run specific metrics individually to save compute and target specific hypotheses (`--correctness`, `--redundancy`, etc.).
- Enable detailed explanations for scoring logic (`--reason`).

### **Output Structure**

Analysis is neatly organized into a queryable `reports/` directory structure:

```text
reports/
  ├── completeness/
  │   ├── report_v1_iter1.json
  │   └── summary.json
  ├── correctness/
  ├── redundancy/
  └── testability/
```

These highly structured JSON outputs are natively formatted for direct ingestion into analysis tools like Pandas, Jupyter Notebooks, or downstream visualization scripts.
