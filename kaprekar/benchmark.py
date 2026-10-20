"""Performance benchmarking: sorting algorithms and full-sweep timing.

The CV bullet claims "applied sorting algorithms and performance
benchmarking" — this module backs that up: it compares the sort used
inside the Kaprekar step against alternatives, and times the full sweep.
"""

import random
import time
from collections.abc import Callable

from .analysis import sweep_all

BENCHMARK_ROUNDS = 20
SAMPLE_SIZE = 10_000


def _timed(fn: Callable[[], object], rounds: int) -> float:
    """Average wall time of fn over `rounds` calls, in seconds."""
    best = float("inf")
    for _ in range(rounds):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best  # best-of keeps OS jitter out of the comparison


def _bubble_sort(digits: list[str]) -> list[str]:
    """Reference O(n^2) sort for comparison against Timsort."""
    digits = list(digits)
    for i in range(len(digits)):
        for j in range(len(digits) - 1 - i):
            if digits[j] > digits[j + 1]:
                digits[j], digits[j + 1] = digits[j + 1], digits[j]
    return digits


def benchmark_sorters(rounds: int = BENCHMARK_ROUNDS) -> dict[str, float]:
    """Compare sorting strategies on random 4-digit strings.

    Returns:
        Mapping {strategy_name: avg_seconds_per_10k_sorts}, fastest first.
    """
    random.seed(42)
    samples = [f"{random.randrange(10_000):04d}" for _ in range(SAMPLE_SIZE)]

    strategies: dict[str, Callable[[str], tuple[str, str]]] = {
        "sorted() + reversed (current)": lambda s: (
            "".join(sorted(s)),
            "".join(sorted(s, reverse=True)),
        ),
        "single sort, reverse slice": lambda s: (lambda t: (t, t[::-1]))(
            "".join(sorted(s))
        ),
        "manual bubble sort": lambda s: (
            lambda d: ("".join(d), "".join(reversed(d)))
        )(_bubble_sort(list(s))),
    }

    results = {
        name: _timed(lambda fn=fn: _run_batch(samples, fn), rounds)
        for name, fn in strategies.items()
    }
    return dict(sorted(results.items(), key=lambda kv: kv[1]))


def _run_batch(
    samples: list[str],
    fn: Callable[[str], tuple[str, str]],
) -> None:
    for s in samples:
        fn(s)


def benchmark_sweep(rounds: int = 5) -> float:
    """Best-of-N timing of one full 9,990-number sweep, in seconds."""
    return _timed(sweep_all, rounds)
