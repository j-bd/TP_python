#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:49:47 2020

@author: j-bd
"""
import os

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
import shap
shap.initjs()

from forecast.infrastructure.preprocessing import Preprocessing
import forecast.settings as stg
import forecast.domain.model_evaluation as me


#path = "/home/latitude/Documents/Yotta/2-Data_Science/Project_1-Advanced_ML/v1/jjj-aml/data/interim/data_socio_merged.csv"
#df_data = pd.read_csv(path)

data = '/home/latitude/Documents/Yotta/2-Data_Science/Project_1-Advanced_ML/v1/jjj-aml/data/raw/data.csv'
socio = '/home/latitude/Documents/Yotta/2-Data_Science/Project_1-Advanced_ML/v1/jjj-aml/data/raw/socio_eco.csv'

model_path = '/home/latitude/Documents/Yotta/2-Data_Science/Project_1-Advanced_ML/v1/jjj-aml/models/model.joblib'
loaded_model = joblib.load(model_path)



preprocessing = Preprocessing(data, socio, predict=False)
preprocessing.do_preprocessing()

# Get features and target
X, y = preprocessing.get_features_target()

# Train test splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

step_prep = loaded_model['preprocessor']
step_model = loaded_model['model']

#X_transformed = step_prep.fit_transform(X_train)
X_test_transformed = step_prep.transform(X_test)
#X_resampled, y_resampled = OverSampler(
#        method="random", inactive=False).fit_resample(X_transformed, y_train)


explanation = shap.TreeExplainer(step_model)
shap_values = explanation.shap_values(X_test_transformed)
df_contrib = pd.DataFrame(shap_values, columns=X_test_transformed.columns, index=X_test_transformed.index)
bias = explanation.expected_value[1]

#
cols = me.get_transformer_feature_names(loaded_model.steps[0][1])

X_test_transformed_pd = pd.DataFrame(X_test_transformed, columns=cols)

#df_contrib = pd.DataFrame(shap_values, columns=X_test_transformed_pd.columns, index=X_test_transformed_pd.index)
#bias = explanation.expected_value[1]

index = 9
fp = shap.force_plot(explanation.expected_value, shap_values[index, :], X_test_transformed_pd.iloc[index, :])
fp_h = fp.data
with open('/home/latitude/Downloads/pl.html','wb') as f:   # Use some reasonable temp name
    f.write(fp)


shap.force_plot(explanation.expected_value, shap_values, X_test_transformed_pd)

shap.summary_plot(shap_values, X_test_transformed_pd, plot_type="dot")

shap.summary_plot(shap_values, X_test_transformed_pd, plot_type="bar")

shap.initjs()
pl = shap.force_plot(explanation.expected_value, shap_values[0,:], X_test_transformed_pd.iloc[0,:])

with open('/home/latitude/Downloads/pl.htm','wb') as f:   # Use some reasonable temp name
    f.write(pl.html.encode("UTF-8"))
