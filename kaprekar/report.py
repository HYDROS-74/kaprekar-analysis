"""Console report and chart generation."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .analysis import REPDIGIT_COUNT, TOTAL_CANDIDATES, step_distribution, sweep_all, verify_convergence
from .benchmark import benchmark_sorters, benchmark_sweep
from .engine import KAPREKAR_CONSTANT

CHART_PATH = "step_distribution.png"


def print_report() -> dict[int, int]:
    """Print the full analysis report to the console; return the sweep."""
    print("Kaprekar Routine — Algorithmic Analysis")
    print("=" * 48)

    sweep = sweep_all()
    distribution = step_distribution(sweep)
    total_valid = len(sweep)

    print(f"\nCandidates processed : {TOTAL_CANDIDATES} (all 4-digit strings 0000-9999)")
    print(f"Valid inputs         : {total_valid} ({REPDIGIT_COUNT} repdigits excluded)")
    print(f"Target constant      : {KAPREKAR_CONSTANT}")
    print(f"Convergence verified : {'YES' if verify_convergence(sweep) else 'NO'}")

    print("\nStep distribution (iterations needed to reach 6174):")
    print(f"  {'steps':>5} | {'numbers':>8} | {'share':>7} | bar")
    print("  " + "-" * 48)
    for steps, count in distribution.items():
        share = count / total_valid
        bar = "#" * round(share * 40)
        print(f"  {steps:>5} | {count:>8} | {share:>6.1%} | {bar}")
    print(f"\n  max steps: {max(distribution)}, min steps: {min(distribution)}")

    print("\nSort-strategy benchmark (best of 20 rounds, 10k random digit strings):")
    for name, seconds in benchmark_sorters().items():
        print(f"  {seconds * 1000:>8.1f} ms  {name}")

    sweep_seconds = benchmark_sweep()
    print(f"\nFull sweep timing: {sweep_seconds * 1000:.1f} ms "
          f"({total_valid / sweep_seconds:,.0f} numbers/second)")

    print(f"\nChart written to {CHART_PATH}")
    return sweep


def make_chart(sweep: dict[int, int]) -> None:
    """Render the step-distribution bar chart to PNG."""
    distribution = step_distribution(sweep)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(distribution.keys(), distribution.values(), color="#4a7fb5", edgecolor="#2c5478")
    ax.set_xlabel("Kaprekar steps to reach 6174")
    ax.set_ylabel("Number of inputs")
    ax.set_title("Convergence speed of 9,990 valid 4-digit inputs")
    ax.set_xticks(list(distribution.keys()))
    for x, count in distribution.items():
        ax.text(x, count + max(distribution.values()) * 0.01, str(count),
                ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(CHART_PATH, dpi=150)
    plt.close(fig)
