# ------------------------------------------------------------------------------
# Copyright 2025, T. Meurers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['svg.fonttype'] = 'none'
mpl.style.use("ggplot")
COLOR = 'black'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

# Read the data
df = pd.read_csv("data_figure_MIE_fig1.csv", sep=";")

def plot_distribution(df):

    # Prepare data
    categories = ["Domestic", "Intra-group sharing", "Extra-group sharing"]
    economies = [
        "Low-income economies",
        "Lower-middle-income economies",
        "Upper-middle-income economies",
        "High-income economies",
    ]

    # Create DataFrames for distribution and counts
    dist_df = pd.DataFrame({
        econ: df[f"Distribution ({econ})"].values for econ in economies
    }, index=categories)

    count_df = pd.DataFrame({
        econ: df[f"Count ({econ})"].values for econ in economies
    }, index=categories)

    # Transpose so each economy type becomes a row (bar)
    dist_df = dist_df.T
    count_df = count_df.T

    # Plot setup
    colormap = mpl.colormaps['Pastel2']
    colors = [colormap(i) for i in range(len(categories))]

    ax = dist_df.plot.barh(stacked=True, figsize=(6, 2.5),
                           color=colors, edgecolor="black", linewidth=1)

    ax.set_xlim([-2, 102])
    ax.set_xlabel("Distribution [%]", fontsize=10)
    ax.set_ylabel("Data origin by\ncountry income group", fontsize=10)
    #ax.legend(title="Sharing Type", bbox_to_anchor=(1.02, 1), loc='upper left')
    #ax.set_title("Distribution of Data Sharing Types by Economy Type")
    ax.set_yticklabels(["Low-income", "Lower-middle\nincome", "Upper-middle\nincome", "High-income"], fontsize=9)

    # Add count labels
    for i, econ in enumerate(dist_df.index):
        cum_width = 0
        for j, cat in enumerate(categories):
            width = dist_df.loc[econ, cat]
            if width > 0:
                count = count_df.loc[econ, cat]
                ax.text(cum_width + width / 2, i,
                        f"{int(count)}", ha='center', va='center', fontsize=9)
                cum_width += width
            else:
                cum_width += 0

    plt.legend(["Same country",
               "Same income group",
               "Different income group"],
              title="First author–Data origin relationship", loc='lower center', ncols=2, bbox_to_anchor=(0.5, 1))
    plt.tight_layout()
    plt.savefig("figure_output/distribution_plot.svg", bbox_inches='tight')
    plt.savefig("figure_output/distribution_plot.png", bbox_inches='tight')
    plt.savefig("figure_output/distribution_plot.pdf", bbox_inches='tight')
    plt.show()

plot_distribution(df)