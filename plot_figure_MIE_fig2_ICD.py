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
df = pd.read_csv("data_figure_MIE2_fig2_ICD.csv", sep=";")

def plot_figure_grouped(df):

    # Drop unnecessary columns
    cols_to_drop = [c for c in ["Region (Country)", "Country"] if c in df.columns]
    df = df.drop(columns=cols_to_drop, errors="ignore")

    # Identify distribution and count columns
    dist_cols = [c for c in df.columns if c.startswith("Distribution")]
    count_cols = [c for c in df.columns if c.startswith("Count")]

    # Build a robust mapping Distribution -> Count
    count_map = {}
    for d in dist_cols:
        candidate = d.replace("Distribution", "Count")
        if candidate in df.columns:
            count_map[d] = candidate
    # Fallback if any are missing (keeps positional pairing for any unmatched)
    if len(count_map) != len(dist_cols):
        for d, c in zip(dist_cols, count_cols):
            count_map.setdefault(d, c)

    # Set index to Disease area
    if "Name (ICD-10 chapter)" not in df.columns:
        raise ValueError("Expected column 'Disease area' not found in the dataset.")
    df = df.set_index("Name (ICD-10 chapter)")

    # Data to plot (transpose so disease areas become columns)
    df_plot = df[dist_cols].T
    print(tabulate(df_plot, headers='keys', tablefmt='psql'))

    # Desired row order + pretty labels
    order_and_labels = [
        ("Distribution (Data: High-income, Author: High-income)", "High-income data;\nHigh-income author"),
        ("Distribution (Data: Non-high-income, Author: High-income)", "Non-high-income data;\nHigh-income author"),
        ("Distribution (Data: Non-high-income, Author: Non-high-income)", "Non-high-income data;\nNon-high-income author"),
    ]
    new_order = [x[0] for x in order_and_labels]
    new_labels = [x[1] for x in order_and_labels]

    # Reindex rows to the desired order
    df_plot = df_plot.reindex(new_order)

    # Apply pretty row labels for plotting
    df_plot.index = new_labels


    # Colormap
    colormap = mpl.colormaps['Pastel2']
    colors = [colormap(i) for i in range(len(df.columns.tolist()))]
    colors[6] = colormap(8)

    # Plot
    ax = df_plot.plot.barh(
        stacked=True,
        figsize=(9, 3),
        color=colors,
        edgecolor="black",
        linewidth=1
    )

    ax.set_xlim([-2, 102])
    ax.set_xticks(range(0, 101, 10))
    ax.set_xlabel("Distribution [%]", size=10)
    #ax.set_ylabel("Data and author origin by\ncountry income group", fontsize=10)
    ax.invert_yaxis()
    ax.axhline(y=2.5, color="grey", linewidth=1.2, linestyle="--")

    # === Correct labeling logic ===
    # containers: one per Disease area (df_plot.columns)
    # inside each container: rectangles in the order of rows (df_plot.index/new_order)
    # We need the original Distribution key for each row by position.
    row_dist_order = new_order  # same order as before relabeling
    disease_names = list(df_plot.columns)

    for col_idx, container in enumerate(ax.containers):
        disease = disease_names[col_idx]  # Disease area name
        for row_idx, rect in enumerate(container):
            # Distribution column for this row
            dist_name = row_dist_order[row_idx]
            count_col = count_map[dist_name]

            width = rect.get_width()  # this is the % value
            if width > 5:  # show only if > 5%
                count_val = df.loc[disease, count_col]
                try:
                    label_txt = f"{int(round(float(count_val)))}"
                except Exception:
                    label_txt = f"{count_val}"

                ax.text(
                    rect.get_x() + rect.get_width() / 2,
                    rect.get_y() + rect.get_height() / 2,
                    label_txt,
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="black"
                )

    # Legend and layout
    plt.legend(loc='lower center', ncols=2, bbox_to_anchor=(0.5, 1))
    plt.tight_layout()

    # Save
    plt.savefig("figure_output/figure_MIE_fig2_ICD.svg", bbox_inches='tight')
    plt.savefig("figure_output/figure_MIE_fig2_ICD.png", bbox_inches='tight')
    plt.savefig("figure_output/figure_MIE_fig2_ICD.pdf", bbox_inches='tight')
    plt.show()

plot_figure_grouped(df)
