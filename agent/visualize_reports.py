"""
Visualization script to generate bar graphs from evaluation reports.
Shows metrics on X-axis and scores from all 10 iterations on Y-axis.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Define metrics
METRICS = ["completeness", "correctness", "redundancy", "testability"]

# Create figs directory if it doesn't exist
FIGS_DIR = Path("figs")
FIGS_DIR.mkdir(exist_ok=True)

def load_all_reports():
    """Load all reports from iter1 to iter10 and extract scores."""
    reports_dir = Path("reports")
    metric_scores = {metric: [] for metric in METRICS}
    
    for iteration in range(1, 11):
        iter_dir = reports_dir / f"iter{iteration}"
        if not iter_dir.exists():
            print(f"Warning: {iter_dir} not found")
            continue
            
        for metric in METRICS:
            report_file = iter_dir / f"report_iter{iteration}_{metric}.json"
            
            if report_file.exists():
                try:
                    with open(report_file, "r") as f:
                        data = json.load(f)
                    
                    # Calculate average score for this metric in this iteration
                    evaluations = data.get("evaluations", [])
                    if evaluations:
                        avg_score = sum(e.get("score", 0) for e in evaluations) / len(evaluations)
                        metric_scores[metric].append(avg_score)
                    else:
                        metric_scores[metric].append(0)
                        
                except Exception as e:
                    print(f"Error reading {report_file}: {e}")
                    metric_scores[metric].append(0)
            else:
                print(f"File not found: {report_file}")
                metric_scores[metric].append(0)
    
    return metric_scores


def create_grouped_bar_chart(metric_scores):
    """Create a grouped bar chart with metrics on X-axis and iteration scores on Y-axis."""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Prepare data
    x = np.arange(len(METRICS))
    width = 0.08  # Width of each bar
    
    # Colors for each iteration
    colors = plt.cm.tab20(np.linspace(0, 1, 10))
    
    # Plot bars for each iteration
    for iteration in range(10):
        scores = [metric_scores[metric][iteration] if iteration < len(metric_scores[metric]) else 0 
                  for metric in METRICS]
        offset = (iteration - 4.5) * width  # Center the bars around each X position
        ax.bar(x + offset, scores, width, label=f"Iter {iteration + 1}", color=colors[iteration])
    
    # Customize the plot
    ax.set_xlabel("Metrics", fontsize=12, fontweight="bold")
    ax.set_ylabel("Average Score (1-5)", fontsize=12, fontweight="bold")
    ax.set_title("Requirements Evaluation Metrics - 10 Iterations", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([m.capitalize() for m in METRICS])
    ax.set_ylim(0, 5.5)
    ax.legend(loc="upper right", ncol=2, fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "grouped_bar_chart.png", dpi=300, bbox_inches="tight")
    print("✓ Grouped bar chart saved as 'figs/grouped_bar_chart.png'")
    plt.show()


def create_line_chart(metric_scores):
    """Create a line chart showing score trends across iterations for each metric."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    iterations = list(range(1, 11))
    colors = plt.cm.Set2(np.linspace(0, 1, len(METRICS)))
    
    for idx, metric in enumerate(METRICS):
        scores = metric_scores[metric]
        ax.plot(iterations, scores, marker="o", linewidth=2.5, markersize=8, 
                label=metric.capitalize(), color=colors[idx])
    
    # Customize the plot
    ax.set_xlabel("Iteration", fontsize=12, fontweight="bold")
    ax.set_ylabel("Average Score (1-5)", fontsize=12, fontweight="bold")
    ax.set_title("Score Trends Across 10 Iterations", fontsize=14, fontweight="bold")
    ax.set_xticks(iterations)
    ax.set_ylim(0, 5.5)
    ax.legend(loc="best", fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "trend_line_chart.png", dpi=300, bbox_inches="tight")
    print("✓ Trend line chart saved as 'figs/trend_line_chart.png'")
    plt.show()


def create_comparison_bar_chart(metric_scores):
    """Create a simple bar chart showing average scores for each metric."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate average score across all iterations for each metric
    avg_scores = {}
    for metric in METRICS:
        scores = metric_scores[metric]
        avg_scores[metric] = np.mean(scores) if scores else 0
    
    # Create bar chart
    colors = plt.cm.Set3(np.linspace(0, 1, len(METRICS)))
    bars = ax.bar(METRICS, [avg_scores[m] for m in METRICS], color=colors, edgecolor="black", linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Customize the plot
    ax.set_ylabel("Average Score (1-5)", fontsize=12, fontweight="bold")
    ax.set_title("Average Scores Across All 10 Iterations", fontsize=14, fontweight="bold")
    ax.set_ylim(0, 5.5)
    ax.set_xticklabels([m.capitalize() for m in METRICS])
    ax.grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "average_bar_chart.png", dpi=300, bbox_inches="tight")
    print("✓ Average bar chart saved as 'figs/average_bar_chart.png'")
    plt.show()


def create_box_plot(metric_scores):
    """Create a box plot (whisker plot) showing score distribution for each metric."""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Prepare data for box plot
    data = [metric_scores[metric] for metric in METRICS]
    
    # Create box plot
    bp = ax.boxplot(data, labels=[m.capitalize() for m in METRICS], patch_artist=True,
                    notch=False, showmeans=True, meanline=True,
                    medianprops=dict(color='red', linewidth=2),
                    meanprops=dict(color='blue', linewidth=2, linestyle='--'),
                    boxprops=dict(facecolor='lightblue', alpha=0.7),
                    whiskerprops=dict(linewidth=1.5),
                    capprops=dict(linewidth=1.5))
    
    # Customize the plot
    ax.set_ylabel("Score (1-5)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Metrics", fontsize=12, fontweight="bold")
    ax.set_title("Score Distribution Across 10 Iterations (Box Plot with Whiskers)", fontsize=14, fontweight="bold")
    ax.set_ylim(2, 5)
    ax.grid(axis="y", alpha=0.3)
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='red', linewidth=2, label='Median'),
        Line2D([0], [0], color='blue', linewidth=2, linestyle='--', label='Mean'),
        plt.Rectangle((0, 0), 1, 1, fc='lightblue', alpha=0.7, label='IQR (25%-75%)')
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=10)
    
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "box_plot_whiskers.png", dpi=300, bbox_inches="tight")
    print("✓ Box plot (mustache) saved as 'figs/box_plot_whiskers.png'")
    plt.show()


def print_summary(metric_scores):
    """Print a summary table of scores."""
    print("\n" + "="*80)
    print("EVALUATION SCORES SUMMARY")
    print("="*80)
    
    # Header
    header = "Metric".ljust(15) + "".join(f"Iter{i:2d}".ljust(8) for i in range(1, 11)) + "Average".ljust(10)
    print(header)
    print("-"*80)
    
    # Data rows
    for metric in METRICS:
        scores = metric_scores[metric]
        avg = np.mean(scores) if scores else 0
        row = metric.capitalize().ljust(15)
        row += "".join(f"{s:.2f}".ljust(8) for s in scores)
        row += f"{avg:.2f}".ljust(10)
        print(row)
    
    print("="*80 + "\n")


if __name__ == "__main__":
    print("\n[*] Loading reports from iter1 to iter10...\n")
    metric_scores = load_all_reports()
    
    print_summary(metric_scores)
    
    print("[*] Generating visualizations...\n")
    create_grouped_bar_chart(metric_scores)
    create_line_chart(metric_scores)
    create_comparison_bar_chart(metric_scores)
    create_box_plot(metric_scores)
    
    print("\n[✓] All visualizations completed!")
    print(f"[✓] Figures saved in 'figs/' directory\n")
