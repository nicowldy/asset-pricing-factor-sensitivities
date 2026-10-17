# Asset Pricing Sector Sensitivities

Empirical pipeline for a bachelor thesis: CAPM, Fama-French 3-factor and 5-factor
models on 12 U.S. industry portfolios (July 1963 to December 2024).

## Commands

The Makefile uses `.venv/bin/python` when it exists.

- `make test` runs the fast tests (a few seconds).
- `make verify` re-runs the whole pipeline in a temp directory and compares the
  result with the committed outputs (two to three minutes).
- `make lint` runs `ruff check` and `ruff format --check`.
- `make run` regenerates everything in `data/processed`, `data/interim` and `reports/`.
- `make install` installs the pinned environment from `requirements.txt`.

## Outputs are generated, committed and reproducible

`data/processed`, `data/interim` and `reports/` are produced by the pipeline and
committed so the results can be read without running anything.

- `data/raw/` is input. Never edit it, and nothing in the pipeline writes to it.
- The pipeline is deterministic: `make run` without a code change reproduces every
  CSV and TXT output. SVGs can differ slightly with the Matplotlib backend (e.g. macOS
  vs. Agg); that is expected and not a regression.
- After a change in `asset_pricing/`, run `make verify`. It names every output that differs
  from the committed version.
- If a difference is intended, run `make run` and commit the regenerated outputs
  together with the code. If it is not intended, fix the code.
- `requirements.txt` pins the versions the outputs were produced with. A package
  upgrade can shift numbers, so check it with `make verify` as well.

## Layout

- `run_pipeline.py` is the entry point. Three stages: `--data`, `--in-sample`,
  `--out-of-sample`.
- `asset_pricing/config.py` holds every path and the model definitions (`MODELS`). Import
  from it directly; do not add per-package config modules.
- `asset_pricing/data/` aligns the raw Kenneth French files to a common sample
  (`processing.py`) and loads the result (`loaders.py`). CAPM has no raw file of its
  own: `MKT` and `RF` come from the FF3 file.
- `asset_pricing/modeling/in_sample/` holds full-sample HAC regressions (`regression.py`,
  whose `run_all_regressions` the other modules reuse), Wald tests, assumption
  diagnostics and decade-by-decade stability.
- `asset_pricing/modeling/out_of_sample/` estimates the loadings on an expanding window
  (first window 24 months), predicts the following month and tests the errors.
- `asset_pricing/modeling/tables.py` writes the result tables of both modeling stages.
- `asset_pricing/plot_style.py` holds the shared plot style and `save_figure`, the only place
  figures are written.
- Output files are prefixed with their step: `descriptive_`, `in_sample_`,
  `out_of_sample_`.

## Conventions

- All regressions use Newey-West HAC standard errors with 12 lags.
- Data CSVs in `data/processed` and `data/interim` are wrapped in `#data-begin#` and
  `#data-end#` lines. Read and write them with `asset_pricing/data/storage.py`.
- The raw industry file names one column `"Hlth "` with a trailing space. It is kept
  as is in the data; only output file names strip it.
- `in_sample_regression_*.csv` and `reports/summaries/*.txt` are full-sample results. The
  decade analysis only produces figures.
