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


class Groundwork:
    '''Return a clean DataFrame object as defined in constants file'''
    def __init__(self, file_path):
        '''Initialize class with original data'''
        self.df = self.check_extension(file_path)

    def check_extension(self, file_path):
        '''Check extension of input file'''
        self.ext = c.FILE_NAME.split(sep=".")[-1].lower()
        if self.ext == "csv":
            df = pd.read_csv(file_path)
        elif self.ext == "parquet":
            df = pd.read_parquet(file_path, engine='pyarrow')
        else:
            print(
                "Extension not take into account. Please get 'csv' or 'parquet'"
                " file"
            )
        return df

    def rename_columns(self):
        '''Rename columns following a pre-defined pattern in constants file'''
        self.df.rename(columns=c.COLUMNS_NAMES, inplace=True)

    def set_date(self):
        '''Provide the right date format'''
        for line, val in enumerate(self.df.loc[:, c.NAMES["d"]]):
            date_format = datetime.datetime.strptime(
                val, c.DATE_FORMAT[self.ext]
            ).date()
            self.df.loc[line, c.NAMES["d"]] = date_format

    def clean_letters(self):
        '''Remove accent letters'''
        for col_name in c.STR_COLUMN:
            for line, val in enumerate(self.df.loc[:, col_name]):
                word = unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode()
                self.df.loc[line, col_name] = word

    def check_cities(self):
        '''Rename cities'''
        self.df.replace(c.CITIES_NAMES, inplace=True)

    def check_numbers(self):
        '''Check if numbers are set to float'''
        for col_name in c.NUMBER_COLUMN:
            self.df[col_name] = pd.to_numeric(self.df[col_name])

    def process_pipeline(self):
        '''Launch full processing pipeline'''
        self.rename_columns()
        self.set_date()
        self.clean_letters()
        self.check_cities()
        self.check_numbers()
        return self.df



class Forecast:
    '''Allow to get information from sales report'''
    export_df_name = "processed_data_{equipement}_v1.csv"
    export_plot_name = "graph.png"
    export_agg = "agg_graph.png"
    weekday = {
        'lundi' : 'monday', 'mardi' : 'tuesday', 'mercredi' : 'wednesday',
        'jeudi' : 'thursday', 'vendredi' : 'friday', 'samedi' : 'saturday',
        'dimanche' : 'sunday'
    }

    def __init__(self, df_original):
        '''Initialize class with original csv'''
        self.df_original = df_original

    def create_specific_df(self, town_list, equipement_list):
        '''Return a custom dataframe based on columns contains user choice'''
        init_df = pd.DataFrame(columns=self.df_original.columns)
        for value in town_list:
            filter_df = self.df_original[self.df_original.loc[:, c.NAMES["t"]] == value]
            frames = [init_df, filter_df]
            init_df = pd.concat(frames)

        second_df = pd.DataFrame(columns=self.df_original.columns)
        for value in equipement_list:
            filter_df = init_df[init_df.loc[:, c.NAMES["e"]] == value]
            frames = [second_df, filter_df]
            second_df = pd.concat(frames)

        self.working_df = second_df.reset_index(drop=True)
        return self.working_df

    def agregate_sr(self):
        '''Agregate Sales Revenues for cities and equipment selected by day'''
        self.group_df = self.working_df.groupby(["DATE", "EQUIP"]).sum()
        self.group_df.reset_index(inplace=True)
        self.agg_graph()

    def add_sr_last_year(self):
        '''Add a column with the sales revenue of one year before for each day'''
        for ind_r, values_r in self.working_df.iterrows():
            sr_l_y = self.working_df.loc[
                (self.working_df[c.NAMES["t"]] == values_r[c.NAMES["t"]]) &
                (self.working_df[c.NAMES["e"]] == values_r[c.NAMES["e"]]) &
                (self.working_df[c.NAMES["d"]] == values_r[c.NAMES["d"]] - relativedelta(years=1)),
                c.NAMES["s"]
            ]
            try:
                self.working_df.at[ind_r, 'sr_last_year'] = float(sr_l_y.values)
            except TypeError:
                self.working_df.at[ind_r, 'sr_last_year'] = "Nan"

    def add_sr_last_year_weekday(self):
        '''Add a column with the sales revenue of one year before for each day
        and linked to the same weekday'''
        for ind_r, values_r in self.working_df.iterrows():
            sr_l_y_sw = self.working_df.loc[
                (self.working_df[c.NAMES["t"]] == values_r[c.NAMES["t"]]) &
                (self.working_df[c.NAMES["e"]] == values_r[c.NAMES["e"]]) &
                (self.working_df[c.NAMES["d"]] == values_r[c.NAMES["d"]] +
                 relativedelta(years=-1, weekday=values_r[c.NAMES["d"]].weekday())),
                c.NAMES["s"]
            ]
            try:
                self.working_df.at[ind_r, 'ca_last_year_same_weekday'] = float(sr_l_y_sw)
            except TypeError:
                self.working_df.at[ind_r, 'ca_last_year_same_weekday'] = "Nan"

    def add_weekday(self):
        '''Add a column with the weekday corresponding to the date'''
        cls = self.__class__
        for ind_r, values_r in self.working_df.iterrows():
            day = self.working_df.loc[ind_r, c.NAMES["d"]].strftime("%A")
            try:
                self.working_df.at[ind_r, 'weekday'] = cls.weekday[day]
            except KeyError:
                self.working_df.at[ind_r, 'weekday'] = day

    def add_is_weekend(self):
        '''Add a column with booleen value. True value for weekend'''
        for ind_r, values_r in self.working_df.iterrows():
            if self.working_df.loc[ind_r, "weekday"] in ['saturday', 'sunday']:
                self.working_df.at[ind_r, 'is weekend'] = True
            else:
                self.working_df.at[ind_r, 'is weekend'] = False

    def add_is_bankholiday(self):
        '''Add a column with booleen value. True value for bankholiday'''
        year = 0
        bankholiday = []
        for ind_r, values_r in self.working_df.iterrows():
            if self.working_df.loc[ind_r, c.NAMES["d"]].year != year:
                year = self.working_df.loc[ind_r, c.NAMES["d"]].year
                bankholiday = list(JoursFeries.for_year(year).values())

            if self.working_df.loc[ind_r, c.NAMES["d"]] in bankholiday:
                self.working_df.at[ind_r, 'is_bankholiday'] = True
            else:
                self.working_df.at[ind_r, 'is_bankholiday'] = False

    def add_distance_to_bankholiday(self):
        '''Add a column with booleen value. True value for bankholiday'''
        year = 0
        bankholiday = []
        for ind_r, values_r in self.working_df.iterrows():
            if self.working_df.loc[ind_r, c.NAMES["d"]].year != year:
                year = self.working_df.loc[ind_r, c.NAMES["d"]].year
                bankholiday = list(JoursFeries.for_year(year).values())

            for bhd in bankholiday:
                if bhd > self.working_df.loc[ind_r, c.NAMES["d"]]:
                    self.working_df.at[
                        ind_r, 'dist_between_closest_bank_holiday'
                    ] = bhd - self.working_df.loc[ind_r, c.NAMES["d"]]
                    break

    def add_is_school_holiday(self):
        '''Add a column with booleen value. True value for school holiday'''
        shd = SchoolHolidayDates()
        for ind_r, values_r in self.working_df.iterrows():
            if shd.is_holiday_for_zone(
                    values_r[c.NAMES["d"]],
                    c.TOWN_HOLIDAY_ZONE[values_r[c.NAMES["t"]]]
            ):
                self.working_df.at[ind_r, 'is_school_holiday'] = True
            else:
                self.working_df.at[ind_r, 'is_school_holiday'] = False

    def process_pipeline(self):
        '''Launch full processing pipeline'''
        self.add_sr_last_year()
        self.add_sr_last_year_weekday()
        self.add_weekday()
        self.add_is_weekend()
        self.add_is_bankholiday()
        self.add_distance_to_bankholiday()
        self.add_is_school_holiday()

    def export_data(self):
        '''Export custom DataFrane in a specidied folder'''
        cls = self.__class__
        self.working_df.to_csv(os.path.join(os.getcwd(), cls.export_df_name))

    def export_graph(self):
        '''Export graph representation of full custom DataFrame'''
        cls = self.__class__
        plot = sns.relplot(
            x=c.NAMES["d"], y=c.NAMES["s"], hue=c.NAMES["e"], style=c.NAMES["t"], kind="line",
            data=self.working_df
        )
        plot.savefig(os.path.join(os.getcwd(), cls.export_plot_name))

    def agg_graph(self):
        '''Export aggregate sales revenues graph representation'''
        cls = self.__class__
        plot = sns.relplot(
            x=c.NAMES["d"], y=c.NAMES["s"], hue=c.NAMES["e"], kind="line",
            data=self.group_df
        )
        plot.savefig(os.path.join(os.getcwd(), cls.export_agg))

    @classmethod
    def display_class_attributes(cls):
        '''Display class attributes values'''
        print(f"DataFrame are export under the name '{cls.export_df_name}'")
        print(f"Graphs are export under the name '{cls.export_plot_name}'")
        print(f"Weekday values are organized as follow '{cls.weekday}'")


def main():
    '''Launch main steps'''
    grd_w = Groundwork(os.path.join(os.getcwd(), c.FILE_NAME))
    grd_w_df = grd_w.process_pipeline()

    fc = Forecast(grd_w_df)
    fc.create_specific_df(c.CITIES_SELEC, c.EQUIP_SELEC)
    fc.agregate_sr()
    fc.process_pipeline()
    fc.export_data()
    fc.export_graph()

    return fc


if __name__ == "__main__":
    main()
