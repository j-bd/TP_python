#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:53:40 2020

@author: j-bd
"""

FILE_NAME = "second_dataset.parquet"

NAMES = {"d": "DATE", "t": "TOWN", "e": "EQUIP", "s": "SALES"}

CITIES = {"mdm" : "Mont_Marsan", "p" : "Paris", "b" : "Bordeaux"}

DATE_FORMAT = {"csv" : "%Y-%m-%d", "parquet" : "%d%m%Y"}


# DO NOT MODIFY FOLLOWING VAR

COLUMNS_NAMES = {
    "Timestamp" : NAMES["d"], "date" : NAMES["d"], "Town" : NAMES["t"],
    "ville" : NAMES["t"], "Equipment" : NAMES["e"], "equipement" : NAMES["e"],
    "Sales" : NAMES["s"], "CA" : NAMES["s"]
}

CITIES_NAMES = {
    "Mont-de-Marsan" : CITIES["mdm"], "Mont de Marsan" : CITIES["mdm"]
}

STR_COLUMN = [NAMES["t"], NAMES["e"]]

NUMBER_COLUMN = [NAMES["s"]]

TOWN_HOLIDAY_ZONE = {"Bordeaux" : "A", CITIES["mdm"] : "A", "Paris" : "C"}


# TO BE MODIFY IN ACCORDANCE WITH REQUEST

CITIES_SELEC = [CITIES["mdm"], CITIES["b"]]

EQUIP_SELEC = ['ordinateur', 'telephone']


#DATE_FORMAT = '%Y-%m-%d'
#DATE_FORMAT = "%d%m%Y"



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