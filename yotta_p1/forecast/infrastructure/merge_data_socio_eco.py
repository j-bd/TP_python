#!/usr/bin/env python
# coding: utf-8

import pandas as pd


def merge_data_socio_eco(data_input, socio_eco_input, output):

    data = pd.read_csv("data/raw/data.csv")
    socio_eco= pd.read_csv("data/raw/socio_eco.csv")

    data["MONTH_YEAR"] = pd.to_datetime(data["DATE"]).dt.to_period("M")
    socio_eco["MONTH_YEAR"] = pd.to_datetime(socio_eco["DATE"]).dt.to_period("M")
    socio_eco.drop(columns=["DATE"], inplace=True)

    # Merge socio eco dataframe with data
    df_data = data.merge(right=socio_eco, on="MONTH_YEAR", how="left")\
                  .drop(columns=["MONTH_YEAR"])

    df_data.to_csv("data/interim/data_socio_merged.csv", index=False)


if __name__ == "__main__":
    data_input = "data/raw/data.csv"
    socio_eco_input = "data/raw/socio_eco.csv"
    output = "data/interim/data_socio_merged.csv"
    merge_data_socio_eco(data_input, socio_eco_input, output)

