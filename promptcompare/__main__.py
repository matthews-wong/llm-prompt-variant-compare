import argparse
import sys
from pathlib import Path

from .compare import format_table, load_cases, regressed, run_prompt
from .provider import FakeProvider
from .template import TemplateError

EXIT_REGRESSION = 1
EXIT_USAGE = 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="promptcompare", description="Compare two prompt versions.")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("cases", type=Path)
    parser.add_argument("--fail-on-regression", action="store_true")
    args = parser.parse_args(argv)

    provider = FakeProvider()
    try:
        cases = load_cases(args.cases)
        base = run_prompt(args.baseline.name, args.baseline.read_text(), cases, provider)
        cand = run_prompt(args.candidate.name, args.candidate.read_text(), cases, provider)
    except (OSError, ValueError, TemplateError) as err:
        print(f"error: {err}", file=sys.stderr)
        return EXIT_USAGE

    print(format_table(base, cand))
    if args.fail_on_regression and regressed(base, cand):
        print("regression: candidate is worse than baseline", file=sys.stderr)
        return EXIT_REGRESSION
    return 0


if __name__ == "__main__":
    sys.exit(main())
