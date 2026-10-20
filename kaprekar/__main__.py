"""CLI entry point: python -m kaprekar"""

from .report import make_chart, print_report


def main() -> None:
    sweep = print_report()
    make_chart(sweep)


if __name__ == "__main__":
    main()
