"""Score one model output against the expected category."""
import json
from dataclasses import dataclass

from .provider import CATEGORIES


@dataclass(frozen=True)
class Score:
    valid_json: bool
    correct: bool
    length: int


def parse_category(output: str) -> str | None:
    """Return the category from a JSON output, or None if it is not valid."""
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    category = data.get("category")
    return category if category in CATEGORIES else None


def score(output: str, expected: str) -> Score:
    category = parse_category(output)
    return Score(valid_json=category is not None, correct=category == expected, length=len(output))
