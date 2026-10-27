.PHONY: validate test compare

validate: test compare

test:
	python3 -m unittest discover -s tests

compare:
	python3 -m promptcompare prompts/baseline.txt prompts/candidate.txt cases/tickets.jsonl --fail-on-regression
