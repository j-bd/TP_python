#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:54:38 2020

@author: j-bd
"""

import os
import unicodedata
import datetime
import calendar

import pandas as pd
from dateutil.relativedelta import relativedelta
from jours_feries_france.compute import JoursFeries
from vacances_scolaires_france import SchoolHolidayDates

import constants as c


def csv_loader(path):
    '''Load a csv file and return a pandas dataset'''
    return pd.read_csv(path)

def specific_df(df, town_list, equipement_list):
    '''Return a custom dataframe based on columns contains user choice'''
    init_df = pd.DataFrame(columns=df.columns)
    for value in town_list:
        filter_df = df[df.loc[:, 'ville'] == value]
        frames = [init_df, filter_df]
        init_df = pd.concat(frames)

    second_df = pd.DataFrame(columns=df.columns)
    for value in equipement_list:
        filter_df = init_df[init_df.loc[:, 'equipement'] == value]
        frames = [second_df, filter_df]
        second_df = pd.concat(frames)
    return second_df.reset_index(drop=True)


#Data Preparation and selection
df_original = csv_loader(os.path.join(c.WORKING_DIR, c.FILE_NAME))

for line, val in enumerate(df_original.iloc[:, 0]):
    date_format = datetime.datetime.strptime(val, '%Y-%m-%d').date()
    df_original.iloc[line, 0] = date_format

for line, val in enumerate(df_original.iloc[:, 1]):
    word = unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode()
    df_original.iloc[line, 1] = word

town_select = ['Mont de Marsan', 'Bordeaux']
equip_select = ['ordinateur', 'telephone']

working_df = specific_df(df_original, town_select, equip_select)


#Data addition

#ca last year
for ind_r, values_r in working_df.iterrows():
    ca_l_y = working_df.loc[
        (working_df["ville"] == values_r["ville"]) &
        (working_df["equipement"] == values_r["equipement"]) &
        (working_df["date"] == values_r["date"] - relativedelta(years=1)), "CA"
    ]

    try:
        working_df.at[ind_r, 'ca_last_year'] = float(ca_l_y.values)
    except TypeError:
        working_df.at[ind_r, 'ca_last_year'] = "Nan"

#ca last year same weekday
for ind_r, values_r in working_df.iterrows():
    ca_l_y_sw = working_df.loc[
        (working_df["ville"] == values_r["ville"]) &
        (working_df["equipement"] == values_r["equipement"]) &
        (working_df["date"] == values_r["date"] + relativedelta(years=-1, weekday=values_r["date"].weekday())),
        "CA"
    ]

    try:
        working_df.at[ind_r, 'ca_last_year_same_weekday'] = float(ca_l_y_sw)
    except TypeError:
        working_df.at[ind_r, 'ca_last_year_same_weekday'] = "Nan"

relativedelta(years=+1, months=-1)
#weekday
for ind_r, values_r in working_df.iterrows():
    day = working_df.loc[ind_r, "date"].strftime("%A")
    working_df.at[ind_r, 'weekday'] = c.WEEKDAY[day]

#weekend
for ind_r, values_r in working_df.iterrows():
    if working_df.loc[ind_r, "weekday"] in ['saturday', 'sunday']:
        working_df.at[ind_r, 'is weekend'] = True
    else:
        working_df.at[ind_r, 'is weekend'] = False

#is bankholiday
year = 0
bankholiday = []
for ind_r, values_r in working_df.iterrows():
    if working_df.loc[ind_r, "date"].year != year:
        year = working_df.loc[ind_r, "date"].year
        bankholiday = list(JoursFeries.for_year(year).values())

    if working_df.loc[ind_r, "date"] in bankholiday:
        working_df.at[ind_r, 'is_bankholiday'] = True
    else:
        working_df.at[ind_r, 'is_bankholiday'] = False

#distance between closest bank holiday
year = 0
bankholiday = []
for ind_r, values_r in working_df.iterrows():
    if working_df.loc[ind_r, "date"].year != year:
        year = working_df.loc[ind_r, "date"].year
        bankholiday = list(JoursFeries.for_year(year).values())

    for bhd in bankholiday:
        if bhd > working_df.loc[ind_r, "date"]:
            working_df.at[ind_r, 'dist_between_closest_bank_holiday'] = bhd - working_df.loc[ind_r, "date"]
            break

#is school holiday
d = SchoolHolidayDates()
for ind_r, values_r in working_df.iterrows():
    if d.is_holiday_for_zone(values_r["date"], c.TOWN_HOLIDAY_ZONE[values_r["ville"]]):
        working_df.at[ind_r, 'is_school_holiday'] = True
    else:
        working_df.at[ind_r, 'is_school_holiday'] = False


#a.strftime("%A")
targ_date = datetime.date(2020, 3, 15)
