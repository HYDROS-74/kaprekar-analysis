# Algorithmic Analysis of Kaprekar Routine

A Python engine that processes **all 10,000 four-digit strings (0000–9999)** and
verifies that every valid one converges to **6174**, the Kaprekar constant.

## The routine

Given any 4-digit number with at least two distinct digits (leading zeros
allowed):

1. Arrange its digits in **descending** order.
2. Arrange them in **ascending** order.
3. Subtract: `descending − ascending`.
4. Repeat with the result.

Every valid input reaches **6174** in at most **7** steps — and 6174 is a fixed
point, since `7641 − 1467 = 6174`. The 10 repdigits (0000, 1111, …, 9999) are
excluded: their subtraction always yields 0, so they never converge.

Example — starting from `5432`:

```
5432 → 3087 → 8352 → 6174
```

## What this project does

- **Iterative analysis engine** — implements the routine with correct
  leading-zero handling and repdigit rejection (`kaprekar/engine.py`).
- **Full sweep** — runs the engine over all 9,990 valid 4-digit inputs and
  proves every one reaches 6174 (`kaprekar/analysis.py`).
- **Step distribution** — reports how many inputs terminate in 0–7 iterations.
- **Performance benchmarking** — compares digit-sorting strategies (Timsort
  via `sorted()`, a reverse-slice variant, and a manual bubble sort) and times
  the full sweep (`kaprekar/benchmark.py`).
- **Reporting** — console table plus a PNG bar chart (`kaprekar/report.py`).

## Results

All 9,990 valid inputs converge to 6174. Distribution of steps needed:

| Steps | Inputs | Share  |
|:-----:|-------:|-------:|
| 0     | 1      | 0.0%   |
| 1     | 383    | 3.8%   |
| 2     | 576    | 5.8%   |
| 3     | 2400   | 24.0%  |
| 4     | 1272   | 12.7%  |
| 5     | 1518   | 15.2%  |
| 6     | 1656   | 16.6%  |
| 7     | 2184   | 21.9%  |

![Step distribution](step_distribution.png)

## How to run

```bash
pip install matplotlib        # only dependency; the engine is stdlib-only
python -m kaprekar            # full sweep + distribution + benchmarks + chart
```

## Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

14 tests cover: classic examples, leading-zero inputs, repdigit rejection,
full-sweep convergence, and distribution totals.

## Project layout

```
kaprekar-analysis/
├── kaprekar/
│   ├── __init__.py
│   ├── __main__.py     # CLI entry point
│   ├── engine.py       # core routine: step, iteration counting, validation
│   ├── analysis.py     # full sweep + step distribution
│   ├── benchmark.py    # sorting-strategy and sweep timing benchmarks
│   └── report.py       # console report + chart
├── tests/
│   └── test_kaprekar.py
├── ACKNOWLEDGEMENTS.md
├── README.md
├── .gitignore
└── requirements.txt
```

## Acknowledgements

See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) — Claude Code was used to
assist with debugging and documentation polish; all analysis and
implementation decisions are the author's own.
