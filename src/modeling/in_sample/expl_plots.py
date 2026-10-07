import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

try:
    from src.modeling.in_sample.expl_config import get_coeffsbydecs_path
    from src.modeling.in_sample.expl_utils import (
        load_industry_data,
        get_industry_names,
        get_models,
        load_factors,
    )
except ModuleNotFoundError:
    try:
        from modeling.in_sample.expl_config import get_coeffsbydecs_path
        from modeling.in_sample.expl_utils import (
            load_industry_data,
            get_industry_names,
            get_models,
            load_factors,
        )
    except ModuleNotFoundError:
        from expl_config import get_coeffsbydecs_path
        from expl_utils import (
            load_industry_data,
            get_industry_names,
            get_models,
            load_factors,
        )


plt.style.use("default")


def plot_rsq(model_results, save_path=None):
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
    fig_width = max(12, count * 1.5)
    fig, ax = plt.subplots(figsize=(fig_width, 8))
    sns.barplot(x="Industry", y="Adjusted R-squared", hue="Model", data=df, ax=ax)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", fontsize=9, padding=3) # type: ignore
    ax.set_xlabel("Industry")
    ax.set_ylabel("Adjusted R-squared")
    many = count > 6
    plt.xticks(rotation=45 if many else 0, ha="right" if many else "center")
    ax.legend(title="Model", loc="best")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_industry_distributions(save_path=None):
    industry_data = load_industry_data()
    industry_names = get_industry_names(industry_data)
    rows, cols = 3, 4
    fig = plt.figure(figsize=(20, 15))
    for i, industry in enumerate(industry_names):
        if i < rows * cols:
            ax = fig.add_subplot(rows, cols, i + 1)
            data_to_plot = industry_data[industry].dropna()
            if isinstance(data_to_plot, pd.Series) and not data_to_plot.empty:
                sns.histplot(
                    x=data_to_plot,
                    kde=True,
                    stat="density",
                    color="steelblue",
                    ax=ax,
                )
            mean = industry_data[industry].mean()
            ax.axvline(
                x=mean,
                color="red",
                linestyle="--",
                alpha=0.7,
                label=f"Mean: {mean:.2f}%",
            )
            ax.axvline(x=0, color="black", linestyle="-", alpha=0.3)
            std = industry_data[industry].std()
            skew = industry_data[industry].skew()
            kurt = industry_data[industry].kurtosis()
            stats = f"Mean: {mean:.2f}%\nStd: {std:.2f}%\nSkew: {skew:.2f}\nKurt: {kurt:.2f}"
            ax.text(
                0.95,
                0.95,
                stats,
                transform=ax.transAxes,
                va="top",
                ha="right",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
            )
            ax.set_title(industry)
            ax.set_xlabel("Return (%)")
            ax.set_ylabel("Density")
            ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_decade_rsquared_grid(
    all_decade_stats, decades_order, save_outputs=True, save_path=None
):
    industries = set()
    for stats in all_decade_stats.values():
        for df in stats.values():
            industries.update(df["Industry"].tolist())
    industries.discard("Average")
    industries = sorted(industries)

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

    n = len(industries)
    rows = (n + 3) // 4
    cols = min(4, n)
    fig = plt.figure(figsize=(20, 5 * rows))

    for i, industry in enumerate(industries):
        ax = fig.add_subplot(rows, cols, i + 1)
        sub = df[df["Industry"] == industry]
        if not sub.empty:
            sns.lineplot(
                data=sub,
                x="Decade",
                y="Adj_R_squared",
                hue="Model",
                marker="o",
                ax=ax,
            )
            ax.set_xticks(range(len(decades_order)))
            ax.set_xticklabels(decades_order, rotation=45, ha="right")
            ax.set_title(industry)
            ax.set_ylabel("Adjusted R-squared")
            ax.set_ylim(0, 1)
            ax.grid(True, alpha=0.3)
            ax.legend(title="Model")

    plt.tight_layout()
    if save_outputs and save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_decade_model_factor_grids(
    all_decade_results,
    decades_order,
    save_outputs=True,
):
    models = get_models()
    factor_order = ["MKT", "SMB", "HML", "RMW", "CMA"]
    first_decade = next(iter(all_decade_results))
    first_model = next(iter(models))
    industries = sorted(all_decade_results[first_decade][first_model].keys())

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
        fig = plt.figure(figsize=(20, 5 * rows))

        for i, industry in enumerate(industries):
            ax = fig.add_subplot(rows, cols, i + 1)
            sub = df[df["Industry"] == industry]
            if not sub.empty:
                sns.lineplot(
                    data=sub,
                    x="Decade",
                    y="Coefficient",
                    hue="Factor",
                    marker="o",
                    ax=ax,
                    hue_order=[f for f in factor_order if f in factors],
                )
                ax.set_xticks(range(len(decades_order)))
                ax.set_xticklabels(decades_order, rotation=45, ha="right")
                ax.set_title(industry)
                ax.set_ylabel("Factor coefficient")
                ax.axhline(y=0, color="black", linestyle="-", alpha=0.3)
                ax.grid(True, alpha=0.3)
                ax.legend(title="Factor")

        plt.tight_layout()
        if save_outputs:
            path = get_coeffsbydecs_path(model)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            plt.savefig(path, bbox_inches="tight")
        plt.close(fig)


def plot_decade_model_alpha_grids(
    all_decade_results,
    decades_order,
    save_outputs=True,
    save_path=None,
):
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
    fig = plt.figure(figsize=(20, 5 * rows))
    for i, industry in enumerate(industries):
        ax = fig.add_subplot(rows, cols, i + 1)
        sub = df[df["Industry"] == industry]
        if not sub.empty:
            sns.lineplot(
                data=sub,
                x="Decade",
                y="Alpha",
                hue="Model",
                marker="o",
                ax=ax,
            )
            ax.set_xticks(range(len(decades_order)))
            ax.set_xticklabels(decades_order, rotation=45, ha="right")
            ax.set_title(industry)
            ax.set_ylabel("Alpha")
            ax.axhline(y=0, color="black", linestyle="-", alpha=0.3)
            ax.grid(True, alpha=0.3)
            ax.legend(title="Model")
    plt.tight_layout()
    if save_outputs and save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_factor_distributions(save_path=None):
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
    fig = plt.figure(figsize=(20, 5 * rows))
    for i, factor in enumerate(df.columns):
        ax = fig.add_subplot(rows, cols, i + 1)
        data_to_plot = df[factor].dropna()
        if isinstance(data_to_plot, pd.Series) and not data_to_plot.empty:
            sns.histplot(
                x=data_to_plot,
                kde=True,
                stat="density",
                color="steelblue",
                ax=ax,
            )
        mean = df[factor].mean()
        ax.axvline(
            x=mean, color="red", linestyle="--", alpha=0.7, label=f"Mean: {mean:.2f}%"
        )
        ax.axvline(x=0, color="black", linestyle="-", alpha=0.3)
        stats = (
            f"Mean: {mean:.2f}%\n"
            f"Std: {df[factor].std():.2f}%\n"
            f"Skew: {df[factor].skew():.2f}\n"
            f"Kurt: {df[factor].kurtosis():.2f}"
        )
        ax.text(
            0.95,
            0.95,
            stats,
            transform=ax.transAxes,
            va="top",
            ha="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
        )
        ax.set_title(factor)
        ax.set_xlabel("Return (%)")
        ax.set_ylabel("Density")
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_residuals_fitted_grid(reg_results, save_path=None, rows=3, cols=4):
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]
    for ax, industry in zip(axes_flat, reg_results.keys()):
        res = reg_results[industry]["residuals"]
        fit = reg_results[industry]["fitted"]
        ax.scatter(fit, res, alpha=0.5)
        ax.axhline(0, color="black", linestyle="--", alpha=0.7)
        ax.set_title(industry)
        ax.set_xlabel("Fitted values")
        ax.set_ylabel("Residuals")
    for ax in axes_flat[len(reg_results) :]:
        fig.delaxes(ax)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_cumulative_log_factor_returns(save_path=None):
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

    fig, ax = plt.subplots(figsize=(12, 6))
    if isinstance(
        log_cum, pd.DataFrame
    ): 
        palette = sns.color_palette("tab10", n_colors=log_cum.shape[1])
        log_cum.plot(ax=ax, color=palette)
    ax.set_xlabel("Date")
    ax.set_ylabel("Log cumulative return")
    ax.grid(True, alpha=0.3)
    if save_path:
        fig.tight_layout()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_cumulative_log_industry_returns(save_path=None):
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

    fig, ax = plt.subplots(figsize=(12, 6))
    if isinstance(
        log_cum, pd.DataFrame
    ):  
        palette = sns.color_palette("tab20", n_colors=log_cum.shape[1])
        log_cum.plot(ax=ax, color=palette)
    ax.set_xlabel("Date")
    ax.set_ylabel("Log cumulative return")
    ax.grid(True, alpha=0.3)
    if save_path:
        fig.tight_layout()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
