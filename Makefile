export REPOSITORY=flyte-app

.SILENT: help
.PHONY: help
help:
	echo Available recipes:
	cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN { FS = ":.*?## " } { cnt++; a[cnt] = $$1; b[cnt] = $$2; if (length($$1) > max) max = length($$1) } END { for (i = 1; i <= cnt; i++) printf "  $(shell tput setaf 6)%-*s$(shell tput setaf 0) %s\n", max, a[i], b[i] }'
	tput sgr0

.PHONY: setup
setup: ## Install requirements
	pip install -U pip-tools pip==21.2.4
	pip install -r requirements.txt

.PHONY: fmt
fmt: ## Format code with black and isort
	pre-commit run black --all-files || true
	pre-commit run isort --all-files || true
