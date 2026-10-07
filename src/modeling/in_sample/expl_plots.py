from __future__ import annotations

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from src.modeling.in_sample.expl_config import get_coeffsbydecs_path
from src.modeling.in_sample.expl_utils import (
    load_industry_data,
    get_industry_names,
    get_models,
    load_factors,
)
from src.plot_style import (
    set_academic_style,
    MODEL_PALETTE,
    FACTOR_PALETTE,
    INDUSTRY_PALETTE,
    COLOR_ZERO_LINE,
    COLOR_REF_LINE,
    BOX_STYLE_STATS,
)


def plot_rsq(model_results: dict, save_path=None) -> None:
    set_academic_style()
    rows = []
    for model, industries in model_results.items():
        for industry, params in industries.items():
            rows.append(
                {
                    "Model": model.upper(),
                    "Industry": industry,
                    "Adjusted R-squared": params["adj_r_squared"],
                }
            )
    df = pd.DataFrame(rows)
    count = len(df["Industry"].unique())
    fig_width = max(11, count * 1.1)
    
    fig, ax = plt.subplots(figsize=(fig_width, 6))
    sns.barplot(
        x="Industry",
        y="Adjusted R-squared",
        hue="Model",
        data=df,
        palette=MODEL_PALETTE,
        ax=ax,
        edgecolor="none",
    )
    
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", fontsize=8.5, padding=2.5, color="#334155")  # type: ignore
        
    ax.set_xlabel("Industry Sector", labelpad=8)
    ax.set_ylabel("In-Sample Adjusted $R^2$", labelpad=8)
    ax.set_ylim(0, max(1.0, df["Adjusted R-squared"].max() + 0.12))
    
    many = count > 6
    plt.xticks(rotation=40 if many else 0, ha="right" if many else "center")
    
    ax.legend(
        title="Model",
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=len(df["Model"].unique()),
        frameon=False,
    )
    
    sns.despine(ax=ax, top=True, right=True)
    ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.6, alpha=0.8)
    ax.xaxis.grid(False)
    
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_industry_distributions(save_path=None) -> None:
    set_academic_style()
    industry_data = load_industry_data()
    industry_names = get_industry_names(industry_data)
    rows, cols = 3, 4
    fig = plt.figure(figsize=(16, 11))
    
    for i, industry in enumerate(industry_names):
        if i < rows * cols:
            ax = fig.add_subplot(rows, cols, i + 1)
            data_to_plot = industry_data[industry].dropna()
            if isinstance(data_to_plot, pd.Series) and not data_to_plot.empty:
                sns.histplot(
                    x=data_to_plot,
                    kde=True,
                    stat="density",
                    color="#2563EB",
                    alpha=0.35,
                    line_kws={"linewidth": 1.4, "color": "#1D4ED8"},
                    ax=ax,
                    edgecolor="none",
                )
            mean = industry_data[industry].mean()
            std = industry_data[industry].std()
            skew = industry_data[industry].skew()
            kurt = industry_data[industry].kurtosis()
            
            ax.axvline(
                x=mean,
                color=COLOR_REF_LINE,
                linestyle="--",
                linewidth=1.1,
                alpha=0.85,
            )
            ax.axvline(x=0, color=COLOR_ZERO_LINE, linestyle=":", linewidth=0.9, alpha=0.7)
            
            stats = f"μ:   {mean:5.2f}%\nσ:   {std:5.2f}%\nSkew:{skew:5.2f}\nKurt:{kurt:5.2f}"
            ax.text(
                0.95,
                0.94,
                stats,
                transform=ax.transAxes,
                va="top",
                ha="right",
                fontsize=7.5,
                family="monospace",
                bbox=BOX_STYLE_STATS,
            )
            ax.set_title(industry, pad=5)
            ax.set_xlabel("Monthly Return (%)")
            ax.set_ylabel("Density")
            
            sns.despine(ax=ax, top=True, right=True)
            ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.5, alpha=0.7)
            ax.xaxis.grid(False)

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_decade_rsquared_grid(
    all_decade_stats: dict,
    decades_order: list[str],
    save_outputs: bool = True,
    save_path=None,
) -> None:
    set_academic_style()
    industries = set()
    for stats in all_decade_stats.values():
        for df in stats.values():
            industries.update(df["Industry"].tolist())
    industries.discard("Average")
    sorted_industries = sorted(industries)

    data = []
    for decade, stats in all_decade_stats.items():
        for model, df_stats in stats.items():
            for _, row in df_stats.iterrows():
                if row["Industry"] != "Average":
                    data.append(
                        {
                            "Industry": row["Industry"],
                            "Decade": decade,
                            "Model": model.upper(),
                            "Adj_R_squared": row["Adj_R_squared"],
                        }
                    )
    df = pd.DataFrame(data)

    n = len(sorted_industries)
    rows = (n + 3) // 4
    cols = min(4, n)
    fig = plt.figure(figsize=(16, 3.8 * rows))

    model_markers = {"CAPM": "o", "FF3": "s", "FF5": "^"}

    for i, industry in enumerate(sorted_industries):
        ax = fig.add_subplot(rows, cols, i + 1)
        sub = df[df["Industry"] == industry]
        if not sub.empty:
            for model_name, sub_model in sub.groupby("Model"):
                ax.plot(
                    sub_model["Decade"],
                    sub_model["Adj_R_squared"],
                    marker=model_markers.get(str(model_name), "o"),
                    markersize=4.5,
                    linewidth=1.4,
                    color=MODEL_PALETTE.get(str(model_name), "#2563EB"),
                    label=str(model_name),
                )
            ax.set_xticks(range(len(decades_order)))
            ax.set_xticklabels(decades_order, rotation=40, ha="right")
            ax.set_title(industry, pad=5)
            ax.set_ylabel("Adjusted $R^2$")
            ax.set_ylim(0, 1.05)
            
            sns.despine(ax=ax, top=True, right=True)
            ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.5, alpha=0.7)
            ax.xaxis.grid(False)
            
            # Show legend only on first subplot to eliminate visual redundancy
            if i == 0:
                ax.legend(title="Model", frameon=False, fontsize=8)

    plt.tight_layout()
    if save_outputs and save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_decade_model_factor_grids(
    all_decade_results: dict,
    decades_order: list[str],
    save_outputs: bool = True,
) -> None:
    set_academic_style()
    models = get_models()
    factor_order = ["MKT", "SMB", "HML", "RMW", "CMA"]
    first_decade = next(iter(all_decade_results))
    first_model = next(iter(models))
    industries = sorted(all_decade_results[first_decade][first_model].keys())

    factor_markers = {"MKT": "o", "SMB": "s", "HML": "^", "RMW": "D", "CMA": "v"}

    for model, info in models.items():
        factors = info["factors"]
        data = []
        for decade, results in all_decade_results.items():
            if model in results:
                for industry, params in results[model].items():
                    for factor in factors:
                        if factor in params["betas"]:
                            data.append(
                                {
                                    "Industry": industry,
                                    "Decade": decade,
                                    "Factor": factor,
                                    "Coefficient": params["betas"][factor],
                                }
                            )
        df = pd.DataFrame(data)
        if df.empty:
            continue

        n = len(industries)
        rows = (n + 3) // 4
        cols = min(4, n)
        fig = plt.figure(figsize=(16, 3.8 * rows))

        for i, industry in enumerate(industries):
            ax = fig.add_subplot(rows, cols, i + 1)
            sub = df[df["Industry"] == industry]
            if not sub.empty:
                for factor_name in [f for f in factor_order if f in factors]:
                    sub_f = sub[sub["Factor"] == factor_name]
                    if not sub_f.empty:
                        ax.plot(
                            sub_f["Decade"],
                            sub_f["Coefficient"],
                            marker=factor_markers.get(factor_name, "o"),
                            markersize=4.5,
                            linewidth=1.4,
                            color=FACTOR_PALETTE.get(factor_name, "#2563EB"),
                            label=factor_name,
                        )
                ax.set_xticks(range(len(decades_order)))
                ax.set_xticklabels(decades_order, rotation=40, ha="right")
                ax.set_title(industry, pad=5)
                ax.set_ylabel("Factor Sensitivity (Beta)")
                ax.axhline(y=0, color=COLOR_ZERO_LINE, linestyle=":", linewidth=0.9, alpha=0.7)
                
                sns.despine(ax=ax, top=True, right=True)
                ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.5, alpha=0.7)
                ax.xaxis.grid(False)
                
                if i == 0:
                    ax.legend(title="Factor", frameon=False, fontsize=8)

        plt.tight_layout()
        if save_outputs:
            path = get_coeffsbydecs_path(model)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            plt.savefig(path, bbox_inches="tight")
        plt.close(fig)


def plot_decade_model_alpha_grids(
    all_decade_results: dict,
    decades_order: list[str],
    save_outputs: bool = True,
    save_path=None,
) -> None:
    set_academic_style()
    data = []
    for decade, results in all_decade_results.items():
        for model, industries in results.items():
            for industry, params in industries.items():
                data.append(
                    {
                        "Industry": industry,
                        "Decade": decade,
                        "Model": model.upper(),
                        "Alpha": params.get("alpha"),
                    }
                )
    df = pd.DataFrame(data)
    industries = sorted(df["Industry"].unique())
    rows = (len(industries) + 3) // 4
    cols = min(4, len(industries))
    fig = plt.figure(figsize=(16, 3.8 * rows))
    
    model_markers = {"CAPM": "o", "FF3": "s", "FF5": "^"}

    for i, industry in enumerate(industries):
        ax = fig.add_subplot(rows, cols, i + 1)
        sub = df[df["Industry"] == industry]
        if not sub.empty:
            for model_name, sub_model in sub.groupby("Model"):
                ax.plot(
                    sub_model["Decade"],
                    sub_model["Alpha"],
                    marker=model_markers.get(str(model_name), "o"),
                    markersize=4.5,
                    linewidth=1.4,
                    color=MODEL_PALETTE.get(str(model_name), "#2563EB"),
                    label=str(model_name),
                )
            ax.set_xticks(range(len(decades_order)))
            ax.set_xticklabels(decades_order, rotation=40, ha="right")
            ax.set_title(industry, pad=5)
            ax.set_ylabel("Alpha (%)")
            ax.axhline(y=0, color=COLOR_ZERO_LINE, linestyle=":", linewidth=0.9, alpha=0.7)
            
            sns.despine(ax=ax, top=True, right=True)
            ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.5, alpha=0.7)
            ax.xaxis.grid(False)
            
            if i == 0:
                ax.legend(title="Model", frameon=False, fontsize=8)

    plt.tight_layout()
    if save_outputs and save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_factor_distributions(save_path=None) -> None:
    set_academic_style()
    models = get_models()
    all_factors = {}
    for model, info in models.items():
        data = load_factors(model)
        for factor in info["factors"]:
            if factor == "SMB":
                label = f"SMB ({model.upper()})"
            else:
                label = factor
            all_factors[label] = data[factor]
    df = pd.DataFrame(all_factors)

    num = len(df.columns)
    rows = (num + 3) // 4
    cols = min(4, num)
    fig = plt.figure(figsize=(16, 3.8 * rows))
    
    for i, factor in enumerate(df.columns):
        ax = fig.add_subplot(rows, cols, i + 1)
        data_to_plot = df[factor].dropna()
        if isinstance(data_to_plot, pd.Series) and not data_to_plot.empty:
            sns.histplot(
                x=data_to_plot,
                kde=True,
                stat="density",
                color="#0D9488",
                alpha=0.35,
                line_kws={"linewidth": 1.4, "color": "#0F766E"},
                ax=ax,
                edgecolor="none",
            )
        mean = df[factor].mean()
        std = df[factor].std()
        skew = df[factor].skew()
        kurt = df[factor].kurtosis()
        
        ax.axvline(
            x=mean,
            color=COLOR_REF_LINE,
            linestyle="--",
            linewidth=1.1,
            alpha=0.85,
        )
        ax.axvline(x=0, color=COLOR_ZERO_LINE, linestyle=":", linewidth=0.9, alpha=0.7)
        
        stats = f"μ:   {mean:5.2f}%\nσ:   {std:5.2f}%\nSkew:{skew:5.2f}\nKurt:{kurt:5.2f}"
        ax.text(
            0.95,
            0.94,
            stats,
            transform=ax.transAxes,
            va="top",
            ha="right",
            fontsize=7.5,
            family="monospace",
            bbox=BOX_STYLE_STATS,
        )
        ax.set_title(factor, pad=5)
        ax.set_xlabel("Factor Return (%)")
        ax.set_ylabel("Density")
        
        sns.despine(ax=ax, top=True, right=True)
        ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.5, alpha=0.7)
        ax.xaxis.grid(False)

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_residuals_fitted_grid(reg_results: dict, save_path=None, rows: int = 3, cols: int = 4) -> None:
    set_academic_style()
    fig, axes = plt.subplots(rows, cols, figsize=(15, 3.5 * rows))
    axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]
    
    for ax, industry in zip(axes_flat, reg_results.keys()):
        res = reg_results[industry]["residuals"]
        fit = reg_results[industry]["fitted"]
        ax.scatter(fit, res, alpha=0.45, s=12, color="#2563EB", edgecolors="none")
        ax.axhline(0, color=COLOR_REF_LINE, linestyle="--", linewidth=1.1, alpha=0.85)
        ax.set_title(industry, pad=5)
        ax.set_xlabel("Fitted Values (%)")
        ax.set_ylabel("Residuals (%)")
        
        sns.despine(ax=ax, top=True, right=True)
        ax.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.5, alpha=0.7)

    for ax in axes_flat[len(reg_results):]:
        fig.delaxes(ax)

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_cumulative_log_factor_returns(save_path=None) -> None:
    set_academic_style()
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
    df_factors = df_factors / 100.0
    log_cum = np.log1p(df_factors).cumsum()
    if not isinstance(log_cum, pd.DataFrame):
        log_cum = pd.DataFrame(log_cum)

    if not log_cum.empty:
        log_cum = log_cum - log_cum.iloc[0]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    if isinstance(log_cum, pd.DataFrame):
        for col in log_cum.columns:
            color = FACTOR_PALETTE.get(col, "#2563EB")
            ax.plot(log_cum.index, log_cum[col], label=col, color=color, linewidth=1.6)

    ax.set_xlabel("Date", labelpad=8)
    ax.set_ylabel("Cumulative Log Return", labelpad=8)
    ax.axhline(0, color=COLOR_ZERO_LINE, linestyle=":", linewidth=0.9, alpha=0.7)
    
    ax.legend(
        loc="upper left",
        ncol=3,
        frameon=False,
        fontsize=8.5,
    )
    
    sns.despine(ax=ax, top=True, right=True)
    ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.6, alpha=0.8)
    ax.xaxis.grid(False)

    if save_path:
        fig.tight_layout()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_cumulative_log_industry_returns(save_path=None) -> None:
    set_academic_style()
    industry_data = load_industry_data()
    industry_names = get_industry_names(industry_data)
    df_industry = industry_data[industry_names] / 100.0

    log_cum_intermediate = np.log1p(df_industry).cumsum()

    if isinstance(log_cum_intermediate, pd.Series):
        log_cum = pd.DataFrame(log_cum_intermediate)
    elif isinstance(log_cum_intermediate, pd.DataFrame):
        log_cum = log_cum_intermediate
    else:
        if isinstance(df_industry, pd.DataFrame):
            log_cum = pd.DataFrame(
                log_cum_intermediate,
                index=df_industry.index,
                columns=df_industry.columns,
            )
        elif isinstance(df_industry, pd.Series):
            col_name = df_industry.name if df_industry.name is not None else 0
            log_cum = pd.DataFrame(
                log_cum_intermediate, index=df_industry.index, columns=[col_name]
            )
        else:
            log_cum = pd.DataFrame(log_cum_intermediate)

    if not log_cum.empty:
        log_cum = log_cum - log_cum.iloc[0]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    if isinstance(log_cum, pd.DataFrame):
        for idx, col in enumerate(log_cum.columns):
            color = INDUSTRY_PALETTE[idx % len(INDUSTRY_PALETTE)]
            ax.plot(log_cum.index, log_cum[col], label=col, color=color, linewidth=1.4)

    ax.set_xlabel("Date", labelpad=8)
    ax.set_ylabel("Cumulative Log Return", labelpad=8)
    ax.axhline(0, color=COLOR_ZERO_LINE, linestyle=":", linewidth=0.9, alpha=0.7)
    
    ax.legend(
        loc="upper left",
        ncol=4,
        frameon=False,
        fontsize=8,
    )
    
    sns.despine(ax=ax, top=True, right=True)
    ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.6, alpha=0.8)
    ax.xaxis.grid(False)

    if save_path:
        fig.tight_layout()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
