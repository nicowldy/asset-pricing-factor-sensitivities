"""Golden-master test: a fresh pipeline run must reproduce the committed outputs.

Slow (two to three minutes), so it is excluded from the default run. Use `make verify`.
"""

import os
import shutil
import subprocess
import sys

import pandas as pd
import pytest

from asset_pricing.config import PROJECT_ROOT

pytestmark = pytest.mark.golden

OUTPUT_DIRS = [
    "data/processed",
    "data/interim",
    "reports/tables",
    "reports/summaries",
    "reports/figures",
]


def _files(root, pattern):
    return sorted(
        str(p.relative_to(root))
        for d in OUTPUT_DIRS
        for p in (root / d).glob(pattern)
        if p.name != ".DS_Store"
    )


@pytest.fixture(scope="module")
def fresh_run(tmp_path_factory):
    """Run the pipeline on a copy of the code and raw data, away from the repo."""
    root = tmp_path_factory.mktemp("pipeline")
    shutil.copytree(
        PROJECT_ROOT / "asset_pricing",
        root / "asset_pricing",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    shutil.copytree(PROJECT_ROOT / "data" / "raw", root / "data" / "raw")
    shutil.copy(PROJECT_ROOT / "run_pipeline.py", root)
    subprocess.run(
        [sys.executable, "run_pipeline.py", "--all"],
        cwd=root,
        check=True,
        env={**os.environ, "MPLBACKEND": "Agg"},
    )
    return root


def test_raw_data_is_not_modified(fresh_run):
    for committed in (PROJECT_ROOT / "data" / "raw").glob("*.csv"):
        fresh = fresh_run / "data" / "raw" / committed.name
        assert fresh.read_bytes() == committed.read_bytes(), committed.name


def test_same_set_of_output_files(fresh_run):
    assert _files(fresh_run, "*") == _files(PROJECT_ROOT, "*")


@pytest.mark.parametrize("rel_path", _files(PROJECT_ROOT, "*.csv"))
def test_csv_matches_committed(fresh_run, rel_path):
    committed = pd.read_csv(PROJECT_ROOT / rel_path, comment="#")
    fresh = pd.read_csv(fresh_run / rel_path, comment="#")
    # Tolerance absorbs floating-point noise between platforms and BLAS builds.
    pd.testing.assert_frame_equal(fresh, committed, rtol=1e-6, atol=1e-9)


@pytest.mark.parametrize("rel_path", _files(PROJECT_ROOT, "*.txt"))
def test_summary_matches_committed(fresh_run, rel_path):
    assert (fresh_run / rel_path).read_text() == (PROJECT_ROOT / rel_path).read_text()
