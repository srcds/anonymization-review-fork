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

import pandas as pd

def load_and_preprocess_charting():

    # load data
    chart_file = "charting_results/results_20250228.csv"
    df = pd.read_csv(chart_file, dtype=str, sep=";", encoding='unicode_escape')

    # Fill empty cells with empty string
    df = df.fillna('')

    # Remove excluded articles
    df = df[df['Include'] == 'Yes']

    # split 1:n fields
    df["Data source_list"] = df.apply(lambda row: [label.lstrip() for label in row["Data source"].split(",")], axis=1)
    df["Data origin_list"] = df.apply(lambda row: row["Data origin"].replace(" ", "").strip().split(","), axis=1)

    print("Loaded %d articles" % (len(df.index)))
    return df


def preprocess_figure_MIE_fig1a(df):

    def filter_various(row):
        return row['Data origin_list'] != "various"

    # Split between corssborder and domestic uses
    df = df.explode('Data origin_list')
    df = df[df.apply(filter_various, axis=1)]

    # Read external CSV to append income group to first author
    auxiliary_data = pd.read_csv("auxiliary_data/Country_information.csv", sep=";")[["Country", "World Bank income group"]]
    df = pd.merge(df, auxiliary_data.rename(columns={"World Bank income group": "Origin income group"}), left_on='Data origin_list', right_on="Country", how='left')
    df = pd.merge(df, auxiliary_data.rename(columns={"World Bank income group": "Author income group"}), left_on="First author", right_on="Country", how="left")

    # Identify same-country and same-income-group cases
    df["same_country"] = (df["First author"] == df["Data origin_list"])
    df["same_group"] = (df["Origin income group"] == df["Author income group"])

    income_groups = ["High-income economies", "Upper-middle-income economies", "Lower-middle-income economies", "Low-income economies"]

    # Compute category counts
    #domestic = df[df['same_country']]['Origin income group'].value_counts().reindex(income_groups, fill_value=0)
    intra = df[df['same_group']]['Origin income group'].value_counts().reindex(income_groups, fill_value=0)
    external = df[~df['same_group']]['Origin income group'].value_counts().reindex(income_groups, fill_value=0)

    # Build transposed summary
    summary = pd.DataFrame({
        'Usage': ['Intra-group sharing', 'Extra-group sharing']
    })

    for group in income_groups:
        counts = [ intra[group], external[group]]
        total = sum(counts)
        dist = [(c / total * 100 if total > 0 else 0) for c in counts]
        summary[f'Count ({group})'] = counts
        summary[f'Distribution ({group})'] = dist


    summary.to_csv('data_figure_MIE_fig1a.csv', sep =";", index=False)

def preprocess_figure_MIE_fig1b(df, other_threshold_5b=0):

    def filter_various(row):
        return row['Data origin_list'] != "various"

    df = df.explode('Data origin_list')
    df = df[df.apply(filter_various, axis=1)]

    # Read external CSV to append income group to first author
    auxiliary_data = pd.read_csv("auxiliary_data/Country_information.csv", sep=";")[["Country", "World Bank income group"]]
    df = pd.merge(df, auxiliary_data.rename(columns={"World Bank income group": "Origin income group"}),left_on='Data origin_list', right_on="Country", how='left')
    df = pd.merge(df, auxiliary_data.rename(columns={"World Bank income group": "Author income group"}),left_on="First author", right_on="Country", how="left")

    df["same_group"] = (df["Author income group"] == df["Origin income group"])
    df = df[~df["same_group"]]


    # Filter combinations that do occure less than "other_threshold_5b" times
    df_combinations = df.groupby(['Origin income group', 'Author income group']).filter(lambda x: len(x) >= other_threshold_5b)[['Origin income group', 'Author income group']]

    df_combinations = df_combinations[['Origin income group', 'Author income group']]

    # Save to csv
    df_combinations.to_csv('data_figure_MIE_fig1b.csv', sep =";", index=False)

def preprocess_figure_MIE_distri(df, income_groups, domestic=True):
    def filter_only_assigned_ICD_chapter(row):
        return row['ICD-10 chapter'] != ""

    def filter_crossborder_origin(row):
        return row['Data origin_list'] != row["First author"]

    def filter_various(row):
        return row['Data origin_list'] != "various"

    def filter_for_income_group(row):
        return row['World Bank income group'] in income_groups

    # Split between corssborder and domestic uses
    df = df.explode('Data origin_list')
    df = df[df.apply(filter_various, axis=1)]
    if domestic:
        df = df[~df.apply(filter_crossborder_origin, axis=1)]
    else:
        df = df[df.apply(filter_crossborder_origin, axis=1)]

    # Read external CSV to append income group to first author
    auxiliary_data = pd.read_csv("auxiliary_data/Country_information.csv", sep=";")[["Country", "World Bank income group"]]
    df = pd.merge(df, auxiliary_data, left_on='First author', right_on="Country", how='left')

    # Remove records not assigned to a chapter
    df = df[df.apply(filter_only_assigned_ICD_chapter, axis=1)]

    # Filter for specific income group
    df = df[df.apply(filter_for_income_group, axis=1)]

    # Count occurrences of chapters
    df = df['ICD-10 chapter'].value_counts().reset_index()
    df.columns = ['ICD-10 chapter', 'Count (ICD-10 chapter)']

    # Read external CSV with total number of articles published
    auxiliary_data = pd.read_csv("auxiliary_data/ICD-10_chapter_mapping_selected.csv", sep=";",skiprows=0, dtype=str)
    explicit_chapters = auxiliary_data['ICD-10 chapter'].unique()
    df = pd.merge(df, auxiliary_data, on='ICD-10 chapter', how='outer')

    # Fill missing values with 0
    df.fillna(0, inplace=True)

    # Convert float counts to integers
    df['Count (ICD-10 chapter)'] = df['Count (ICD-10 chapter)'].astype(int)

    # Calculate distribution
    df['Distribution (ICD-10 chapter)'] = df['Count (ICD-10 chapter)'] * 100 / df['Count (ICD-10 chapter)'].sum()

    # Split country files into countries commonly mentioned and "other" by given threshold
    df_other = df[~df['ICD-10 chapter'].isin(explicit_chapters)]
    df = df[df['ICD-10 chapter'].isin(explicit_chapters)]

    # Sort
    df = df.sort_values("Count (ICD-10 chapter)", ascending=False)

    # Create and append "other" column
    row_other = {"ICD-10 chapter": "other", "Name (ICD-10 chapter)": "other", "Count (ICD-10 chapter)": df_other["Count (ICD-10 chapter)"].sum(), "Distribution (ICD-10 chapter)": df_other["Distribution (ICD-10 chapter)"].sum()}
    df = df._append(row_other, ignore_index=True)

    df.to_csv('data_figure_MIE2_%s_%s.csv' % (income_groups, domestic), sep =";", index=False)




def preprocess_figure_MIE_fig2(df, data_origin_group, author_origin_group):
    def filter_only_assigned_ICD_chapter(row):
        return row['ICD-10 chapter'] != ""

    def filter_various(row):
        return row['Data origin_list'] != "various"

    # Split between corssborder and domestic uses
    df = df.explode('Data origin_list')

    # Filter various and unassigned ICD chapter
    df = df[df.apply(filter_various, axis=1)]
    df = df[df.apply(filter_only_assigned_ICD_chapter, axis=1)]

    # Append income group of author and data
    auxiliary_data = pd.read_csv("auxiliary_data/Country_information.csv", sep=";")[["Country", "World Bank income group"]]
    df = pd.merge(df, auxiliary_data.rename(columns={"World Bank income group": "Origin income group"}),left_on='Data origin_list', right_on="Country", how='left')
    df = pd.merge(df, auxiliary_data.rename(columns={"World Bank income group": "Author income group"}),left_on="First author", right_on="Country", how="left")

    # Append mapping to GHE disease area
    auxiliary_data = pd.read_csv("auxiliary_data/ICD_GHE_mapping.csv", sep=";", dtype="str")
    df = pd.merge(df, auxiliary_data, on = "ICD-10 chapter", how="left")

    # Filter for specific income group
    df = df[df['Origin income group'].isin(data_origin_group)]
    df = df[df['Author income group'].isin(author_origin_group)]

    # Count occurrences of chapters
    df = df['Disease area'].value_counts().reset_index()
    df.columns = ['Disease area', 'Count (Disease area)']

    # Fill missing values with 0
    df.fillna(0, inplace=True)

    # Convert float counts to integers
    df['Count (Disease area)'] = df['Count (Disease area)'].astype(int)

    # Calculate distribution
    df['Distribution (Disease area)'] = df['Count (Disease area)'] * 100 / df['Count (Disease area)'].sum()

    explicit_disease_areas = ["Infectious and parasitic diseases", "Respiratory Infectious and diseases", "Neoplasms", "Endocrine, Metabolic, Immune and Genitourinary Disorders", "Mental and neurological conditions", "Cardiovascular diseases", "Injuries"]

    # Split country files into countries commonly mentioned and "other" by given threshold
    #df_other = df[~df['Disease area'].isin(explicit_disease_areas)]
    #df = df[df['Disease area'].isin(explicit_disease_areas)]

    # Sort
    df = df.sort_values("Disease area", ascending=False)

    # Create and append "other" column
    #row_other = {"Disease area": "other", "Name (Disease area)": "other", "Count (Disease area)": df_other["Count (Disease area)"].sum(), "Distribution (Disease area)": df_other["Distribution (Disease area)"].sum()}
    #df = df._append(row_other, ignore_index=True)

    df.to_csv('data_figure_MIE2_fig2_%s_%s.csv' % (data_origin_group, author_origin_group), sep =";", index=False)

def preprocess_figure_MIE_fig2_ICD(df, data_origin_group, author_origin_group):
    def filter_only_assigned_ICD_chapter(row):
        return row['ICD-10 chapter'] != ""

    def filter_various(row):
        return row['Data origin_list'] != "various"

    df = df.explode('Data origin_list')
    df = df[df.apply(filter_various, axis=1)]
    df = df[df.apply(filter_only_assigned_ICD_chapter, axis=1)]

    # Append income group of author and data
    auxiliary_data = pd.read_csv("auxiliary_data/Country_information.csv", sep=";")[["Country", "World Bank income group"]]
    df = pd.merge(df, auxiliary_data.rename(columns={"World Bank income group": "Origin income group"}), left_on='Data origin_list', right_on="Country", how='left')
    df = pd.merge(df, auxiliary_data.rename(columns={"World Bank income group": "Author income group"}), left_on="First author", right_on="Country", how="left")

    # Filter for specific income group
    df = df[df['Origin income group'].isin(data_origin_group)]
    df = df[df['Author income group'].isin(author_origin_group)]

    # Count occurrences of chapters
    df = df['ICD-10 chapter'].value_counts().reset_index()
    df.columns = ['ICD-10 chapter', 'Count (ICD-10 chapter)']

    # Read external CSV with total number of articles published
    auxiliary_data = pd.read_csv("auxiliary_data/ICD-10_chapter_mapping_selected.csv", sep=";",skiprows=0, dtype=str)
    explicit_chapters = auxiliary_data['ICD-10 chapter'].unique()
    df = pd.merge(df, auxiliary_data, on='ICD-10 chapter', how='outer')

    # Fill missing values with 0
    df.fillna(0, inplace=True)

    # Convert float counts to integers
    df['Count (ICD-10 chapter)'] = df['Count (ICD-10 chapter)'].astype(int)

    # Calculate distribution
    df['Distribution (ICD-10 chapter)'] = df['Count (ICD-10 chapter)'] * 100 / df['Count (ICD-10 chapter)'].sum()

    # Split country files into countries commonly mentioned and "other" by given threshold
    df_other = df[~df['ICD-10 chapter'].isin(explicit_chapters)]
    df = df[df['ICD-10 chapter'].isin(explicit_chapters)]

    # Sort
    df = df.sort_values("Count (ICD-10 chapter)", ascending=False)

    # Create and append "other" column
    row_other = {"ICD-10 chapter": "other", "Name (ICD-10 chapter)": "other", "Count (ICD-10 chapter)": df_other["Count (ICD-10 chapter)"].sum(), "Distribution (ICD-10 chapter)": df_other["Distribution (ICD-10 chapter)"].sum()}
    df = df._append(row_other, ignore_index=True)

    df.to_csv('data_figure_MIE2_fig2_ICD_%s_%s.csv' % (data_origin_group, author_origin_group), sep =";", index=False)


df_raw = load_and_preprocess_charting()

#preprocess_figure_MIE_fig1a(df_raw)
#preprocess_figure_MIE_fig1b(df_raw)

preprocess_figure_MIE_fig2(df_raw,  ["High-income economies"], ["High-income economies"])
preprocess_figure_MIE_fig2(df_raw, ['Low-income economies', 'Lower-middle-income economies', 'Upper-middle-income economies'], ["High-income economies"])
preprocess_figure_MIE_fig2(df_raw, ['Low-income economies', 'Lower-middle-income economies', 'Upper-middle-income economies'], ['Low-income economies', 'Lower-middle-income economies', 'Upper-middle-income economies'])

#preprocess_figure_S1(df_raw)