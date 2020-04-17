#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:04:48 2020

@author: j-bd
"""

import pandas as pd
import numpy as np
import seaborn as sns

path = "/home/latitude/Documents/Yotta/2-Data_Science/1-Machine_Learning/TP/2-TP_Dimensionality_Reduction/data/applications.csv"

df_pb = pd.read_csv(path)

for col_name in df_pb.columns:
    df_pb[col_name] = df_pb.fillna(df_pb[col_name].mode()[0])

var = df_pb.var()



null = df_pb.isnull().sum() * 100 / len(df_pb)
col_list = [idx for idx, val in null.iteritems() if val >= 60]
df_pb = df_pb.drop(columns=col_list)


xs = df_pb.drop(columns="TARGET")
y = df_pb["TARGET"]


# Compute the correlation matrix
corr = xs.corr()
# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=np.bool))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

