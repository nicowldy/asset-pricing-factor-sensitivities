.PHONY: help install run data in-sample out-of-sample test clean

PYTHON ?= python3

help:
	@echo "Empirical Asset Pricing Pipeline - Available Commands:"
	@echo "  make install         Install package in editable mode with dependencies"
	@echo "  make run             Execute full end-to-end empirical pipeline"
	@echo "  make data            Run data extraction and preprocessing"
	@echo "  make in-sample       Run in-sample econometric regressions and tests"
	@echo "  make out-of-sample   Run out-of-sample predictive forecasts & metrics"
	@echo "  make test            Run test suite with pytest"
	@echo "  make clean           Remove temporary cache and build artifacts"

install:
	$(PYTHON) -m pip install -e .

run:
	$(PYTHON) run_pipeline.py --all

data:
	$(PYTHON) run_pipeline.py --data

in-sample:
	$(PYTHON) run_pipeline.py --in-sample

out-of-sample:
	$(PYTHON) run_pipeline.py --out-of-sample

test:
	$(PYTHON) -m pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
