"""Core Kaprekar routine: the step function, iteration counting, validation."""

# The Kaprekar constant for 4-digit numbers.
KAPREKAR_CONSTANT = 6174


def is_valid_input(n: int) -> bool:
    """A 4-digit input is valid only if it has at least two distinct digits.

    Repdigits (1111, 2222, ...) yield 0 from the subtraction step and never
    reach 6174. Leading zeros are allowed: 0012 is treated as the digit
    string "0012" (0012 -> 2100 - 0012 = 2088 ...).
    """
    digits = f"{n:04d}"
    return len(set(digits)) > 1


def kaprekar_step(n: int) -> int:
    """One Kaprekar step: sort digits descending minus ascending (zero-padded).

    Args:
        n: an integer treated as a 4-digit string (leading zeros allowed).

    Returns:
        The result of descending - ascending, as an integer.
    """
    digits = sorted(f"{n:04d}")
    ascending = int("".join(digits))
    descending = int("".join(reversed(digits)))
    return descending - ascending


def iterations_to_6174(n: int, max_iterations: int = 64) -> int:
    """Number of Kaprekar steps to reach 6174, or raise if it never does.

    Args:
        n: starting 4-digit number (leading zeros allowed).
        max_iterations: safety bound; valid inputs always converge in <= 7.

    Raises:
        ValueError: if n is a repdigit (invalid input).
        RuntimeError: if convergence was not reached within max_iterations.
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
