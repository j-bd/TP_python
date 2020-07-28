# CONFIGURATION
.DEFAULT_GOAL := help

install: requirements.txt  ## install project dependencies (requirements.txt)
	pip install -e .
	pip install -r requirements.txt
	touch install

init: ## initiate virtual environment
	bash init.sh
	touch init

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
