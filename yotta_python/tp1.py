#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:54:38 2020

@author: j-bd
"""

import os
import unicodedata

import pandas as pd
import datetime

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



