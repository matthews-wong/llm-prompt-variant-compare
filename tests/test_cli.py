import contextlib
import io
import unittest

from promptcompare.__main__ import EXIT_REGRESSION, EXIT_USAGE, main

ARGS = ["prompts/baseline.txt", "prompts/candidate.txt", "cases/tickets.jsonl"]


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def test_candidate_improves_on_baseline(self):
        code, out, _ = run(ARGS + ["--fail-on-regression"])
        self.assertEqual(code, 0)
        self.assertIn("cases: 8", out)

    def test_swapped_order_is_a_regression(self):
        code, _, err = run([ARGS[1], ARGS[0], ARGS[2], "--fail-on-regression"])
        self.assertEqual(code, EXIT_REGRESSION)
        self.assertIn("regression", err)

    def test_missing_file_is_usage_error(self):
        code, _, err = run(["nope.txt"] + ARGS[1:])
        self.assertEqual(code, EXIT_USAGE)
        self.assertIn("nope.txt", err)


if __name__ == "__main__":
    unittest.main()
