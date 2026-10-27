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

Example output on the 8 bundled fixture cases, scored against the fake provider
(not a real model):

```
cases: 8
metric           baseline.txt candidate.txt     delta
accuracy                 0.00          1.00     +1.00
json validity            0.00          1.00     +1.00
mean length             23.38         22.50     -0.88
```

The baseline scores 0 because it never asks for JSON, and output is only
accepted when it parses as `{"category": ...}` with a known category. Model
output is treated as untrusted: anything else counts as invalid, never repaired
or executed. Case `t08` carries an injected instruction; the candidate prompt
labels the ticket as data.

`--fail-on-regression` exits 1 when the second prompt is worse on accuracy or
JSON validity, so it can gate a prompt change in CI.

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
