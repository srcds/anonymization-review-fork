import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

plt.rcParams['svg.fonttype'] = 'none'
mpl.style.use("ggplot")
COLOR = 'black'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

# Load your attached CSV
df = pd.read_csv("data_figure_MIE2_fig2.csv", sep=";")

def plot_figure_grouped(df):

    # Drop columns not required (adjust as needed)
    cols_to_drop = [c for c in ["Region (Country)", "Country", "Count (First author)", "Count (Data origin)"] if c in df.columns]
    df = df.drop(columns=cols_to_drop, errors="ignore")

    # Set index to Disease area
    if "Disease area" not in df.columns:
        raise ValueError("Expected column 'Disease area' not found in the dataset.")
    df = df.set_index("Disease area")

    # Transpose so disease areas are columns
    df = df.T
    print(tabulate(df, headers='keys', tablefmt='psql'))

    # Define new row order
    new_order = [
        "Distribution (Data: High-income, Author: High-income)",
        "Distribution (Data: Non-high-income, Author: High-income)",
        "Distribution (Data: Non-high-income, Author: Non-high-income)",
        "Distribution (GHE, High-income)",
        "Distribution (GHE, Non-high-income)"
    ]
    df = df.reindex(new_order)

    # Apply line breaks for the first three
    df.index = [
        "Data: High-income\nAuthor: High-income",
        "Data: Non-high-income\nAuthor: High-income",
        "Data: Non-high-income\nAuthor: Non-high-income",
        "GHE, High-income",
        "GHE, Non-high-income"
    ]

    # Colormap
    colormap = mpl.colormaps['Pastel2']
    colors = [colormap(i) for i in range(len(df.columns.tolist()))]
    colors[-1] = colormap(8)

    # Plot
    ax = df.plot.barh(
        stacked=True,
        figsize=(10, 4),
        color=colors,
        edgecolor="black",
        linewidth=1
    )

    ax.set_xlim([-2, 102])
    ax.set_xticks(range(0, 101, 10))
    ax.set_xlabel("Geographical distribution [%]", size=10)
    ax.invert_yaxis()

    # Add horizontal divider between groups
    ax.axhline(y=2.5, color="grey", linewidth=1.2, linestyle="--")

    # Annotations
    for c in ax.containers:
        labels_big = [f'{w:.1f}' if (w := v.get_width()) >= 3.4 else '' for v in c]
        ax.bar_label(c, labels=labels_big, label_type='center', fontsize=8)

    # Legend
    plt.legend(loc='lower center', ncols=2, bbox_to_anchor=(0.5, 1))
    plt.tight_layout()

    plt.savefig("figure_output/figure_MIE_fig2.svg", bbox_inches='tight')
    plt.savefig("figure_output/figure_MIE_fig2.png", bbox_inches='tight')
    plt.savefig("figure_output/figure_MIE_fig2.pdf", bbox_inches='tight')
    plt.show()

plot_figure_grouped(df)