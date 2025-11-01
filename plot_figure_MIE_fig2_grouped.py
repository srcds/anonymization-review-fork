import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# --- Setup from original code ---
plt.rcParams['svg.fonttype'] = 'none'
mpl.style.use("ggplot")
COLOR = 'black'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

# Ensure output directory exists
os.makedirs("figure_output", exist_ok=True)

# Load your attached CSV
df = pd.read_csv("data_figure_MIE2_fig2.csv", sep=";")


# Helper to format integer labels robustly
def to_int_labels(values):
    out = []
    for v in values:
        if pd.isna(v):
            out.append("")
        else:
            try:
                out.append(f"{int(round(float(v)))}")
            except Exception:
                out.append(str(v))
    return out

def plot_figure_final_configurable(df):
    # --- Data Preparation ---

    df = df.set_index("Disease area")

    # Define once: which "Distribution" col pairs with which "Count" col and how it should be labeled in the legend
    series = [
        {
            "dist": "Distribution (Data: High-income, Author: High-income)",
            "count": "Count (Data: High-income, Author: High-income)",
            "label": "High-income data;\nHigh-income author",
        },
        {
            "dist": "Distribution (Data: Non-high-income, Author: High-income)",
            "count": "Count (Data: Non-high-income, Author: High-income)",
            "label": "Non-high-income data;\nHigh-income author",
        },
        {
            "dist": "Distribution (Data: Non-high-income, Author: Non-high-income)",
            "count": "Count (Data: Non-high-income, Author: Non-high-income)",
            "label": "Non-high-income data;\nNon-high-income author",
        },
        {
            "dist": "Distribution (GHE, High-income)",
            "count": "Count (GHE, High-income)",
            "label": "Death causes in high-income economies",
        },
        {
            "dist": "Distribution (GHE, Non-high-income)",
            "count": "Count (GHE, Non-high-income)",
            "label": "Death causes in non-high-income economies",
        },
    ]
    series_a = series[:3]  # top subplot
    series_b = series[3:]  # bottom subplot

    # --- Central Configuration Block ---
    base_fontsize = 14
    fontsize_axislabel = base_fontsize -2
    fontsize_ticklabel = base_fontsize - 2
    fontsize_barlabel = base_fontsize - 2
    fontsize_legend = base_fontsize - 2
    group_spacing = 0.9
    bar_width = 0.20

    # --- Plotting ---
    colormap = mpl.colormaps['Pastel2']
    indices_to_get = [0, 1, 2, 3, 4]
    colors = [colormap.colors[i] for i in indices_to_get]

    # Color map keyed by legend label (not by dataframe column names)
    all_labels = [s["label"] for s in series]
    color_map = {label: color for label, color in zip(all_labels, colors)}

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(10.5, 5),
        sharex=True,
        gridspec_kw={'height_ratios': [50, 40]}
    )

    x_indices = np.arange(len(df.index)) * group_spacing


    # Plot Subplot a) (Top): 3 series
    offsets_a = [-bar_width, 0, bar_width]
    for i, s in enumerate(series_a):
        pos = x_indices + offsets_a[i]
        heights = df[s["dist"]].values
        count_labels = to_int_labels(df[s["count"]].values)

        container = ax1.bar(
            pos, heights,
            width=bar_width,
            label=s["label"],
            color=color_map[s["label"]],
            edgecolor='black',
            linewidth=1.5
        )
        ax1.bar_label(
            container,
            labels=count_labels,         # <-- show COUNT here
            label_type='edge',
            fontsize=fontsize_barlabel,
            padding=3,
            color='black'
        )

    # Plot Subplot b) (Bottom): 2 series
    offsets_b = [-bar_width / 2, bar_width / 2]
    for i, s in enumerate(series_b):
        pos = x_indices + offsets_b[i]
        heights = df[s["dist"]].values
        count_labels = to_int_labels(df[s["count"]].values)

        container = ax2.bar(
            pos, heights,
            width=bar_width,
            label=s["label"],
            color=color_map[s["label"]],
            edgecolor='black',
            linewidth=1.5
        )
        ax2.bar_label(
            container,
            labels=count_labels,         # <-- show COUNT here
            label_type='edge',
            fontsize=fontsize_barlabel,
            padding=-16,                 # matches your original layout
            color='black'
        )

    # Styling and Configuration
    ax1.set_ylabel("Distribution [%]", fontsize=fontsize_axislabel)
    ax1.tick_params(axis='y', labelsize=fontsize_ticklabel)
    ax1.grid(axis='both', linestyle='--', alpha=0.7)

    ax2.set_ylabel("Distribution [%]", fontsize=fontsize_axislabel)
    ax2.tick_params(axis='y', labelsize=fontsize_ticklabel)
    ax2.grid(axis='both', linestyle='--', alpha=0.7)
    ax2.invert_yaxis()

    ax1.tick_params(axis='x', labelbottom=True, pad=0, length=6)
    ax2.tick_params(axis='x', labelbottom=False, length=6)

    new_labels = ['\nNeoplasms', 'Mental,\nneurological', 'Endocrine,\nmetabolic,\ngenitourinary',
                  'Cardio-\nvascular', '\nRespiratory', "Infectious,\nparasitic\ndiseases", "\nother"]
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(new_labels, rotation=0, fontsize=fontsize_ticklabel)

    ax1.set_ylim(0, 50)
    ax2.set_ylim(40, 0)
    ax1.set_yticks(np.arange(0, 41, 10))
    ax2.set_yticks(np.arange(0, 31, 10))

    # Legends (only relabelled via the bar's label argument)
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    fig.legend(
        handles1, labels1,
        loc='upper center',
        bbox_to_anchor=(0.52, 1.05, 0, 0),
        ncols=3,
        fontsize=fontsize_legend,
        frameon=True,
        columnspacing=4        # your wider spacing
    )
    fig.legend(
        handles2, labels2,
        loc='lower center',
        bbox_to_anchor=(0.52, -0.008, 0, 0),
        ncols=2,
        fontsize=fontsize_legend,
        frameon=True
    )

    # Final Layout Adjustments
    plt.tight_layout(rect=[0, 0.06, 1, 0.94])
    plt.subplots_adjust(hspace=0.5)

    # Save
    plt.savefig("figure_output/figure_MIE_fig2_final_configurable.svg", bbox_inches='tight')
    plt.savefig("figure_output/figure_MIE_fig2_final_configurable.png", bbox_inches='tight', dpi=300)
    plt.savefig("figure_output/figure_MIE_fig2_final_configurable.pdf", bbox_inches='tight')
    plt.show()


# Run the final plotting function
plot_figure_final_configurable(df)