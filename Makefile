.PHONY: requirements
requirements:
	pipenv run pipenv_to_requirements
	rm requirements-dev.txt

.PHONY: lint
lint:
	pipenv run isort -rc .
	pipenv run black -l 120 .
