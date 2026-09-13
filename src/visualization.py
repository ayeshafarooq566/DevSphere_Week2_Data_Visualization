from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "superstore.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "charts"


def create_charts(df):
    """Create and save the required visualizations."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # 1. Sales by Category - Bar Chart
    # -----------------------------
    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        category_sales.index,
        category_sales.values
    )

    plt.title(
        "Total Sales by Product Category",
        fontsize=16,
        fontweight="bold"
    )
    plt.xlabel("Product Category")
    plt.ylabel("Sales ($)")
    plt.grid(axis="y", linestyle="--", alpha=0.3)

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"${bar.get_height():,.0f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "sales_by_category_bar.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # -----------------------------
    # 2. Sales by Year - Line Chart
    # -----------------------------
    yearly_sales = (
        df.groupby(df["Order Date"].dt.year)["Sales"]
        .sum()
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        yearly_sales.index,
        yearly_sales.values,
        marker="o",
        linewidth=2
    )

    plt.title(
        "Total Sales by Year",
        fontsize=16,
        fontweight="bold"
    )
    plt.xlabel("Year")
    plt.ylabel("Sales ($)")
    plt.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "sales_by_year_line.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # -----------------------------
    # 3. Sales Distribution - Pie Chart
    # -----------------------------
    plt.figure(figsize=(8, 8))

    plt.pie(
        category_sales,
        labels=category_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        "Sales Distribution by Product Category",
        fontsize=16,
        fontweight="bold"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "sales_distribution_pie.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


if __name__ == "__main__":

    df = pd.read_csv(
        DATA_PATH,
        encoding="latin1"
    )

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    create_charts(df)

    print("Charts created successfully.")