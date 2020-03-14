#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:54:38 2020

@author: j-bd
"""

import os

import pandas as pd

import constants as c


def csv_loader(path):
    '''Load a csv file and return a pandas dataset'''
    return pd.read_csv(path)



df = csv_loader(os.path.join(c.WORKING_DIR, c.FILE_NAME))
