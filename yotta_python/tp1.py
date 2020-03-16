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


class Forecast:
    '''Allow to get information from sales report'''
    export_df_name = "processed_data_{equipement}_v1.csv"
    export_plot_name = "graph.png"
    weekday = {
        'lundi' : 'monday', 'mardi' : 'tuesday', 'mercredi' : 'wednesday',
        'jeudi' : 'thursday', 'vendredi' : 'friday', 'samedi' : 'saturday',
        'dimanche' : 'sunday'
    }

    def __init__(self, csv_path):
        '''Initialize class with original csv'''
        self.df_original = pd.read_csv(csv_path)

    def clean_data(self):
        '''Set date type and remove accent letters'''
        for line, val in enumerate(self.df_original.iloc[:, 0]):
            date_format = datetime.datetime.strptime(val, c.DATE_FORMAT).date()
            self.df_original.iloc[line, 0] = date_format

        for line, val in enumerate(self.df_original.iloc[:, 1]):
            word = unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode()
            self.df_original.iloc[line, 1] = word

    def create_specific_df(self, town_list, equipement_list):
        '''Return a custom dataframe based on columns contains user choice'''
        init_df = pd.DataFrame(columns=self.df_original.columns)
        for value in town_list:
            filter_df = self.df_original[self.df_original.loc[:, 'ville'] == value]
            frames = [init_df, filter_df]
            init_df = pd.concat(frames)

        second_df = pd.DataFrame(columns=self.df_original.columns)
        for value in equipement_list:
            filter_df = init_df[init_df.loc[:, 'equipement'] == value]
            frames = [second_df, filter_df]
            second_df = pd.concat(frames)

        self.working_df = second_df.reset_index(drop=True)
        return self.working_df

    def add_sr_last_year(self):
        '''Add a column with the sales revenue of one year before for each day'''
        for ind_r, values_r in self.working_df.iterrows():
            sr_l_y = self.working_df.loc[
                (self.working_df["ville"] == values_r["ville"]) &
                (self.working_df["equipement"] == values_r["equipement"]) &
                (self.working_df["date"] == values_r["date"] - relativedelta(years=1)),
                "CA"
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
                (self.working_df["ville"] == values_r["ville"]) &
                (self.working_df["equipement"] == values_r["equipement"]) &
                (self.working_df["date"] == values_r["date"] +
                 relativedelta(years=-1, weekday=values_r["date"].weekday())),
                "CA"
            ]
            try:
                self.working_df.at[ind_r, 'ca_last_year_same_weekday'] = float(sr_l_y_sw)
            except TypeError:
                self.working_df.at[ind_r, 'ca_last_year_same_weekday'] = "Nan"

    def add_weekday(self):
        '''Add a column with the weekday corresponding to the date'''
        cls = self.__class__
        for ind_r, values_r in self.working_df.iterrows():
            day = self.working_df.loc[ind_r, "date"].strftime("%A")
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
            if self.working_df.loc[ind_r, "date"].year != year:
                year = self.working_df.loc[ind_r, "date"].year
                bankholiday = list(JoursFeries.for_year(year).values())

            if self.working_df.loc[ind_r, "date"] in bankholiday:
                self.working_df.at[ind_r, 'is_bankholiday'] = True
            else:
                self.working_df.at[ind_r, 'is_bankholiday'] = False

    def add_distance_to_bankholiday(self):
        '''Add a column with booleen value. True value for bankholiday'''
        year = 0
        bankholiday = []
        for ind_r, values_r in self.working_df.iterrows():
            if self.working_df.loc[ind_r, "date"].year != year:
                year = self.working_df.loc[ind_r, "date"].year
                bankholiday = list(JoursFeries.for_year(year).values())

            for bhd in bankholiday:
                if bhd > self.working_df.loc[ind_r, "date"]:
                    self.working_df.at[ind_r, 'dist_between_closest_bank_holiday'] = bhd - self.working_df.loc[ind_r, "date"]
                    break

    def add_is_school_holiday(self):
        '''Add a column with booleen value. True value for school holiday'''
        shd = SchoolHolidayDates()
        for ind_r, values_r in self.working_df.iterrows():
            if shd.is_holiday_for_zone(values_r["date"], c.TOWN_HOLIDAY_ZONE[values_r["ville"]]):
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
        '''Export graph representation of custom DataFrame'''
        cls = self.__class__
        plot = sns.relplot(
            x="date", y="CA", hue="equipement", style="ville", kind="line",
            data=self.working_df
        )
        plot.savefig(os.path.join(os.getcwd(), cls.export_plot_name))

    @classmethod
    def display_class_attributes(cls):
        '''Display class attributes values'''
        print(f"DataFrame are export under the name '{cls.export_df_name}'")
        print(f"Graphs are export under the name '{cls.export_plot_name}'")
        print(f"Weekday values are organized as follow '{cls.weekday}'")


def main(town_list, equip_list):
    '''Launch main steps'''
    fc = Forecast(os.path.join(os.getcwd(), c.FILE_NAME))
    fc.clean_data()
    fc.create_specific_df(town_list, equip_list)
    fc.process_pipeline()
    fc.export_data()
    fc.export_graph()

    return fc


if __name__ == "__main__":
    town_select = ['Mont de Marsan', 'Bordeaux']
    equip_select = ['ordinateur', 'telephone']
    forecast = main(town_select, equip_select)
