import matplotlib.pyplot as plt
import pandas as pd

def create_numeric_histogram(df: pd.DataFrame, column: str):
    fig, ax = plt.subplots(figsize=(8, 4))
    df[column].dropna().hist(ax=ax, bins=30)
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return fig

def create_correlation_heatmap(df: pd.DataFrame):
    corr = df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, aspect="auto")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.index)

    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)

    ax.set_title("Correlation Heatmap")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    return fig

def create_categorical_bar_chart(df: pd.DataFrame, column: str):
    counts = df[column].astype(str).value_counts(dropna=False).head(15)
    fig, ax = plt.subplots(figsize=(8, 4))
    counts.plot(kind="bar", ax=ax)
    ax.set_title(f"Top Categories in {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig
