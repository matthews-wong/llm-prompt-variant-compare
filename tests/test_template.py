import unittest

from promptcompare.template import TemplateError, render


class RenderTest(unittest.TestCase):
    def test_substitutes_variables(self):
        self.assertEqual(render("Hi {{ name }}!", {"name": "Ada"}), "Hi Ada!")

    def test_missing_variable_is_named(self):
        with self.assertRaisesRegex(TemplateError, "missing variables: name"):
            render("Hi {{name}}", {})

    def test_unused_variable_is_named(self):
        with self.assertRaisesRegex(TemplateError, "unused variables: extra"):
            render("Hi", {"extra": "x"})

    def test_substituted_text_is_not_rerendered(self):
        self.assertEqual(render("{{a}}", {"a": "{{b}}"}), "{{b}}")


if __name__ == "__main__":
    unittest.main()
