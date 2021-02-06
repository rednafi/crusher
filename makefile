.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


# .PHONY: venvcheck ## Check if venv is active
# venvcheck:
# ifeq ("$(VIRTUAL_ENV)","")
# 	@echo "Venv is not activated!"
# 	@echo "Activate venv first."
# 	@echo
# 	exit 1
# endif

install:  ## Install the dependencies
	@poetry install

test:		## Run the tests
	@tox

lint: 		## Run Black and Isort linters
	@black .
	@isort .

upgrade: 	## Upgrade the dependencies
	poetry update

downgrade: ## Downgrade the dependencies
	git checkout pyproject.toml && git checkout poetry.lock

publish:   ## Build and publish to PYPI
	@poetry build
	@poetry publish

coverage: ## Upload code coverage

	pytest -v -s --cov-report=xml --cov=konfik tests/

export:  ## Export pyproject.toml deps to requirements.txt
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	poetry export -f requirements.txt -o requirements-dev.txt --without-hashes --dev
