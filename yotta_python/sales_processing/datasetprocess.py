#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:54:10 2020

@author: j-bd
"""

import os

import pandas as pd
import seaborn as sns
import numpy as np
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from jours_feries_france.compute import JoursFeries
from vacances_scolaires_france import SchoolHolidayDates

import constants as c


class DataframeFilter:
    """Provide sub-dataframe"""
    def __init__(self, df):
        """Initialize class with dataframe"""
        self.df = df
        self._create_specific_df()

    def _create_specific_df(self):
        """Return a custom dataframe based on columns contains user choice in constants.py"""
        self.sub_df = self.df.query(
            f"{c.COL_KEY['equip']} in @c.EQUIP_SELEC and {c.COL_KEY['town']} in @c.CITIES_SELEC"
        )
        self.sub_df = self.sub_df.reset_index(drop=True)
        return self.sub_df


class DataSelection:
    """Return an aggregate DataFrame and export graph of aggregate data"""
    def __init__(self, df):
        """Initialize class with dataframe"""
        self.df = df
        self.export_agg = f"{'_'.join(c.EQUIP_SELEC)}-agg_graph.png"

    def aggregate_data(self,group_list, freq=None):
        """Aggregate Sales Revenue for cities and equipment selected by month"""
        self.aggregate_df = self.df.set_index(
            pd.DatetimeIndex(self.df[c.COL_KEY["date"]])
        )

        if freq:
            group_list.append(pd.Grouper(freq=freq))

        self.aggregate_df = self.aggregate_df.groupby(group_list).sum()
        self.aggregate_df.reset_index(inplace=True)
        self._create_graph()

    def _create_graph(self):
        """Export aggregate sales revenues graph representation"""
        plot = sns.relplot(
            x=c.COL_KEY["date"], y=c.COL_KEY["sales"], hue=c.COL_KEY["equip"],
            kind="line", data=self.aggregate_df
        )
        plot.savefig(os.path.join(os.getcwd(), self.export_agg))


class SalesRevenue:
    """Add columns of past Sales Revenue information"""
    RELATIVE_WEEKDAY = {0 : MO, 1 : TU, 2 : WE, 3 : TH, 4 :FR, 5 : SA, 6 : SU}

    def __init__(self, df):
        """Initialize class with dataframe"""
        self.df = df

    @property
    def provide_past_figures(self):
        """Lauch full process"""
        self._add_sales_revenue_last_year()
        self._add_sales_revenue_last_year_weekday()
        return self.df

    def _add_sales_revenue_last_year(self):
        """Add a column with the sales revenue of one year before for each day"""
        self._retrieve_past_value(
            c.YEAR_STEP_BACKWARD, 'sr_last_year', c.COL_KEY["sales"]
        )

    def _add_sales_revenue_last_year_weekday(self):
        """Add a column with the sales revenue of one year before for each day
        and linked to the same weekday"""
        self._retrieve_past_value(
            c.YEAR_STEP_BACKWARD, 'sr_last_year_same_weekday', c.COL_KEY["sales"], True
        )

    def _retrieve_past_value(self, year_step, new_column_name, column_reported, weekday_act=False):
        """Add a column with the backward value of the column watched"""
        for row_idx, row_value in self.df.iterrows():
            if weekday_act:
                weekd = self.RELATIVE_WEEKDAY[row_value[c.COL_KEY["date"]].weekday()]
            else:
                weekd = None
            town_selection = (
                self.df[c.COL_KEY["town"]] == row_value[c.COL_KEY["town"]]
            )
            equipment_selection = (
                self.df[c.COL_KEY["equip"]] == row_value[c.COL_KEY["equip"]]
            )
            previous_date_selection = (
                self.df[c.COL_KEY["date"]] == row_value[c.COL_KEY["date"]] +
                relativedelta(years=year_step, weekday=weekd)
            )
            previous_value = self.df.loc[
                 (town_selection & equipment_selection & previous_date_selection),
                 column_reported
            ]
            try:
                self.df.at[row_idx, new_column_name] = float(
                    previous_value.values
                )
            except TypeError:
                self.df.at[row_idx, new_column_name] = np.nan


class CalendarInformation:
    """Add columns with calendar information such days and holidays"""
    WEEKDAY = {
        'lundi' : 'monday', 'mardi' : 'tuesday', 'mercredi' : 'wednesday',
        'jeudi' : 'thursday', 'vendredi' : 'friday', 'samedi' : 'saturday',
        'dimanche' : 'sunday'
    }

    def __init__(self, df):
        """Initialize class with dataframe"""
        self.df = df

    @property
    def provide_calendar_information(self):
        """Lauch full process"""
        self._add_weekday()
        self._add_is_weekend()
        self._add_is_bankholiday()
        self._add_distance_to_bankholiday()
        self._add_is_school_holiday()
        return self.df

    def _add_weekday(self):
        """Add a column with the weekday corresponding to the date"""
        for row_idx, row_value in self.df.iterrows():
            day = self.df.loc[row_idx, c.COL_KEY["date"]].strftime("%A")
            try:
                self.df.at[row_idx, 'weekday'] = self.WEEKDAY[day]
            except KeyError:
                self.df.at[row_idx, 'weekday'] = day

    def _add_is_weekend(self):
        """Add a column with booleen value. True value for weekend"""
        for row_idx, row_value in self.df.iterrows():
            if self.df.loc[row_idx, "weekday"] in ['saturday', 'sunday']:
                self.df.at[row_idx, 'is weekend'] = True
            else:
                self.df.at[row_idx, 'is weekend'] = False

    def _add_is_bankholiday(self):
        """Add a column with booleen value. True value for bankholiday"""
        year = 0
        bankholiday = []
        for row_idx, row_value in self.df.iterrows():
            if self.df.loc[row_idx, c.COL_KEY["date"]].year != year:
                year = self.df.loc[row_idx, c.COL_KEY["date"]].year
                bankholiday = list(JoursFeries.for_year(year).values())

            if self.df.loc[row_idx, c.COL_KEY["date"]] in bankholiday:
                self.df.at[row_idx, 'is_bankholiday'] = True
            else:
                self.df.at[row_idx, 'is_bankholiday'] = False

    def _add_distance_to_bankholiday(self):
        """Add a column with booleen value. True value for bankholiday"""
        year = 0
        bankholiday = []
        for row_idx, row_value in self.df.iterrows():
            if self.df.loc[row_idx, c.COL_KEY["date"]].year != year:
                year = self.df.loc[row_idx, c.COL_KEY["date"]].year
                bankholiday = list(JoursFeries.for_year(year).values())

            for bhd in bankholiday:
                if bhd > self.df.loc[row_idx, c.COL_KEY["date"]]:
                    self.df.at[
                        row_idx, 'dist_between_closest_bank_holiday'
                    ] = bhd - self.df.loc[row_idx, c.COL_KEY["date"]]
                    break

    def _add_is_school_holiday(self):
        """Add a column with booleen value. True value for school holiday"""
        school_holiday_date = SchoolHolidayDates()
        for row_idx, row_value in self.df.iterrows():
            if school_holiday_date.is_holiday_for_zone(
                    row_value[c.COL_KEY["date"]],
                    c.TOWN_HOLIDAY_ZONE[row_value[c.COL_KEY["town"]]]
            ):
                self.df.at[row_idx, 'is_school_holiday'] = True
            else:
                self.df.at[row_idx, 'is_school_holiday'] = False

def export_data(df):
    """Export custom DataFrane in a specidied folder"""
    export_df_name = f"processed_data_{'_'.join(c.EQUIP_SELEC)}_v1-{'_'.join(c.CITIES_SELEC)}.csv"
    df.to_csv(os.path.join(os.getcwd(), export_df_name))
