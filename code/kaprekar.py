"""The Kaprekar routine and the full analysis over all 4-digit numbers.

The routine: sort a number's digits biggest-to-smallest and
smallest-to-biggest, then subtract. Every valid 4-digit number ends at
6174 — Kaprekar's constant — within 7 steps.
"""

# Every valid 4-digit number ends up here. 6174 is a "fixed point":
# 7641 - 1467 = 6174, so once you arrive, you stay.
KAPREKAR_CONSTANT = 6174

TOTAL_CANDIDATES = 10_000  # all 4-digit strings 0000-9999
REPDIGIT_COUNT = 10        # 0000, 1111, ..., 9999 — the invalid ones


def is_valid_input(n: int) -> bool:
    """A number is valid if its 4 digits are not all the same.

    Numbers like 1111 or 7777 (called "repdigits") give 0 when you
    subtract small-from-big, so the routine can never take off.
    Leading zeros count: 12 is really the digit string "0012".
    """
    digits = f"{n:04d}"
    return len(set(digits)) > 1


def kaprekar_step(n: int) -> int:
    """One Kaprekar step: (digits biggest-to-smallest) - (smallest-to-biggest).

    Example: 5432 -> digits sorted down = 5432, sorted up = 2345,
    so the result is 5432 - 2345 = 3087.

    The number is treated as a 4-digit string, so leading zeros are kept
    (12 counts as "0012", which sorts to "0012" and "2100").
    """
    digits = sorted(f"{n:04d}")          # digits from smallest to biggest
    ascending = int("".join(digits))
    descending = int("".join(reversed(digits)))
    return descending - ascending


def iterations_to_6174(n: int, max_iterations: int = 64) -> int:
    """How many Kaprekar steps until n reaches 6174?

    Args:
        n: starting number (leading zeros allowed).
        max_iterations: a safety net so a broken loop can't run forever.
            Real inputs always finish within 7 steps.

    Raises:
        ValueError: if n is a repdigit (invalid input).
        RuntimeError: if 6174 wasn't reached within max_iterations steps.
    """
    if not is_valid_input(n):
        raise ValueError(f"{n:04d} is a repdigit — the routine never converges")

    current = n
    steps = 0
    while current != KAPREKAR_CONSTANT:
        current = kaprekar_step(current)
        steps += 1
        if steps > max_iterations:
            raise RuntimeError(
                f"{n:04d} did not reach {KAPREKAR_CONSTANT} "
                f"within {max_iterations} steps"
            )
    return steps


def sweep_all() -> dict[int, int]:
    """Run the Kaprekar routine on every valid 4-digit input.

    Returns:
        A dictionary like {number: steps_needed}, one entry for each of
        the 9,990 valid numbers (the 10 repdigits are left out).
    """
    return {
        n: iterations_to_6174(n)
        for n in range(TOTAL_CANDIDATES)
        if is_valid_input(n)
    }


def step_distribution(sweep: dict[int, int]) -> dict[int, int]:
    """Count how many numbers finished in 0 steps, 1 step, 2 steps, and so on."""
    histogram: dict[int, int] = {}
    for steps in sweep.values():
        histogram[steps] = histogram.get(steps, 0) + 1
    return dict(sorted(histogram.items()))


def verify_convergence(sweep: dict[int, int]) -> bool:
    """True if every swept number reached 6174 within 7 steps.

    This is the heart of the project: checking the famous result that
    all 9,990 valid inputs converge, and none needs more than 7 steps.
    """
    return all(0 <= steps <= 7 for steps in sweep.values()) and len(
        sweep
    ) == TOTAL_CANDIDATES - REPDIGIT_COUNT