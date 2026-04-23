import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup
INPUT_FILE = "analysis/results_enriched.csv"
OUTPUT_DIR = "analysis/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Consistent styling
sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 200
plt.rcParams["font.size"] = 11

df = pd.read_csv(INPUT_FILE)


# Chart 1: Response length by race
def chart_length_by_race():
    fig, ax = plt.subplots(figsize=(8, 5))
    data = df.groupby("race")["word_count"].mean().sort_values()
    colors = ["#4C72B0", "#DD8452", "#55A467", "#C44E52"]
    bars = ax.bar(data.index, data.values, color=colors)
    ax.set_ylabel("Average Response Length (words)")
    ax.set_title("Response Length by Race", fontweight="bold", pad=15)
    ax.set_ylim(0, max(data.values) * 1.15)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                f"{bar.get_height():.0f}", ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/01_length_by_race.png")
    plt.close()


# Chart 2: The income finding (most interesting!)
def chart_income_effect():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    income_order = ["low-income", "middle-class", "wealthy"]
    colors = ["#C44E52", "#DD8452", "#55A467"]

    metrics = [
        ("word_count", "Avg Response Length (words)"),
        ("bias_flagged", "Avg Bias Flags per Response"),
        ("positive_word_count", "Avg Positive Word Count"),
    ]

    for ax, (col, title) in zip(axes, metrics):
        data = df.groupby("income")[col].mean().reindex(income_order)
        bars = ax.bar(data.index, data.values, color=colors)
        ax.set_title(title, fontweight="bold")
        ax.set_ylim(0, max(data.values) * 1.2)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(data.values)*0.02,
                    f"{bar.get_height():.2f}", ha="center", fontweight="bold")
        ax.tick_params(axis="x", rotation=15)

    fig.suptitle("The Income Paradox: Wealthy Prompts Get More Defensive, Shorter Responses",
                 fontweight="bold", fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/02_income_paradox.png")
    plt.close()


# Chart 3: Bias flags by scenario and race
def chart_scenario_race():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    pivot = df.groupby(["scenario", "race"])["bias_flagged"].mean().unstack()
    pivot.plot(kind="bar", ax=ax, width=0.8,
               color=["#4C72B0", "#DD8452", "#55A467", "#C44E52"])
    ax.set_ylabel("Average Bias Flags per Response")
    ax.set_xlabel("Scenario")
    ax.set_title("How Strongly Claude Flags Demographic Framing, by Scenario and Race",
                 fontweight="bold", pad=15)
    ax.legend(title="Race", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/03_scenario_race_flags.png")
    plt.close()


# Chart 4: Intersectional heatmap (race x gender)
def chart_intersectional_heatmap():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Heatmap 1: Word count
    pivot1 = df.groupby(["race", "gender"])["word_count"].mean().unstack()
    sns.heatmap(pivot1, annot=True, fmt=".0f", cmap="Blues", ax=axes[0],
                cbar_kws={"label": "Avg Word Count"})
    axes[0].set_title("Response Length: Race × Gender", fontweight="bold")

    # Heatmap 2: Bias flags
    pivot2 = df.groupby(["race", "gender"])["bias_flagged"].mean().unstack()
    sns.heatmap(pivot2, annot=True, fmt=".2f", cmap="Reds", ax=axes[1],
                cbar_kws={"label": "Avg Bias Flags"})
    axes[1].set_title("Bias Flagging: Race × Gender", fontweight="bold")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/04_intersectional_heatmap.png")
    plt.close()


# Chart 5: Risk vs positive language ratio
def chart_risk_vs_positive():
    fig, ax = plt.subplots(figsize=(10, 5.5))

    summary = df.groupby("race").agg(
        risk=("risk_word_count", "mean"),
        positive=("positive_word_count", "mean")
    )
    summary["ratio"] = summary["risk"] / summary["positive"]

    x = range(len(summary.index))
    width = 0.35
    ax.bar([i - width/2 for i in x], summary["risk"], width,
           label="Risk-language words", color="#C44E52")
    ax.bar([i + width/2 for i in x], summary["positive"], width,
           label="Positive-language words", color="#55A467")

    ax.set_xticks(x)
    ax.set_xticklabels(summary.index)
    ax.set_ylabel("Average Word Count per Response")
    ax.set_title("Risk vs. Positive Language by Race", fontweight="bold", pad=15)
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/05_risk_vs_positive.png")
    plt.close()


if __name__ == "__main__":
    chart_length_by_race()
    chart_income_effect()
    chart_scenario_race()
    chart_intersectional_heatmap()
    chart_risk_vs_positive()
    print(f"All charts saved to {OUTPUT_DIR}/")