.PHONY: requirements
requirements:
	pipenv run pipenv_to_requirements
	rm requirements-dev.txt

.PHONY: dep
dep:
	pip3 install pipenv
	pipenv install --dev

.PHONY: fmt
fmt:
	pipenv run black .
	pipenv run isort .

.PHONY: lint
lint:
	pipenv run mypy .
	pipenv run flake8 .
	pipenv run isort --check .
	pipenv run black --check .