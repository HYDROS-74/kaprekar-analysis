"""Kaprekar Routine analysis engine.

Tools for analyzing the Kaprekar routine on 4-digit numbers:
the iteration 5432 - 2345 = 3087 (digits sorted descending minus ascending,
zero-padded) which converges to 6174 for every valid 4-digit input.
"""

__version__ = "1.0.0"

from .engine import kaprekar_step, iterations_to_6174, is_valid_input
from .analysis import sweep_all, step_distribution
from .benchmark import benchmark_sorters, benchmark_sweep

__all__ = [
    "kaprekar_step",
    "iterations_to_6174",
    "is_valid_input",
    "sweep_all",
    "step_distribution",
    "benchmark_sorters",
    "benchmark_sweep",
]
