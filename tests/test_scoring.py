import unittest

from promptcompare.scoring import parse_category, score


class ScoringTest(unittest.TestCase):
    def test_valid_correct(self):
        s = score('{"category": "billing"}', "billing")
        self.assertTrue(s.valid_json and s.correct)

    def test_valid_but_wrong(self):
        s = score('{"category": "outage"}', "billing")
        self.assertTrue(s.valid_json)
        self.assertFalse(s.correct)

    def test_prose_is_invalid(self):
        s = score("The category is billing.", "billing")
        self.assertFalse(s.valid_json or s.correct)

    def test_rejects_non_object_and_unknown_category(self):
        self.assertIsNone(parse_category("[1]"))
        self.assertIsNone(parse_category('{"category": "refunds"}'))
        self.assertIsNone(parse_category("{}"))


if __name__ == "__main__":
    unittest.main()
