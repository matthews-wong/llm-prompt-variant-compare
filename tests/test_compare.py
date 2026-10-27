import tempfile
import unittest
from pathlib import Path

from promptcompare.compare import load_cases, regressed, run_prompt
from promptcompare.provider import FakeProvider

CASES = [
    {"id": "a", "vars": {"ticket": "I was charged twice"}, "expected": "billing"},
    {"id": "b", "vars": {"ticket": "The site is down"}, "expected": "outage"},
]
PLAIN = "Classify.\nTicket: {{ticket}}"
JSON = "Respond with JSON only.\nTicket: {{ticket}}"


class CompareTest(unittest.TestCase):
    def test_json_prompt_beats_prose_prompt(self):
        base = run_prompt("base", PLAIN, CASES, FakeProvider())
        cand = run_prompt("cand", JSON, CASES, FakeProvider())
        self.assertEqual((base.accuracy, cand.accuracy), (0.0, 1.0))
        self.assertFalse(regressed(base, cand))
        self.assertTrue(regressed(cand, base))

    def test_load_cases_names_the_bad_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.jsonl"
            path.write_text('{"id": "a", "vars": {}}\n')
            with self.assertRaisesRegex(ValueError, r"c.jsonl:1: case missing expected"):
                load_cases(path)

    def test_load_cases_rejects_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.jsonl"
            path.write_text("\n")
            with self.assertRaisesRegex(ValueError, "no cases"):
                load_cases(path)


if __name__ == "__main__":
    unittest.main()
