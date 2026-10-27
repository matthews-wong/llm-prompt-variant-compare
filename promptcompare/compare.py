"""Run a prompt over the golden cases and summarise it."""
import json
from dataclasses import dataclass
from pathlib import Path

from .provider import Provider
from .scoring import score
from .template import render


@dataclass(frozen=True)
class Summary:
    name: str
    cases: int
    accuracy: float
    json_validity: float
    mean_length: float


def load_cases(path: Path) -> list[dict]:
    cases = []
    for number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        case = json.loads(line)
        missing = {"id", "vars", "expected"} - case.keys()
        if missing:
            raise ValueError(f"{path}:{number}: case missing {', '.join(sorted(missing))}")
        cases.append(case)
    if not cases:
        raise ValueError(f"{path}: no cases")
    return cases


def run_prompt(name: str, template: str, cases: list[dict], provider: Provider) -> Summary:
    scores = [
        score(provider.complete(render(template, case["vars"])), case["expected"])
        for case in cases
    ]
    total = len(scores)
    return Summary(
        name=name,
        cases=total,
        accuracy=sum(s.correct for s in scores) / total,
        json_validity=sum(s.valid_json for s in scores) / total,
        mean_length=sum(s.length for s in scores) / total,
    )


def format_table(baseline: Summary, candidate: Summary) -> str:
    rows = [
        ("accuracy", baseline.accuracy, candidate.accuracy),
        ("json validity", baseline.json_validity, candidate.json_validity),
        ("mean length", baseline.mean_length, candidate.mean_length),
    ]
    lines = [f"cases: {baseline.cases}", f"{'metric':<15}{baseline.name:>14}{candidate.name:>14}{'delta':>10}"]
    for label, a, b in rows:
        lines.append(f"{label:<15}{a:>14.2f}{b:>14.2f}{b - a:>+10.2f}")
    return "\n".join(lines)


def regressed(baseline: Summary, candidate: Summary) -> bool:
    return candidate.accuracy < baseline.accuracy or candidate.json_validity < baseline.json_validity
