#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:53:40 2020

@author: j-bd
"""

FILE_NAME = "second_dataset.parquet"

#DATE_FORMAT = '%Y-%m-%d'
#DATE_FORMAT = "%d%m%Y"

TOWN_HOLIDAY_ZONE = {"Bordeaux" : "A", "Mont_Marsan" : "A", "Paris" : "C"}

#DATE = "Timestamp"
#TOWN = "Town"
#EQUIP = "Equipment"
#SALES = "Sales"

#Request format

#base = {
#    "zone" : {
#        "Bordeaux" : "A", "Mont-de-Marsan" : "A", "Paris" : "C",
#        "Mont de Marsan" : "A"
#    },
#    "date_format" : {"ymd" : "%Y-%m-%d", "dmy" : "%d%m%Y"},
#    "column_format" : {
#        "Timestamp" : "date", "date" : "date", "Town" : "town", "ville" : "town",
#        "Equipment" : "equip", "equipement" : "equip", "Sales" : "sales",
#        "CA" : "sales"
#    }
#}

NAMES = {"d": "DATE", "t": "TOWN", "e": "EQUIP", "s": "SALES"}

COLUMNS_NAMES = {
    "Timestamp" : NAMES["d"], "date" : NAMES["d"], "Town" : NAMES["t"],
    "ville" : NAMES["t"], "Equipment" : NAMES["e"], "equipement" : NAMES["e"],
    "Sales" : NAMES["s"], "CA" : NAMES["s"]
}

CITIES_NAMES = {
    "Paris" : ["Paris"], "Bordeaux" : ["Bordeaux"],
    "Mont_Marsan" : ["Mont-de-Marsan", "Mont de Marsan"]
}

DATE_FORMAT = {"csv" : "%Y-%m-%d", "parquet" : "%d%m%Y"}


#result = {"date_format" : "%Y-%m-%d", "date_col" : "Timestamp",
#    "town_col" : "Town", "equip_col" : "Equipment", "sales_col" : "Sales"
#}

#    "date_col" : ["Timestamp", "date"], "equip_col" : ["Equipment", "equipement"],
#    "town_col" : ["Town", "ville"],"sales_col" : ["Sales", "CA"]

#columns_name = {}
#for column_name in list(df.columns):
#    for key, value in dictionary.items():
#        if column_name in value:
#            columns_name[key] = column_name