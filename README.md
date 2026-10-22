# Kaprekar's Constant — 6174

Take any 4-digit number, say **5432**. Line its digits up from biggest to
smallest (5432), then smallest to biggest (2345), and subtract:

```
5432 − 2345 = 3087
```

Now do the same thing to 3087, and to whatever comes after that. Something
funny happens: no matter which 4-digit number you start with, you always
land on **6174** — in 7 steps or fewer. And 6174 reproduces itself
(7641 − 1467 = 6174), so the loop stops there. That's why it's called
*Kaprekar's constant*, after the mathematician D. R. Kaprekar who found it.

One exception: numbers with all four digits the same, like 1111 (called
*repdigits*). Big minus small is just 0, so they never go anywhere.

Leading zeros count, by the way — 12 is really "0012", so its digits are
0, 0, 1, 2.

A quick full example, starting from 3524:

```
3524 → 5432 − 2345 = 3087
3087 → 8730 − 0378 = 8352
8352 → 8532 − 2358 = 6174 ✓
```

## What the code does

This project runs the trick on **every** 4-digit number from 0000 to 9999
(all 9,990 valid ones) and checks that every single one really does reach
6174. There are just three Python files, in the `code/` folder:

1. `code/kaprekar.py` — **the algorithm.** The Kaprekar routine itself,
   plus the full sweep over all 9,990 valid inputs.
2. `code/run_analysis.py` — **the runner.** Imports the algorithm, prints
   the results table, and draws the bar chart.
3. `tests/test_kaprekar.py` — **the tests.** 14 checks that the routine
   behaves correctly.

## Results

All 9,990 valid inputs reach 6174. Here's how many steps they took:

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

(Step 0 is just 6174 itself — it's already there.)

![Step distribution](step_distribution.png)

## Running it

From the repo root, you only need one library, `matplotlib` (for the chart):

```bash
pip install matplotlib
python code/run_analysis.py
```

## Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

The 14 tests cover: classic examples, leading-zero inputs like 0012,
repdigit rejection, the full 9,990-number sweep, and the distribution
totals.

## Project layout

```
kaprekar-analysis/
├── code/
│   ├── kaprekar.py       # the algorithm
│   └── run_analysis.py   # imports the algorithm and runs it
├── tests/
│   └── test_kaprekar.py  # the tests
├── ACKNOWLEDGEMENTS.md
├── README.md
├── LICENSE
├── .gitignore
└── requirements.txt
```

## Acknowledgements

See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) — Claude Code helped with
documentation, the MIT license, and making sure the files are all in
good shape. The analysis and implementation decisions are the author's own.