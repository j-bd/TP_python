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

class DatasetPreparation:
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
        """Return the input dataset as a dataframe"""
        if self.extension == "csv":
            df = pd.read_csv(c.INPUT_FILE_NAME)
        else:
            df = pd.read_parquet(c.INPUT_FILE_NAME, engine='pyarrow')
        return df

    @property
    def prepare_data(self):
        """Launch full processing pipeline"""
        self._rename_columns()
        self._format_date()
        self._clean_letters()
        self._rename_cities()
        self._check_columns_format()
        return self.df

    def _rename_columns(self):
        """Rename columns following a pre-defined pattern in constants file"""
        self.df.rename(columns=c.COLUMNS_NAMES_VARIATION, inplace=True)

    def _format_date(self):
        """Provide the right date format"""
        for line, val in enumerate(self.df.loc[:, c.COL_KEY["date"]]):
            date_format = datetime.datetime.strptime(
                val, c.DATE_FORMAT[self.extension]
            ).date()
            self.df.loc[line, c.COL_KEY["date"]] = date_format

    def _clean_letters(self):
        """Remove accent letters"""
        for col_name in c.COL_STR_FORMAT:
            for line, val in enumerate(self.df.loc[:, col_name]):
                word = unicodedata.normalize('NFKD', val)\
                    .encode('ascii', 'ignore').decode()
                self.df.loc[line, col_name] = word

    def _rename_cities(self):
        """Take all cities spelling variations list in constants and uniform it"""
        self.df.replace(c.CITIES_NAMES_VARIATION, inplace=True)

    def _check_columns_format(self):
        """Check if columns numbers are set to float"""
        for col_name in c.COL_NUMBER_FORMAT:
            self.df[col_name] = pd.to_numeric(self.df[col_name])
