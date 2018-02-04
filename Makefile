.PHONY: init lint test

init:
	pip install -r requirements.txt

lint:
	pylint -E lollibot

test: lint
	python -m pytest
