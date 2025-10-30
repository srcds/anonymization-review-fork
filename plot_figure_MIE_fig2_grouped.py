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

def plot_figure_final_configurable(df):
    # --- Data Preparation ---
    cols_to_drop = [c for c in ["Region (Country)", "Country"] if c in df.columns]
    df = df.drop(columns=cols_to_drop, errors="ignore")
    df = df.set_index("Disease area")
    order_and_labels = [
        ("Distribution (Data: High-income, Author: High-income)", "High-income data;\nHigh-income author"),
        ("Distribution (Data: Non-high-income, Author: High-income)", "Non-high-income data;\nHigh-income author"),
        ("Distribution (Data: Non-high-income, Author: Non-high-income)",
         "Non-high-income data;\nNon-high-income author"),
        ("Distribution (GHE, High-income)", "Death causes in high-income economies"),
        ("Distribution (GHE, Non-high-income)", "Death causes in non-high-income economies"),
    ]
    order_and_labels_a = order_and_labels[:3]
    order_and_labels_b = order_and_labels[3:]
    cols_a, labels_a = zip(*order_and_labels_a)
    cols_b, labels_b = zip(*order_and_labels_b)
    df_a = df[list(cols_a)]; df_a.columns = labels_a
    df_b = df[list(cols_b)]; df_b.columns = labels_b

    # --- Central Configuration Block ---
    base_fontsize = 14
    fontsize_axislabel = base_fontsize
    fontsize_ticklabel = base_fontsize - 2
    fontsize_barlabel = base_fontsize - 2
    fontsize_legend = base_fontsize - 2
    group_spacing = 0.9
    bar_width = 0.20

    # --- Plotting ---
    colormap = mpl.colormaps['Pastel2']
    indices_to_get = [0, 1, 2, 3, 4]
    colors = [colormap.colors[i] for i in indices_to_get]
    color_map = {label: color for label, color in zip([l for _, l in order_and_labels], colors)}

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(10, 5),
        sharex=True,
        gridspec_kw={'height_ratios': [50, 40]}
    )

    x_indices = np.arange(len(df.index)) * group_spacing

    # Plot Subplot a) (Top)
    offsets_a = [-bar_width, 0, bar_width]
    for i, col in enumerate(df_a.columns):
        pos = x_indices + offsets_a[i]
        container = ax1.bar(pos, df_a[col], width=bar_width, label=col, color=color_map[col], edgecolor='black', linewidth=1.5)
        ax1.bar_label(container, fmt='%.0f', label_type='edge', fontsize=fontsize_barlabel, padding=3)

    # Plot Subplot b) (Bottom)
    offsets_b = [-bar_width / 2, bar_width / 2]
    for i, col in enumerate(df_b.columns):
        pos = x_indices + offsets_b[i]
        container = ax2.bar(pos, df_b[col], width=bar_width, label=col, color=color_map[col], edgecolor='black', linewidth=1.5)
        ax2.bar_label(container, fmt='%.0f', label_type='edge', fontsize=fontsize_barlabel, padding=-14, color='black')

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

    # --- KEY CHANGE 1: Move Legend to the bottom ---
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    # Legend for Plot 'a' (Top)
    fig.legend(handles1, labels1,
               loc='upper center',
               bbox_to_anchor=(0.5, 1.05), # Positioned at the top
               ncols=3,
               fontsize=fontsize_legend,
               frameon=True,)

    # Legend for Plot 'b' (Bottom)
    fig.legend(handles2, labels2,
               loc='lower center',
               bbox_to_anchor=(0.5, -0.05), # Positioned at the bottom
               ncols=2,
               fontsize=fontsize_legend,
               frameon=True,)

    # Final Layout Adjustments
    # Make room at the top (0.94) for the suptitle and at the bottom (0.1) for the legend
    plt.tight_layout(rect=[0, 0.06, 1, 0.94])

    # --- KEY CHANGE 2: Increase vertical space between the plots ---
    plt.subplots_adjust(hspace=0.5)

    # Save
    plt.savefig("figure_output/figure_MIE_fig2_final_configurable.svg", bbox_inches='tight')
    plt.savefig("figure_output/figure_MIE_fig2_final_configurable.png", bbox_inches='tight', dpi=300)
    plt.savefig("figure_output/figure_MIE_fig2_final_configurable.pdf", bbox_inches='tight')
    plt.show()

# Run the final plotting function
plot_figure_final_configurable(df)