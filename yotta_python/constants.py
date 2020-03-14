#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:53:40 2020

@author: j-bd
"""

WORKING_DIR = "/home/latitude/Documents/Yotta/yotta_exs/yotta_python"

FILE_NAME = "initial_dataset.csv"

FEATURES_NAMES = [
    'date', 'ca', 'ca_last_year', 'ca_last_year_same_weekday', 'weekday',
    'is_weekend', 'is_bankholiday', 'distance_between_closest_bank_holiday',
    'is_school_holiday'
]

#FEATURES_TYPES = [date, int, int, int, str, bool, bool, int, bool]

TARGET_TOWNS = ["Bordeaux", "Mont de Marsan"]

YEARS_SELECTED = [2017, 2018, 2019]

