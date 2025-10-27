'''
------------------------------------------------------------------------------
Copyright 2025, T. Meurers

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------------
'''

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pysankey2 import Sankey

plt.rcParams['svg.fonttype'] = 'none'
mpl.style.use("ggplot")
COLOR = 'black'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

df_counts = pd.read_csv("data_figure_MIE_groupDistribution.csv", sep=";")

def plot_figure_5a(df):

    # Set font sizes
    font_size_label = 10
    font_size_ticks = 10
    font_size_legend = 10
    font_size_bar_label = 10
    distance_bar_label = 0.02
    y_lim = 0.5

    # Plot configuration
    fig, ax = plt.subplots(figsize=(4, 3.5))

    x = np.arange(len(df["World Bank income group"])) # the label locations
    width = 0.35  # the width of the bars

    bars_first_author = ax.bar(x - width/2 -0.03, df["First author per 1000 citable documents"], width, color='#B3E2CD', edgecolor="black", linewidth=1)
    bars_data_origin = ax.bar(x + width/2 +0.03, df["Data origin per 1000 citable documents"], width, color='#FDCDAC', edgecolor="black", linewidth=1)

    # Adding value labels to each bar
    for idx, rect in enumerate(bars_first_author):
        ax.text(rect.get_x() + rect.get_width() / 2.0, df["First author per 1000 citable documents"][idx] + distance_bar_label, str(df["Count (First Author)"][idx]),
                ha='center', va='bottom', fontsize=font_size_bar_label)

    for idx, rect in enumerate(bars_data_origin):
        ax.text(rect.get_x() + rect.get_width() / 2.0, df["Data origin per 1000 citable documents"][idx] + distance_bar_label, str(df["Count (Data origin)"][idx]),
                ha='center', va='bottom', fontsize=font_size_bar_label)

    # Grid
    ax.grid(axis='x')

    # Customizations with larger font sizes
    ax.set_ylabel('Origin per 1000 \n citable documents', fontsize=font_size_label)
    ax.set_xticks(x)
    ax.set_xticklabels(df["World Bank income group"], fontsize=font_size_ticks,  rotation=45, ha="center")
    #ax.set_yticks(np.arange(0, y_lim+1, 10), np.arange(0, y_lim+1, 10).astype(int), fontsize=font_size_ticks)
    ax.tick_params(axis='y', labelsize=font_size_ticks)
    ax.set_ylim(0, y_lim)

    ax.set_title("A\n", loc="left")

    fig.tight_layout()

    plt.legend(handles=[bars_first_author,  bars_data_origin], labels=['First author', 'Data'], loc='lower center', ncols = 2, bbox_to_anchor=(0.5, 1), fontsize=font_size_legend)
    plt.savefig("figure_output/figure_MIE_groupDistribution5a.svg", bbox_inches='tight')
    plt.savefig("figure_output/figure_MIE_groupDistribution5a.png", bbox_inches='tight')
    plt.show()
    plt.close()

plot_figure_5a(df_counts)