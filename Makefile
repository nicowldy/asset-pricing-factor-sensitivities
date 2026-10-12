.PHONY: help install run data in-sample out-of-sample test verify lint clean

PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

help:
	@echo "Empirical Asset Pricing Pipeline - Available Commands:"
	@echo "  make install         Install pinned dependencies and the package (editable)"
	@echo "  make run             Execute full end-to-end empirical pipeline"
	@echo "  make data            Run data extraction and preprocessing"
	@echo "  make in-sample       Run in-sample econometric regressions and tests"
	@echo "  make out-of-sample   Run out-of-sample predictive forecasts & metrics"
	@echo "  make test            Run the fast test suite"
	@echo "  make verify          Re-run the pipeline in a temp dir and compare with committed outputs"
	@echo "  make lint            Check code style with ruff"
	@echo "  make clean           Remove temporary cache and build artifacts"

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install --no-deps -e .

run:
	$(PYTHON) run_pipeline.py --all

data:
	$(PYTHON) run_pipeline.py --data

in-sample:
	$(PYTHON) run_pipeline.py --in-sample

out-of-sample:
	$(PYTHON) run_pipeline.py --out-of-sample

test:
	$(PYTHON) -m pytest

verify:
	$(PYTHON) -m pytest -m golden

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
