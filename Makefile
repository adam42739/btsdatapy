init: ## Initialize the development environment
	uv sync

build: ## Build the package
	uv build

pre-commit-install: ## Install pre-commit hooks
	uv run pre-commit install

pre-commit: ## Run pre-commit checks
	uv run pre-commit run --all-files

unit-tests: ## Run unit tests with coverage report
	uv run pytest --cov=src/btsdatapy --cov-report=html