from __future__ import annotations

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

try:
    from src.modeling.out_of_sample.pred_config import RSQ, RMSE, get_comp_path, COMPEXAM
except ModuleNotFoundError:
    try:
        from modeling.out_of_sample.pred_config import RSQ, RMSE, get_comp_path, COMPEXAM
    except ModuleNotFoundError:
        from pred_config import RSQ, RMSE, get_comp_path, COMPEXAM

try:
    from src.plot_style import (
        set_academic_style,
        MODEL_PALETTE,
        COLOR_REF_LINE,
    )
except ModuleNotFoundError:
    try:
        from plot_style import (
            set_academic_style,
            MODEL_PALETTE,
            COLOR_REF_LINE,
        )
    except ModuleNotFoundError:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).resolve().parents[2]))
        from src.plot_style import (
            set_academic_style,
            MODEL_PALETTE,
            COLOR_REF_LINE,
        )


def _plot_bar(df: pd.DataFrame, value_col: str, y_label: str, save_path) -> None:
    set_academic_style()
    if all(col in df.columns for col in ["Model", value_col]):
        df_long = df.copy()
    else:
        df_long = df.melt(id_vars="industry", var_name="Model", value_name=value_col)
    
    df_long["Model"] = df_long["Model"].str.upper()
    count = df_long["industry"].nunique()
    fig_width = max(11, count * 1.1)
    
    fig, ax = plt.subplots(figsize=(fig_width, 6))
    
    sns.barplot(
        x="industry",
        y=value_col,
        hue="Model",
        data=df_long,
        palette=MODEL_PALETTE,
        ax=ax,
        edgecolor="none",
    )
    
    for c in ax.containers:
        ax.bar_label(c, fmt="%.2f", fontsize=8.5, padding=2.5, color="#334155")  # type: ignore
        
    ax.set_xlabel("Industry Sector", labelpad=8)
    ax.set_ylabel(y_label, labelpad=8)
    
    many = count > 6
    plt.xticks(rotation=40 if many else 0, ha="right" if many else "center")
    
    # Clean top-center legend
    ax.legend(
        title="Model",
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=len(df_long["Model"].unique()),
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


def plot_rmse_bar(df: pd.DataFrame) -> None:
    _plot_bar(df, "RMSE", "Root Mean Squared Error (RMSE, %)", RMSE)


def plot_r2_bar(df: pd.DataFrame) -> None:
    _plot_bar(df, "R2", "Out-of-Sample $R^2$", RSQ)


def plot_actual_vs_pred(data: dict, model: str) -> None:
    set_academic_style()
    save_path = get_comp_path(model)
    inds = sorted(data.keys())
    
    rows, cols = 3, 4
    fig, axes = plt.subplots(rows, cols, figsize=(15, 11), sharex=True, sharey=True)
    axes_flat = axes.flatten()
    
    for ax, ind in zip(axes_flat, inds):
        df = data[ind]
        mask = df["Actual"].notna() & df["Expected"].notna()
        ax.scatter(
            df.loc[mask, "Actual"],
            df.loc[mask, "Expected"],
            s=12,
            alpha=0.45,
            color="#2563EB",
            edgecolors="none",
        )
        mn = min(df["Actual"].min(), df["Expected"].min())
        mx = max(df["Actual"].max(), df["Expected"].max())
        ax.plot([mn, mx], [mn, mx], color=COLOR_REF_LINE, linestyle="--", linewidth=1.1, alpha=0.85)
        ax.set_title(ind, pad=6)
        ax.set_xlabel("Actual Return (%)")
        ax.set_ylabel("Predicted Return (%)")
        
        sns.despine(ax=ax, top=True, right=True)
        ax.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.5, alpha=0.7)

    for ax in axes_flat[len(inds):]:
        fig.delaxes(ax)

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_comp_three(data: dict, model: str, industries: list[str] = ["Manuf", "Utils"]) -> None:
    set_academic_style()
    save_path = COMPEXAM
    fig, axes = plt.subplots(
        1, len(industries), figsize=(5.5 * len(industries), 4.5), sharex=True, sharey=True
    )
    if len(industries) == 1:
        axes = [axes]  # type: ignore
        
    for ax, ind in zip(axes, industries):
        df = data.get(ind)
        if df is None:
            continue
        mask = df["Actual"].notna() & df["Expected"].notna()
        ax.scatter(
            df.loc[mask, "Actual"],
            df.loc[mask, "Expected"],
            s=14,
            alpha=0.45,
            color="#2563EB",
            edgecolors="none",
        )
        mn = min(df["Actual"].min(), df["Expected"].min())
        mx = max(df["Actual"].max(), df["Expected"].max())
        ax.plot([mn, mx], [mn, mx], color=COLOR_REF_LINE, linestyle="--", linewidth=1.1, alpha=0.85)
        ax.set_title(ind, pad=6)
        ax.set_xlabel("Actual Return (%)")
        ax.set_ylabel("Predicted Return (%)")
        
        sns.despine(ax=ax, top=True, right=True)
        ax.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
