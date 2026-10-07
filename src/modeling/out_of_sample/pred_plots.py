import matplotlib.pyplot as plt
import seaborn as sns
try:
    from src.modeling.out_of_sample.pred_config import RSQ, RMSE, get_comp_path, COMPEXAM
except ModuleNotFoundError:
    try:
        from modeling.out_of_sample.pred_config import RSQ, RMSE, get_comp_path, COMPEXAM
    except ModuleNotFoundError:
        from pred_config import RSQ, RMSE, get_comp_path, COMPEXAM



def _plot_bar(df, value_col, y_label, save_path):
    if all(col in df.columns for col in ["Model", value_col]):
        df_long = df.copy()
    else:
        df_long = df.melt(id_vars="industry", var_name="Model", value_name=value_col)
    df_long["Model"] = df_long["Model"].str.upper()
    count = df_long["industry"].nunique()
    fig, ax = plt.subplots(figsize=(max(12, count * 1.5), 8))
    sns.barplot(x="industry", y=value_col, hue="Model", data=df_long, ax=ax)
    for c in ax.containers:
        ax.bar_label(c, fmt="%.2f", fontsize=9, padding=3) # type: ignore
    ax.set(xlabel="Industry", ylabel=y_label)
    plt.xticks(rotation=45 if count > 6 else 0, ha="right" if count > 6 else "center")
    ax.legend(title="Model")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_rmse_bar(df):
    _plot_bar(df, "RMSE", "Root mean squared error", RMSE)


def plot_r2_bar(df):
    _plot_bar(df, "R2", "Out-of-sample R2", RSQ)


def plot_actual_vs_pred(data, model):
    save_path = get_comp_path(model)
    inds = sorted(data)
    fig, axes = plt.subplots(3, 4, figsize=(16, 12), sharex=True, sharey=True)
    axes = axes.flatten()
    for ax, ind in zip(axes, inds):
        df = data[ind]
        mask = df["Actual"].notna() & df["Expected"].notna()
        ax.scatter(df.loc[mask, "Actual"], df.loc[mask, "Expected"], s=10, alpha=0.6)
        mn = min(df["Actual"].min(), df["Expected"].min())
        mx = max(df["Actual"].max(), df["Expected"].max())
        ax.plot([mn, mx], [mn, mx], "r--")
        ax.set(title=ind, xlabel="Actual (%)", ylabel="Predicted (%)")
    for ax in axes[len(inds) :]:
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_comp_three(data, model, industries=["Manuf", "Utils"]):
    save_path = COMPEXAM
    fig, axes = plt.subplots(
        1, len(industries), figsize=(10, 5), sharex=True, sharey=True
    )
    for ax, ind in zip(axes, industries):
        df = data.get(ind)
        mask = df["Actual"].notna() & df["Expected"].notna()
        ax.scatter(df.loc[mask, "Actual"], df.loc[mask, "Expected"], s=10, alpha=0.6)
        mn = min(df["Actual"].min(), df["Expected"].min())
        mx = max(df["Actual"].max(), df["Expected"].max())
        ax.plot([mn, mx], [mn, mx], "r--")
        ax.set(title=ind, xlabel="Actual (%)", ylabel="Predicted (%)")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
