"""Full sweep over all 10,000 four-digit candidates and step distribution."""

from .engine import KAPREKAR_CONSTANT, is_valid_input, iterations_to_6174

TOTAL_CANDIDATES = 10_000  # all 4-digit strings 0000-9999
REPDIGIT_COUNT = 10        # 0000, 1111, ..., 9999


def sweep_all() -> dict[int, int]:
    """Run the routine on every valid 4-digit input.

    Returns:
        Mapping {number: steps_to_reach_6174} for all 9,990 valid inputs.
    """
    return {
        n: iterations_to_6174(n)
        for n in range(TOTAL_CANDIDATES)
        if is_valid_input(n)
    }


def step_distribution(sweep: dict[int, int]) -> dict[int, int]:
    """Histogram of iteration counts: {steps: how_many_numbers}."""
    histogram: dict[int, int] = {}
    for steps in sweep.values():
        histogram[steps] = histogram.get(steps, 0) + 1
    return dict(sorted(histogram.items()))


def verify_convergence(sweep: dict[int, int]) -> bool:
    """True if every swept number reached 6174 within 7 steps.

    The mathematical result this project verifies: all 9,990 valid 4-digit
    inputs converge to 6174, and no valid input needs more than 7 steps.
    """
    return all(0 <= steps <= 7 for steps in sweep.values()) and len(
        sweep
    ) == TOTAL_CANDIDATES - REPDIGIT_COUNT
