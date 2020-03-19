#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:53:40 2020

@author: j-bd
"""

import os

INPUT_FILE_NAME = os.path.join(os.getcwd(), "initial_dataset.csv")

COL_KEY = {"date": "DATE", "town": "TOWN", "equip": "EQUIP", "sales": "SALES"}

CITIES_KEY = {
    "mont_marsan" : "Mont_Marsan", "paris" : "Paris", "bordeaux" : "Bordeaux"
}

DATE_FORMAT = {"csv" : "%Y-%m-%d", "parquet" : "%d%m%Y"}

COLUMNS_NAMES_VARIATION = {
    "Timestamp" : COL_KEY["date"], "date" : COL_KEY["date"],
    "Town" : COL_KEY["town"], "ville" : COL_KEY["town"],
    "Equipment" : COL_KEY["equip"], "equipement" : COL_KEY["equip"],
    "Sales" : COL_KEY["sales"], "CA" : COL_KEY["sales"]
}

CITIES_NAMES_VARIATION = {
    "Mont-de-Marsan" : CITIES_KEY["mont_marsan"], "Mont de Marsan" : CITIES_KEY["mont_marsan"]
}

COL_STR_FORMAT = [COL_KEY["town"], COL_KEY["equip"]]

COL_NUMBER_FORMAT = [COL_KEY["sales"]]

TOWN_HOLIDAY_ZONE = {
    CITIES_KEY["bordeaux"] : "A", CITIES_KEY["mont_marsan"] : "A",
    CITIES_KEY["paris"] : "C"
}


# TO BE MODIFIED IN ACCORDANCE WITH REQUEST

CITIES_SELEC = [CITIES_KEY["mont_marsan"], CITIES_KEY["bordeaux"]]

EQUIP_SELEC = ['ordinateur', 'telephone']

YEAR_STEP_BACKWARD = 1
