from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from asset_pricing.config import (
    FIG_PRED_COMPEXAM,
    FIG_PRED_RMSE,
    FIG_PRED_RSQ,
    get_comp_path,
)
from asset_pricing.plot_style import (
    COLOR_REF_LINE,
    plot_model_bars,
    save_figure,
    set_academic_style,
    style_axes,
)


def _plot_bar(df: pd.DataFrame, value_col: str, y_label: str, save_path) -> None:
    df = df.assign(Model=df["Model"].str.upper())
    plot_model_bars(df, "industry", value_col, y_label, save_path)


def plot_rmse_bar(df: pd.DataFrame) -> None:
    _plot_bar(df, "RMSE", "Root Mean Squared Error (RMSE, %)", FIG_PRED_RMSE)


def plot_r2_bar(df: pd.DataFrame) -> None:
    _plot_bar(df, "R2", "Out-of-Sample $R^2$", FIG_PRED_RSQ)


def _scatter_actual_vs_pred(ax, df: pd.DataFrame, title: str, size: float) -> None:
    """Predicted against actual returns with the 45-degree line."""
    mask = df["Actual"].notna() & df["Expected"].notna()
    ax.scatter(
        df.loc[mask, "Actual"],
        df.loc[mask, "Expected"],
        s=size,
        alpha=0.45,
        color="#2563EB",
        edgecolors="none",
    )
    mn = min(df["Actual"].min(), df["Expected"].min())
    mx = max(df["Actual"].max(), df["Expected"].max())
    ax.plot(
        [mn, mx],
        [mn, mx],
        color=COLOR_REF_LINE,
        linestyle="--",
        linewidth=1.1,
        alpha=0.85,
    )
    ax.set_title(title, pad=6)
    ax.set_xlabel("Actual Return (%)")
    ax.set_ylabel("Predicted Return (%)")
    style_axes(ax, both=True)


def plot_actual_vs_pred(data: dict, model: str) -> None:
    set_academic_style()
    inds = sorted(data.keys())
    fig, axes = plt.subplots(3, 4, figsize=(15, 11), sharex=True, sharey=True)
    axes_flat = axes.flatten()

    for ax, ind in zip(axes_flat, inds, strict=False):
        _scatter_actual_vs_pred(ax, data[ind], ind, size=12)

    for ax in axes_flat[len(inds) :]:
        fig.delaxes(ax)

    save_figure(fig, get_comp_path(model))


def plot_comp_three(
    data: dict, industries: tuple[str, ...] = ("Manuf", "Utils")
) -> None:
    set_academic_style()
    fig, axes = plt.subplots(
        1,
        len(industries),
        figsize=(5.5 * len(industries), 4.5),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for ax, ind in zip(axes.flatten(), industries, strict=True):
        _scatter_actual_vs_pred(ax, data[ind], ind, size=14)

    save_figure(fig, FIG_PRED_COMPEXAM)
