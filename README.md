# llm-prompt-variant-compare

Run two versions of a prompt over the same labelled cases and compare them
side by side: label accuracy, JSON validity and output length. Everything runs
offline against a deterministic fake provider, so a prompt edit can be judged
in a diff before it ever reaches a real model.

The task used here is support-ticket triage (billing / outage / account / other).

## Usage

```sh
python3 -m promptcompare prompts/baseline.txt prompts/candidate.txt cases/tickets.jsonl
python3 -m promptcompare prompts/baseline.txt prompts/candidate.txt cases/tickets.jsonl --fail-on-regression
```

## Layout

- `prompts/` - prompt templates with `{{variable}}` placeholders
- `cases/` - JSONL golden cases: `id`, `vars`, `expected`
- `promptcompare/` - renderer, provider interface, scoring, report

## Providers

Every call goes through `Provider.complete(prompt) -> str`. The bundled
`FakeProvider` is rule-based and deterministic. A real adapter only needs to
implement that one method; nothing here requires one to run.

## Validation

```sh
make validate
```
