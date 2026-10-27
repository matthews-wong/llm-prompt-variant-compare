"""Strict {{variable}} rendering: a missing or unused variable is an error."""
import re

PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")


class TemplateError(ValueError):
    pass


def placeholders(template: str) -> set[str]:
    return set(PLACEHOLDER.findall(template))


def render(template: str, variables: dict[str, str]) -> str:
    needed = placeholders(template)
    missing = needed - variables.keys()
    if missing:
        raise TemplateError(f"missing variables: {', '.join(sorted(missing))}")
    unused = variables.keys() - needed
    if unused:
        raise TemplateError(f"unused variables: {', '.join(sorted(unused))}")
    return PLACEHOLDER.sub(lambda m: str(variables[m.group(1)]), template)
