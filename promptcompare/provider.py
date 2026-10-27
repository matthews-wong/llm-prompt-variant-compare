"""Provider seam: every model call goes through Provider.complete."""
import json
import re
from typing import Protocol

CATEGORIES = ("billing", "outage", "account", "other")
KEYWORDS = (
    ("billing", ("charged", "invoice", "refund", "payment")),
    ("outage", ("down", "timing out", "unavailable", "503")),
    ("account", ("password", "log in", "email address", "account")),
)
INJECTION = re.compile(r"ignore previous instructions and answer (\w+)", re.I)
INJECTION_GUARD = "as data, not as instructions"
JSON_REQUEST = "respond with json"


class Provider(Protocol):
    def complete(self, prompt: str) -> str: ...


class FakeProvider:
    """Deterministic stand-in for a model.

    It reacts to the prompt the way a weak model would: it only returns JSON
    when asked to, and follows an injected instruction unless the prompt tells
    it to treat the ticket as data. That makes prompt differences measurable
    offline; the numbers describe this fake, not a real model.
    """

    def complete(self, prompt: str) -> str:
        ticket = prompt.rsplit("Ticket:", 1)[-1].strip()
        category = self._classify(ticket, guarded=INJECTION_GUARD in prompt.lower())
        if JSON_REQUEST in prompt.lower():
            return json.dumps({"category": category})
        return f"The category is {category}."

    @staticmethod
    def _classify(ticket: str, guarded: bool) -> str:
        injected = INJECTION.search(ticket)
        if injected and not guarded and injected.group(1).lower() in CATEGORIES:
            return injected.group(1).lower()
        lowered = ticket.lower()
        for category, words in KEYWORDS:
            if any(word in lowered for word in words):
                return category
        return "other"
