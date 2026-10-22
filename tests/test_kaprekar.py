"""Tests for the Kaprekar analysis.

Run with pytest (python -m pytest tests/ -v) or directly in VS Code.
"""

import os
import sys

# Make the code folder importable regardless of how this file is launched.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "code"))

import pytest

from kaprekar import (
    KAPREKAR_CONSTANT,
    REPDIGIT_COUNT,
    TOTAL_CANDIDATES,
    is_valid_input,
    iterations_to_6174,
    kaprekar_step,
    step_distribution,
    sweep_all,
    verify_convergence,
)


class TestKaprekarStep:
    def test_classic_example(self):
        # 5432 - 2345 = 3087
        assert kaprekar_step(5432) == 3087

    def test_leading_zeros_handled(self):
        # 0012 -> digits 0,0,1,2: 2100 - 0012 = 2088
        assert kaprekar_step(12) == 2088

    def test_constant_reproduces_itself(self):
        # 6174 is a fixed point: 7641 - 1467 = 6174
        assert kaprekar_step(6174) == KAPREKAR_CONSTANT


class TestIterationsTo6174:
    def test_constant_needs_zero_steps(self):
        assert iterations_to_6174(6174) == 0

    def test_known_path_3524(self):
        # Hand-checked chain: 5432-2345=3087 -> 8730-0378=8352 -> 8532-2358=6174
        assert iterations_to_6174(3524) == 3

    def test_all_valid_inputs_converge_within_7_steps(self):
        sweep = sweep_all()
        assert max(sweep.values()) <= 7

    def test_repdigit_raises(self):
        with pytest.raises(ValueError):
            iterations_to_6174(1111)

    def test_zero_is_repdigit(self):
        with pytest.raises(ValueError):
            iterations_to_6174(0)


class TestValidation:
    def test_repdigits_invalid(self):
        for n in (0, 1111, 2222, 9999):
            assert not is_valid_input(n)

    def test_normal_numbers_valid(self):
        assert is_valid_input(6174)
        assert is_valid_input(1)  # 0001 has digits 0,0,0,1


class TestFullSweep:
    def test_sweep_covers_all_valid_inputs(self):
        sweep = sweep_all()
        assert len(sweep) == TOTAL_CANDIDATES - REPDIGIT_COUNT
        assert len(sweep) == 9_990

    def test_convergence_verified(self):
        assert verify_convergence(sweep_all())

    def test_distribution_sums_to_valid_count(self):
        sweep = sweep_all()
        distribution = step_distribution(sweep)
        assert sum(distribution.values()) == 9_990

    def test_distribution_step_range(self):
        distribution = step_distribution(sweep_all())
        assert set(distribution) == {0, 1, 2, 3, 4, 5, 6, 7}  # 0 = 6174 itself


if __name__ == "__main__":
    # Allow direct execution (e.g. VS Code "Run Python File") to run the suite.
    sys.exit(pytest.main([os.path.abspath(__file__), "-v"]))