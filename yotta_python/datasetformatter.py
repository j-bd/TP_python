#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 18:02:14 2020

@author: j-bd
"""

import unicodedata
import datetime
import logging

import pandas as pd

import constants as c

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class DatasetFormatter:
    """Return a clean DataFrame object as defined in constants file"""

    def __init__(self):
        """Initialize class with original data"""
        self.check_extension()
        self.df = self.read_data()

    def check_extension(self):
        """Check extension of input file"""
        self.extension = c.INPUT_FILE_NAME.split(sep=".")[-1].lower()
        if self.extension not in ["csv", "parquet"]:
            logging.ERROR(
                "Extension not take into account. Please get 'csv' or 'parquet'"
                " file"
            )

    def read_data(self):
        """Return a dataframe"""
        if self.extension == "csv":
            df = pd.read_csv(c.INPUT_FILE_NAME)
        else:
            df = pd.read_parquet(c.INPUT_FILE_NAME, engine='pyarrow')
        return df

    def rename_columns(self):
        """Rename columns following a pre-defined pattern in constants file"""
        self.df.rename(columns=c.COLUMNS_NAMES_VARIATION, inplace=True)

    def format_date(self):
        """Provide the right date format"""
        for line, val in enumerate(self.df.loc[:, c.COL_KEY["date"]]):
            date_format = datetime.datetime.strptime(
                val, c.DATE_FORMAT[self.extension]
            ).date()
            self.df.loc[line, c.COL_KEY["date"]] = date_format

    def clean_letters(self):
        """Remove accent letters"""
        for col_name in c.COL_STR_FORMAT:
            for line, val in enumerate(self.df.loc[:, col_name]):
                word = unicodedata.normalize('NFKD', val)\
                    .encode('ascii', 'ignore').decode()
                self.df.loc[line, col_name] = word

    def rename_cities(self):
        """Rename cities"""
        self.df.replace(c.CITIES_NAMES_VARIATION, inplace=True)

    def check_columns_format(self):
        """Check if columns numbers are set to float"""
        for col_name in c.COL_NUMBER_FORMAT:
            self.df[col_name] = pd.to_numeric(self.df[col_name])

    def process_pipeline(self):
        """Launch full processing pipeline"""
        self.rename_columns()
        self.format_date()
        self.clean_letters()
        self.rename_cities()
        self.check_columns_format()
        return self.df


def main():
    """Launch main steps"""
    grd_w = DatasetFormatter()
    df_grd_w = grd_w.process_pipeline



if __name__ == "__main__":
    main()
