"""Figures of the in-sample stage."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from asset_pricing.config import FIG_BETAS_BY_DECADE, MODELS
from asset_pricing.data.loaders import (
    get_industry_names,
    load_factors,
    load_industry_data,
)
from asset_pricing.plot_style import (
    BOX_STYLE_STATS,
    COLOR_REF_LINE,
    COLOR_ZERO_LINE,
    FACTOR_PALETTE,
    INDUSTRY_PALETTE,
    MODEL_PALETTE,
    plot_model_bars,
    save_figure,
    set_academic_style,
    style_axes,
)

# Series drawn in the decade grids, in plotting order, with their markers.
MODEL_MARKERS = {"CAPM": "o", "FF3": "s", "FF5": "^"}
FACTOR_MARKERS = {"MKT": "o", "SMB": "s", "HML": "^", "RMW": "D", "CMA": "v"}


def _zero_line(ax) -> None:
    ax.axhline(0, color=COLOR_ZERO_LINE, linestyle=":", linewidth=0.9, alpha=0.7)


def plot_adj_r2(model_results: dict, save_path=None) -> None:
    df = pd.DataFrame(
        [
            {
                "Model": model.upper(),
                "Industry": industry,
                "Adjusted R-squared": params["adj_r_squared"],
            }
            for model, industries in model_results.items()
            for industry, params in industries.items()
        ]
    )
    plot_model_bars(
        df,
        "Industry",
        "Adjusted R-squared",
        "In-Sample Adjusted $R^2$",
        save_path,
        ylim=(0, max(1.0, df["Adjusted R-squared"].max() + 0.12)),
    )


def _plot_distribution_grid(
    df, color, line_color, x_label, save_path, fig_height=None
) -> None:
    """One histogram with density curve and summary statistics per column."""
    set_academic_style()
    rows = (len(df.columns) + 3) // 4
    cols = min(4, len(df.columns))
    fig = plt.figure(figsize=(16, fig_height or 3.8 * rows))

    for i, name in enumerate(df.columns):
        ax = fig.add_subplot(rows, cols, i + 1)
        series = df[name]
        sns.histplot(
            x=series.dropna(),
            kde=True,
            stat="density",
            color=color,
            alpha=0.35,
            line_kws={"linewidth": 1.4, "color": line_color},
            ax=ax,
            edgecolor="none",
        )
        mean = series.mean()
        ax.axvline(
            x=mean, color=COLOR_REF_LINE, linestyle="--", linewidth=1.1, alpha=0.85
        )
        ax.axvline(x=0, color=COLOR_ZERO_LINE, linestyle=":", linewidth=0.9, alpha=0.7)
        ax.text(
            0.95,
            0.94,
            f"μ:   {mean:5.2f}%\nσ:   {series.std():5.2f}%\n"
            f"Skew:{series.skew():5.2f}\nKurt:{series.kurtosis():5.2f}",
            transform=ax.transAxes,
            va="top",
            ha="right",
            fontsize=7.5,
            family="monospace",
            bbox=BOX_STYLE_STATS,
        )
        ax.set_title(name, pad=5)
        ax.set_xlabel(x_label)
        ax.set_ylabel("Density")
        style_axes(ax)

    save_figure(fig, save_path)


def plot_industry_distributions(save_path=None) -> None:
    industry_data = load_industry_data()
    _plot_distribution_grid(
        industry_data[get_industry_names(industry_data)],
        color="#2563EB",
        line_color="#1D4ED8",
        x_label="Monthly Return (%)",
        save_path=save_path,
        fig_height=11,
    )


def plot_factor_distributions(save_path=None) -> None:
    all_factors = {}
    for model, info in MODELS.items():
        data = load_factors(model)
        for factor in info["factors"]:
            label = f"SMB ({model.upper()})" if factor == "SMB" else factor
            all_factors[label] = data[factor]
    _plot_distribution_grid(
        pd.DataFrame(all_factors),
        color="#0D9488",
        line_color="#0F766E",
        x_label="Factor Return (%)",
        save_path=save_path,
    )


def _plot_decade_grid(
    df,
    decades_order,
    series_col,
    value_col,
    markers,
    palette,
    y_label,
    save_path,
    zero_line=True,
    ylim=None,
) -> None:
    """One panel per industry with a line over the decades for each series.

    `df` is in long format with the columns "Industry", "Decade", `series_col`
    and `value_col`. `markers` names the series and fixes their drawing order.
    """
    set_academic_style()
    industries = sorted(df["Industry"].unique())
    rows = (len(industries) + 3) // 4
    cols = min(4, len(industries))
    fig = plt.figure(figsize=(16, 3.8 * rows))

    for i, industry in enumerate(industries):
        ax = fig.add_subplot(rows, cols, i + 1)
        sub = df[df["Industry"] == industry]
        for name, marker in markers.items():
            sub_series = sub[sub[series_col] == name]
            if not sub_series.empty:
                ax.plot(
                    sub_series["Decade"],
                    sub_series[value_col],
                    marker=marker,
                    markersize=4.5,
                    linewidth=1.4,
                    color=palette[name],
                    label=name,
                )
        ax.set_xticks(range(len(decades_order)))
        ax.set_xticklabels(decades_order, rotation=40, ha="right")
        ax.set_title(industry, pad=5)
        ax.set_ylabel(y_label)
        if ylim:
            ax.set_ylim(*ylim)
        if zero_line:
            _zero_line(ax)
        style_axes(ax)

        # Show legend only on first subplot to eliminate visual redundancy
        if i == 0:
            ax.legend(title=series_col, frameon=False, fontsize=8)

    save_figure(fig, save_path)


def plot_decade_rsquared_grid(
    all_decade_stats: dict, decades_order: list[str], save_path=None
) -> None:
    df = pd.concat(
        [
            df_stats[["Industry", "Adj_R_squared"]].assign(
                Decade=decade, Model=model.upper()
            )
            for decade, stats in all_decade_stats.items()
            for model, df_stats in stats.items()
        ],
        ignore_index=True,
    )
    _plot_decade_grid(
        df,
        decades_order,
        "Model",
        "Adj_R_squared",
        MODEL_MARKERS,
        MODEL_PALETTE,
        "Adjusted $R^2$",
        save_path,
        zero_line=False,
        ylim=(0, 1.05),
    )


def plot_decade_model_factor_grids(
    all_decade_results: dict, decades_order: list[str]
) -> None:
    for model in MODELS:
        df = pd.DataFrame(
            [
                {
                    "Industry": industry,
                    "Decade": decade,
                    "Factor": factor,
                    "Coefficient": coefficient,
                }
                for decade, results in all_decade_results.items()
                for industry, params in results[model].items()
                for factor, coefficient in params["betas"].items()
            ]
        )
        _plot_decade_grid(
            df,
            decades_order,
            "Factor",
            "Coefficient",
            FACTOR_MARKERS,
            FACTOR_PALETTE,
            "Factor Sensitivity (Beta)",
            FIG_BETAS_BY_DECADE[model],
        )


def plot_decade_model_alpha_grids(
    all_decade_results: dict, decades_order: list[str], save_path=None
) -> None:
    df = pd.DataFrame(
        [
            {
                "Industry": industry,
                "Decade": decade,
                "Model": model.upper(),
                "Alpha": params["alpha"],
            }
            for decade, results in all_decade_results.items()
            for model, industries in results.items()
            for industry, params in industries.items()
        ]
    )
    _plot_decade_grid(
        df,
        decades_order,
        "Model",
        "Alpha",
        MODEL_MARKERS,
        MODEL_PALETTE,
        "Alpha (%)",
        save_path,
    )


def plot_residuals_fitted_grid(
    reg_results: dict, save_path=None, rows: int = 3, cols: int = 4
) -> None:
    set_academic_style()
    fig, axes = plt.subplots(rows, cols, figsize=(15, 3.5 * rows))
    axes_flat = axes.flatten()

    for ax, (industry, params) in zip(axes_flat, reg_results.items(), strict=False):
        ax.scatter(
            params["fitted"],
            params["residuals"],
            alpha=0.45,
            s=12,
            color="#2563EB",
            edgecolors="none",
        )
        ax.axhline(0, color=COLOR_REF_LINE, linestyle="--", linewidth=1.1, alpha=0.85)
        ax.set_title(industry, pad=5)
        ax.set_xlabel("Fitted Values (%)")
        ax.set_ylabel("Residuals (%)")
        style_axes(ax, both=True)

    for ax in axes_flat[len(reg_results) :]:
        fig.delaxes(ax)

    save_figure(fig, save_path)


def _plot_cumulative_log_returns(
    returns_pct, colors, linewidth, legend_ncol, legend_fontsize, save_path
) -> None:
    """Cumulative log return of each column, starting at zero."""
    set_academic_style()
    log_cum = np.log1p(returns_pct / 100.0).cumsum()
    log_cum = log_cum - log_cum.iloc[0]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    for col, color in zip(log_cum.columns, colors, strict=True):
        ax.plot(
            log_cum.index, log_cum[col], label=col, color=color, linewidth=linewidth
        )

    ax.set_xlabel("Date", labelpad=8)
    ax.set_ylabel("Cumulative Log Return", labelpad=8)
    _zero_line(ax)
    ax.legend(
        loc="upper left", ncol=legend_ncol, frameon=False, fontsize=legend_fontsize
    )
    style_axes(ax, grid_width=0.6, grid_alpha=0.8)
    save_figure(fig, save_path)


def plot_cumulative_log_factor_returns(save_path=None) -> None:
    data3 = load_factors("ff3")
    data5 = load_factors("ff5")
    df_factors = pd.DataFrame(
        {
            "MKT": data5["MKT"],
            "SMB (FF3)": data3["SMB"],
            "SMB (FF5)": data5["SMB"],
            "HML": data5["HML"],
            "RMW": data5["RMW"],
            "CMA": data5["CMA"],
        }
    )
    _plot_cumulative_log_returns(
        df_factors,
        colors=[FACTOR_PALETTE[col] for col in df_factors.columns],
        linewidth=1.6,
        legend_ncol=3,
        legend_fontsize=8.5,
        save_path=save_path,
    )


def plot_cumulative_log_industry_returns(save_path=None) -> None:
    industry_data = load_industry_data()
    industry_names = get_industry_names(industry_data)
    _plot_cumulative_log_returns(
        industry_data[industry_names],
        colors=INDUSTRY_PALETTE[: len(industry_names)],
        linewidth=1.4,
        legend_ncol=4,
        legend_fontsize=8,
        save_path=save_path,
    )
