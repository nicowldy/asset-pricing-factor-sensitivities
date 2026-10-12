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
- The pipeline is deterministic: `make run` without a code change leaves
  `git status` clean.
- After a change in `src/`, run `make verify`. It names every output that differs
  from the committed version.
- If a difference is intended, run `make run` and commit the regenerated outputs
  together with the code. If it is not intended, fix the code.
- `requirements.txt` pins the versions the outputs were produced with. A package
  upgrade can shift numbers, so check it with `make verify` as well.

## Layout

- `run_pipeline.py` is the entry point. Three stages: `--data`, `--in-sample`,
  `--out-of-sample`.
- `src/config.py` holds every path and the model definitions (`MODELS`). Import
  from it directly; do not add per-package config modules.
- `src/data/` aligns the raw Kenneth French files to a common sample. CAPM has no
  raw file of its own: `MKT` and `RF` come from the FF3 file.
- `src/modeling/in_sample/` (`expl_*`) holds full-sample HAC regressions, Wald
  tests, assumption diagnostics and decade-by-decade stability.
- `src/modeling/out_of_sample/` (`pred_*`) holds expanding-window forecasts
  (first window 24 months) and forecast-error tests.
- `src/plot_style.py` holds the shared plot style and `save_figure`, the only place
  figures are written.

## Conventions

- All regressions use Newey-West HAC standard errors with 12 lags.
- Data CSVs in `data/processed` and `data/interim` are wrapped in `#data-begin#` and
  `#data-end#` lines. Read and write them with `src/data/data_utils.py`.
- The raw industry file names one column `"Hlth "` with a trailing space. It is kept
  as is in the data; only output file names strip it.
- `expl_regress_*.csv` and `reports/other/*.txt` are full-sample results. The
  decade analysis only produces figures.
