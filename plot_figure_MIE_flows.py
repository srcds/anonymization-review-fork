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

import matplotlib.pyplot as plt
import pandas as pd
from pysankey2 import Sankey

plt.rcParams['svg.fonttype'] = 'none'

df = pd.read_csv("data_figure_MIE_flows.csv", sep=";")

def plot_figure_MIE_flows(df):
    # Remove columns not required and rename to "layer1" and "layer2"
    df.rename(columns={"World Bank income group (Data origin)": "layer1", "World Bank income group (First author)":"layer2"}, inplace=True)

    print(df["layer1"].unique())
    print(df["layer2"].unique())

    # Assign colors
    cmap_p1 = plt.get_cmap("Pastel1")
    cmap_p2 = plt.get_cmap("Pastel2")
    cmap_a = plt.get_cmap("Dark2")
    color_dict = {"layer1": {
                    'Low-income economies' : cmap_p2.colors[3],
                    'Lower-middle-income economies': cmap_p2.colors[2],
                    'Upper-middle-income economies': cmap_p2.colors[1],
                    'High-income economies': cmap_p2.colors[0],},
                  "layer2": {
                    'Upper-middle-income economies': cmap_p2.colors[7],
                    'High-income economies': cmap_p2.colors[7],
                    }
                  }


    # Costum order
    layer_labels = {'layer1': ['Low-income economies', 'Lower-middle-income economies', 'Upper-middle-income economies', 'High-income economies'],
                     'layer2':['Upper-middle-income economies', 'High-income economies']}

    # Plot sankey
    sky = Sankey(df, layerLabels = layer_labels,  colorDict=color_dict, colorMode="layer", stripColor='left', )
    #sky = Sankey(df, layerLabels = layer_labels, colorMode="layer", stripColor='left', )
    fig, ax = sky.plot(figSize=(7, 4), fontSize=10, boxInterv=0.05, boxWidth=0.5, stripLen=8)

    # Add label for "axes"
    ax.text(0, 690, 'Data source', weight='bold', fontsize=10, ha="left", va="bottom")
    ax.text(9, 690, 'ICD-10 chapter', weight='bold', fontsize=10, ha="right", va="bottom")

    # Plot and save
    fig.tight_layout()
    plt.savefig("figure_output/figure_MIE_flows.svg", bbox_inches='tight')
    plt.savefig("figure_output/figure_MIE_flows.png", bbox_inches='tight')
    plt.show()
    plt.close()
    plt.show()

plot_figure_MIE_flows(df)