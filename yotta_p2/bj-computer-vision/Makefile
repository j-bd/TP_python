# CONFIGURATION
.DEFAULT_GOAL := help

init: ## initiate virtual environment
	bash init.sh
	touch init

install: ## install project dependencies
	pip install -e .
	pip install -r requirements.txt
	touch install

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
