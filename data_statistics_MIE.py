import pandas as pd
from tabulate import tabulate
import statsmodels.api as smApi
import statsmodels.regression.linear_model as smReg
import numpy as np
from collections import Counter

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
    # Create a new column 'Authors_list' by splitting the "Authors" string by " and "
    df['Authors_list'] = df['Authors'].apply(lambda x: [a.strip() for a in x.split(" and ")] if isinstance(x, str) else [])

    print("Loaded %d articles" % (len(df.index)))
    return df

df_charting = load_and_preprocess_charting()

def number_of_countries_per_income_group(df):

    # Filter out rows where 'Data origin' is "various"
    df = df[df['Data origin'] != "various"].copy()
    df = df.explode("Data origin_list")

    income_groups = ["High-income economies", "Low-income economies", "Lower-middle-income economies", "Upper-middle-income economies"]

    all_countries = pd.Series(
        pd.unique(df['First author'].tolist() + df['Data origin_list'].tolist()),
        name="Country"
    ).to_frame()
    df = pd.DataFrame(all_countries, columns=['Country'])

    print(f"Unique countries: {all_countries['Country'].nunique()}")
    print("Unique countries %d" % len(df["Country"].unique()))

    auxiliary_data_country_information = pd.read_csv("auxiliary_data/Country_information.csv", sep=";", dtype=str, na_filter=False)[["Country", "Name (Country)", "World Bank income group"]]
    df = pd.merge(df, auxiliary_data_country_information, how="left", on="Country")

    for income_group in income_groups:
        df_temp = df[df["World Bank income group"] == income_group]
        print()
        print(income_group)
        print("Unique countries %d" % len(df_temp["Country"].unique()))

#number_of_countries_per_income_group(df_charting)


def research_output_per_income_group(df):

    # Filter out rows where 'Data origin' is "various"
    df = df[df['Data origin'] != "various"].copy()
    df = df.explode("Data origin_list")

    all_countries = pd.Series(
        pd.unique(df['First author'].tolist() + df['Data origin_list'].tolist()),
        name="Country"
    ).to_frame()
    df = pd.DataFrame(all_countries, columns=['Country'])


    auxiliary_data_country_information = pd.read_csv("auxiliary_data/Country_information.csv", sep=";", dtype=str, na_filter=False)[["Country", "Name (Country)", "World Bank income group"]]
    df = pd.merge(df, auxiliary_data_country_information, how="left", on="Country")
    auxiliary_data_citable_documents = pd.read_csv("auxiliary_data/Citable_documents_per_country.csv", sep=";")[["Name (Country)", "Citable documents_total"]]
    df = pd.merge(df, auxiliary_data_citable_documents, on='Name (Country)', how='left')

    df = (df.groupby("World Bank income group", dropna=False).agg({
            "Citable documents_total": "sum"
        }).reset_index()
    )

    # Save to csv
    df.to_csv('data_figure_MIE_citableDocuments_per_IncomeGroup.csv', sep=";", index=False)

research_output_per_income_group(df_charting)
