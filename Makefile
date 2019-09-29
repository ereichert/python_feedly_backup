.PHONY: run
run:
	pipenv run python main.py


.PHONY: test
test:
	pipenv run pytest


.PHONY: watchtests
watchtests:
	pipenv run pytest-watch
