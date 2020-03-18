#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:53:40 2020

@author: j-bd
"""

FILE_NAME = "initial_dataset.csv"

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
