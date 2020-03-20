#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:54:10 2020

@author: j-bd
"""

import os
import unicodedata
import datetime

import pandas as pd
import seaborn as sns
from dateutil.relativedelta import relativedelta
from jours_feries_france.compute import JoursFeries
from vacances_scolaires_france import SchoolHolidayDates

import constants as c


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
            print(
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
                word = unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode()
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


class AggregateData:
    """Allow to get information from sales report"""
    WEEKDAY = {
        'lundi' : 'monday', 'mardi' : 'tuesday', 'mercredi' : 'wednesday',
        'jeudi' : 'thursday', 'vendredi' : 'friday', 'samedi' : 'saturday',
        'dimanche' : 'sunday'
    }

    def __init__(self, df_original):
        """Initialize class with original csv"""
        self.df_original = df_original
        self.EXPORT_DF_NAME = f"processed_data_{'_'.join(c.EQUIP_SELEC)}_v1.csv"
        self.EXPORT_PLOT_NAME = f"{'_'.join(c.EQUIP_SELEC)}-{'_'.join(c.CITIES_SELEC)}.png"
        self.EXPORT_AGG = f"{'_'.join(c.EQUIP_SELEC)}-agg_graph.png"

    def create_specific_df(self):
        """Return a custom dataframe based on columns contains user choice"""
        init_df = pd.DataFrame(columns=self.df_original.columns)
        for value in c.CITIES_SELEC:
            filter_df = self.df_original[self.df_original.loc[:, c.COL_KEY["town"]] == value]
            frames = [init_df, filter_df]
            init_df = pd.concat(frames)

        second_df = pd.DataFrame(columns=self.df_original.columns)
        for value in c.EQUIP_SELEC:
            filter_df = init_df[init_df.loc[:, c.COL_KEY["equip"]] == value]
            frames = [second_df, filter_df]
            second_df = pd.concat(frames)

        self.working_df = second_df.reset_index(drop=True)
        return self.working_df

    def aggregate_sales_revenue(self):
        """Aggregate Sales Revenue for cities and equipment selected by day"""
        self.group_df = self.working_df.groupby(["DATE", "EQUIP"]).sum()
        self.group_df.reset_index(inplace=True)
        self.agg_graph()

    def add_sales_revenue_last_year(self):
        """Add a column with the sales revenue of one year before for each day"""
        for row_idx, row_value in self.working_df.iterrows():
            sales_rev_last_year = self.working_df.loc[
                (self.working_df[c.COL_KEY["town"]] == row_value[c.COL_KEY["town"]]) &
                (self.working_df[c.COL_KEY["equip"]] == row_value[c.COL_KEY["equip"]]) &
                (self.working_df[c.COL_KEY["date"]] == row_value[c.COL_KEY["date"]] - relativedelta(years=c.YEAR_STEP_BACKWARD)),
                c.COL_KEY["sales"]
            ]
            try:
                self.working_df.at[row_idx, 'sr_last_year'] = float(sales_rev_last_year.values)
            except TypeError:
                self.working_df.at[row_idx, 'sr_last_year'] = "Nan"

    def add_sales_revenue_last_year_weekday(self):
        """Add a column with the sales revenue of one year before for each day
        and linked to the same weekday"""
        for row_idx, row_value in self.working_df.iterrows():
            sales_rev_last_year_same_weekd = self.working_df.loc[
                (self.working_df[c.COL_KEY["town"]] == row_value[c.COL_KEY["town"]]) &
                (self.working_df[c.COL_KEY["equip"]] == row_value[c.COL_KEY["equip"]]) &
                (self.working_df[c.COL_KEY["date"]] == row_value[c.COL_KEY["date"]] +
                 relativedelta(
                    years=-c.YEAR_STEP_BACKWARD, weekday=row_value[c.COL_KEY["date"]].weekday()
                )), c.COL_KEY["sales"]
            ]
            try:
                self.working_df.at[row_idx, 'ca_last_year_same_weekday'] = float(
                    sales_rev_last_year_same_weekd
                )
            except TypeError:
                self.working_df.at[row_idx, 'ca_last_year_same_weekday'] = "Nan"

    def add_weekday(self):
        """Add a column with the weekday corresponding to the date"""
        for row_idx, row_value in self.working_df.iterrows():
            day = self.working_df.loc[row_idx, c.COL_KEY["date"]].strftime("%A")
            try:
                self.working_df.at[row_idx, 'weekday'] = self.WEEKDAY[day]
            except KeyError:
                self.working_df.at[row_idx, 'weekday'] = day

    def add_is_weekend(self):
        """Add a column with booleen value. True value for weekend"""
        for row_idx, row_value in self.working_df.iterrows():
            if self.working_df.loc[row_idx, "weekday"] in ['saturday', 'sunday']:
                self.working_df.at[row_idx, 'is weekend'] = True
            else:
                self.working_df.at[row_idx, 'is weekend'] = False

    def add_is_bankholiday(self):
        """Add a column with booleen value. True value for bankholiday"""
        year = 0
        bankholiday = []
        for row_idx, row_value in self.working_df.iterrows():
            if self.working_df.loc[row_idx, c.COL_KEY["date"]].year != year:
                year = self.working_df.loc[row_idx, c.COL_KEY["date"]].year
                bankholiday = list(JoursFeries.for_year(year).values())

            if self.working_df.loc[row_idx, c.COL_KEY["date"]] in bankholiday:
                self.working_df.at[row_idx, 'is_bankholiday'] = True
            else:
                self.working_df.at[row_idx, 'is_bankholiday'] = False

    def add_distance_to_bankholiday(self):
        """Add a column with booleen value. True value for bankholiday"""
        year = 0 #initiate variable
        bankholiday = []
        for row_idx, row_value in self.working_df.iterrows():
            if self.working_df.loc[row_idx, c.COL_KEY["date"]].year != year:
                year = self.working_df.loc[row_idx, c.COL_KEY["date"]].year
                bankholiday = list(JoursFeries.for_year(year).values())

            for bhd in bankholiday:
                if bhd > self.working_df.loc[row_idx, c.COL_KEY["date"]]:
                    self.working_df.at[
                        row_idx, 'dist_between_closest_bank_holiday'
                    ] = bhd - self.working_df.loc[row_idx, c.COL_KEY["date"]]
                    break

    def add_is_school_holiday(self):
        """Add a column with booleen value. True value for school holiday"""
        school_holiday_date = SchoolHolidayDates()
        for row_idx, row_value in self.working_df.iterrows():
            if school_holiday_date.is_holiday_for_zone(
                    row_value[c.COL_KEY["date"]],
                    c.TOWN_HOLIDAY_ZONE[row_value[c.COL_KEY["town"]]]
            ):
                self.working_df.at[row_idx, 'is_school_holiday'] = True
            else:
                self.working_df.at[row_idx, 'is_school_holiday'] = False

    def process_pipeline(self):
        """Launch full processing pipeline"""
        self.add_sales_revenue_last_year()
        self.add_sales_revenue_last_year_weekday()
        self.add_weekday()
        self.add_is_weekend()
        self.add_is_bankholiday()
        self.add_distance_to_bankholiday()
        self.add_is_school_holiday()

    def export_data(self):
        """Export custom DataFrane in a specidied folder"""
        self.working_df.to_csv(os.path.join(os.getcwd(), self.EXPORT_DF_NAME))

    def export_graph(self):
        """Export graph representation of full custom DataFrame"""
        plot = sns.relplot(
            x=c.COL_KEY["date"], y=c.COL_KEY["sales"], hue=c.COL_KEY["equip"],
            style=c.COL_KEY["town"], kind="line", data=self.working_df
        )
        plot.savefig(os.path.join(os.getcwd(), self.EXPORT_PLOT_NAME))

    def agg_graph(self):
        """Export aggregate sales revenues graph representation"""
        plot = sns.relplot(
            x=c.COL_KEY["date"], y=c.COL_KEY["sales"], hue=c.COL_KEY["equip"],
            kind="line", data=self.group_df
        )
        plot.savefig(os.path.join(os.getcwd(), self.EXPORT_AGG))



def main():
    """Launch main steps"""
    grd_w = DatasetFormatter()
    df_grd_w = grd_w.process_pipeline()

    fc = AggregateData(df_grd_w)
    fc.create_specific_df()
    fc.aggregate_sales_revenue()
    fc.process_pipeline()
    fc.export_data()
    fc.export_graph()

    return fc

if __name__ == "__main__":
    main()
