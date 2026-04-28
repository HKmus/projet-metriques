# Requirements Evaluation Agent

## **Overview**

The **Requirements Evaluation Agent** is an automated, Multi-Agent System (MAS) designed to evaluate Software Requirements Specifications (SRS). Built on top of **LangGraph** and Large Language Models (LLMs), the system provides quantifiable quality assessments of requirements against a canonical system description.

The pipeline is purposefully designed for empirical research, metric evaluation, and consistency testing. It offers two distinct modes:

1. **Single SRS Mode** (Default): Evaluates a single SRS example from `srs.json` across all 4 metrics, running **10 independent iterations** to measure metric consistency and reliability.
2. **Batch Mode**: Evaluates multiple SRS versions from `srs_history_groq.json`, tracking requirement evolution across different prompts and generations.

Both modes produce highly structured JSON reports organized by iteration, enabling detailed statistical analysis and visualization of metric performance.

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

### **Evaluation Modes**

#### **Single SRS Mode (Default)**
When loading `srs.json` (a flat array of requirements without batch metadata):
- Automatically detects single SRS format
- Runs **10 sequential iterations** on the same requirements
- Each iteration independently evaluates all 4 metrics (Completeness, Correctness, Redundancy, Testability)
- Ideal for measuring metric consistency, variability, and reliability on a single example
- Each iteration's results are saved to separate `iter1/` through `iter10/` folders

#### **Batch Evaluation Mode**
When loading `srs_history_groq.json` (with `prompt_version` and `generation_number` metadata):
- Parses data grouped by `prompt_version` and `generation_number`
- Generates isolated reports for each iteration and version
- Tracks progression/regression of SRS quality across different LLM prompts or generations

### **Component-Level Metric Selection**

A highly modular CLI allows researchers to isolate evaluations:

- Run all metrics simultaneously (`--all`, default for single SRS mode)
- Run specific metrics individually to save compute and target specific hypotheses (`--correctness`, `--redundancy`, `--completeness`, `--testability`)
- Enable detailed explanations for scoring logic (`--reason`)
- Specify custom input files with `--sys <file>` and `--json <file>`
- Enable human-in-the-loop review with `--hitl`

### **Output Structure**

#### **Single SRS Mode Output**
Reports are organized by iteration, with each metric saved as a separate file with metric suffix:

```text
reports/
  ├── iter1/
  │   ├── report_iter1_completeness.json
  │   ├── report_iter1_correctness.json
  │   ├── report_iter1_redundancy.json
  │   └── report_iter1_testability.json
  ├── iter2/
  │   ├── report_iter2_completeness.json
  │   ├── report_iter2_correctness.json
  │   ├── report_iter2_redundancy.json
  │   └── report_iter2_testability.json
  └── iter3-iter10/
      └── [Same structure for iterations 3-10]
```

#### **Batch Mode Output**
Reports maintain the same iteration-based structure with version information in filenames:

```text
reports/
  ├── iter1/
  │   ├── report_v1_iter1_completeness.json
  │   ├── report_v1_iter1_correctness.json
  │   └── ...
  ├── iter2/
  └── ...
```

Each report is a highly structured JSON file with evaluations, scores, and statistical summaries, ready for direct ingestion into analysis tools like Pandas, Jupyter Notebooks, or visualization scripts.

---

## **Visualization & Analysis**

### **Visualization Script: `visualize_reports.py`**

A comprehensive visualization tool generates multiple chart types from the evaluation reports. All figures are saved to the `figs/` directory at 300 DPI for publication-quality output.

#### **Chart Types Generated:**

1. **Grouped Bar Chart** (`grouped_bar_chart.png`)
   - X-axis: Metrics (Completeness, Correctness, Redundancy, Testability)
   - Y-axis: Scores (1-5 scale)
   - Shows all 10 iteration scores per metric with distinct colors
   - Ideal for comparing performance across iterations

2. **Trend Line Chart** (`trend_line_chart.png`)
   - X-axis: Iteration (1-10)
   - Y-axis: Scores (1-5 scale)
   - One line per metric showing score progression
   - Reveals consistency patterns and potential drift over iterations

3. **Average Bar Chart** (`average_bar_chart.png`)
   - X-axis: Metrics
   - Y-axis: Average score across all 10 iterations
   - Quick overview of overall metric performance
   - Includes value labels on bars

4. **Box Plot with Whiskers** (`box_plot_whiskers.png`)
   - X-axis: Metrics
   - Y-axis: Score range (zoomed 2-5 for clarity)
   - Shows data distribution with:
     - **Red line**: Median score
     - **Blue dashed line**: Mean score
     - **Light blue box**: Interquartile range (25%-75%)
     - **Whiskers**: Min/Max values
   - Reveals score variability and outliers

#### **Usage:**

```bash
python visualize_reports.py
```

The script automatically:
- Loads all 10 iterations from `reports/iter1/` through `reports/iter10/`
- Extracts and averages scores per metric per iteration
- Generates all 4 chart types
- Prints a summary table to console
- Saves high-resolution PNGs to `figs/`
