import os
from pathlib import Path

import matplotlib
import pandas as pd
import seaborn as sns

# Backend no interactivo para entornos sin UI.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def setup_style() -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["figure.dpi"] = 120


def save_dataframe_preview(df: pd.DataFrame, output_dir: Path) -> None:
    df.head(20).to_csv(output_dir / "preview_head20.csv", index=False)
    df.describe(include="all").transpose().to_csv(output_dir / "describe_all.csv")


def summarize_dataset(df: pd.DataFrame, output_dir: Path) -> None:
    n_rows, n_cols = df.shape
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    missing_pct = (df.isna().mean() * 100).sort_values(ascending=False)
    duplicates = int(df.duplicated().sum())

    summary_lines = [
        "=== EDA - PETFINDER TRAIN ===",
        f"Filas: {n_rows}",
        f"Columnas: {n_cols}",
        f"Columnas numericas: {len(numeric_cols)}",
        f"Columnas categoricas: {len(cat_cols)}",
        f"Filas duplicadas: {duplicates}",
        "",
        "Top 15 columnas con mayor porcentaje de nulos:",
    ]

    for col, pct in missing_pct.head(15).items():
        summary_lines.append(f"- {col}: {pct:.2f}%")

    (output_dir / "summary.txt").write_text("\n".join(summary_lines), encoding="utf-8")
    missing_pct.rename("missing_pct").to_csv(output_dir / "missingness.csv")

    print("\n".join(summary_lines))


def plot_missingness(df: pd.DataFrame, output_dir: Path) -> None:
    missing_pct = (df.isna().mean() * 100).sort_values(ascending=False)
    top_missing = missing_pct[missing_pct > 0].head(20)
    if top_missing.empty:
        return

    plt.figure(figsize=(11, 6))
    sns.barplot(x=top_missing.values, y=top_missing.index, color="#3B82F6")
    plt.title("Top columnas con valores faltantes")
    plt.xlabel("% de valores faltantes")
    plt.ylabel("Columnas")
    plt.tight_layout()
    plt.savefig(output_dir / "missingness_top20.png")
    plt.close()


def plot_target_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    target_col = "AdoptionSpeed"
    if target_col not in df.columns:
        return

    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x=target_col, color="#10B981")
    plt.title("Distribucion de AdoptionSpeed")
    plt.xlabel("AdoptionSpeed")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.savefig(output_dir / "target_distribution.png")
    plt.close()


def plot_numeric_distributions(df: pd.DataFrame, output_dir: Path) -> None:
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not numeric_cols:
        return

    preferred = ["Age", "Fee", "Quantity", "PhotoAmt", "VideoAmt", "MaturitySize"]
    selected = [col for col in preferred if col in numeric_cols]
    if len(selected) < 6:
        selected += [c for c in numeric_cols if c not in selected][: 6 - len(selected)]

    n = len(selected)
    if n == 0:
        return

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(14, 8))
    axes = axes.flatten()

    for i, col in enumerate(selected):
        sns.histplot(df[col], kde=True, ax=axes[i], color="#6366F1")
        axes[i].set_title(f"Distribucion: {col}")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frecuencia")

    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    plt.tight_layout()
    plt.savefig(output_dir / "numeric_distributions.png")
    plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, output_dir: Path) -> None:
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.shape[1] < 2:
        return

    corr = numeric_df.corr(numeric_only=True)
    if corr.empty:
        return

    if corr.shape[0] > 20:
        variances = numeric_df.var(numeric_only=True).sort_values(ascending=False)
        keep = variances.head(20).index
        corr = numeric_df[keep].corr(numeric_only=True)

    plt.figure(figsize=(12, 9))
    sns.heatmap(
        corr,
        cmap="coolwarm",
        center=0,
        square=False,
        cbar_kws={"shrink": 0.8},
    )
    plt.title("Matriz de correlacion (columnas numericas)")
    plt.tight_layout()
    plt.savefig(output_dir / "correlation_heatmap.png")
    plt.close()


def plot_target_vs_features(df: pd.DataFrame, output_dir: Path) -> None:
    target_col = "AdoptionSpeed"
    if target_col not in df.columns:
        return

    candidates = [c for c in ["Age", "Fee", "Quantity", "PhotoAmt"] if c in df.columns]
    if not candidates:
        return

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()

    for i, col in enumerate(candidates[:4]):
        sns.boxplot(data=df, x=target_col, y=col, ax=axes[i], color="#F59E0B")
        axes[i].set_title(f"{col} vs {target_col}")

    for j in range(len(candidates), 4):
        axes[j].axis("off")

    plt.tight_layout()
    plt.savefig(output_dir / "target_vs_numeric_boxplots.png")
    plt.close()


def plot_top_categories(df: pd.DataFrame, output_dir: Path) -> None:
    cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    if not cat_cols:
        return

    selected = cat_cols[:4]
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()

    for i, col in enumerate(selected):
        top_counts = df[col].astype("string").fillna("MISSING").value_counts().head(10)
        sns.barplot(
            x=top_counts.values,
            y=top_counts.index,
            ax=axes[i],
            color="#EC4899",
        )
        axes[i].set_title(f"Top categorias: {col}")
        axes[i].set_xlabel("Cantidad")
        axes[i].set_ylabel(col)

    for j in range(len(selected), 4):
        axes[j].axis("off")

    plt.tight_layout()
    plt.savefig(output_dir / "top_categories.png")
    plt.close()


def run_eda() -> None:
    root = Path(__file__).resolve().parents[2]
    csv_path = root / "input" / "petfinder-adoption-prediction" / "train" / "train.csv"
    output_dir = root / "work" / "EDA" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(output_dir / ".mpl-cache"))

    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontro el archivo: {csv_path}")

    setup_style()
    df = pd.read_csv(csv_path)

    save_dataframe_preview(df, output_dir)
    summarize_dataset(df, output_dir)
    plot_missingness(df, output_dir)
    plot_target_distribution(df, output_dir)
    plot_numeric_distributions(df, output_dir)
    plot_correlation_heatmap(df, output_dir)
    plot_target_vs_features(df, output_dir)
    plot_top_categories(df, output_dir)

    print(f"\nEDA completado. Resultados guardados en: {output_dir}")


if __name__ == "__main__":
    run_eda()
