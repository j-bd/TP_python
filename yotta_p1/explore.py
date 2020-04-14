#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:03:02 2020

@author: j-bd
"""

import os
import calendar
from datetime import datetime

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer


path = "/home/latitude/Documents/Yotta/yotta_exs/yotta_p1/data"

DATA = os.path.join(path, "data.csv")
SOCIO = os.path.join(path, "socio_eco.csv")

df_data = pd.read_csv(DATA)
df_socio = pd.read_csv(SOCIO)

# =============================================================================
# Overview
# =============================================================================
print(df_data.shape)
print(df_data.describe())
print(df_data.info())
print(df_data.columns)
print(df_data.isnull().sum(axis=0) *100 / len(df_data))
print(df_data.head())
print(df_data.nunique(dropna = False))


# =============================================================================
# Clean data
# =============================================================================

df_data.drop(columns=["DATE", "DURATION_CONTACT", "RESULT_LAST_CAMPAIGN", "CONTACT"], inplace=True)

numeric_variables = list(df_data.select_dtypes(include=['int64', 'float64']))
cat_variables = list(df_data.select_dtypes(include=[object]).drop(['SUBSCRIPTION'], axis=1))

# =============================================================================
# Visualisation
# =============================================================================
df_data.skew()
df_data.kurtosis()
numeric_variables_variance = numeric_variables.var()
print(numeric_variables_variance)

# univariee quantitative
for col in numeric_variables:
    plt.figure()
    graph = sns.countplot(x=col, hue='SUBSCRIPTION', data=df_data)
    graph.set_yscale("log")


# multivarie quantitative avec quantitative
sns.pairplot(df_data, hue='SUBSCRIPTION')
df_data.plotting.scatter_matrix() # method : {‘pearson’, ‘kendall’, ‘spearman’}


#univariee qualitative
for col in cat_variables:
    plt.figure()
    graph = sns.countplot(x=col, hue='SUBSCRIPTION', data=df_data)
    graph.set_yscale("log")


# multivarie qualitative avec quantitative
for cat in cat_variables:
    for num in numeric_variables:
        plt.figure()
        sns.boxplot(x=num, y=cat, data=df_data)


sns.heatmap(df_data.corr(), nominal_columns=cat_variables.columns, annot=True)


# =============================================================================
# Variable Date
# =============================================================================
#df_data["weekday"] = df_data.DATE.apply(
#    lambda dateString : calendar.day_name[datetime.strptime(dateString,"%Y-%m-%d").weekday()]
#)
#df_data["month"] = df_data.DATE.apply(
#    lambda dateString : calendar.month_name[datetime.strptime(dateString,"%Y-%m-%d").month]
#)
df_data['DATE'] = pd.to_datetime(df_data['DATE'], format='%Y-%m-%d')
df_data["day"] = df_data['DATE'].dt.day
df_data["weekday"] = df_data['DATE'].dt.day_name()
df_data["month"] = df_data['DATE'].dt.month_name()
data_col = ["weekday", "month"]
sort_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]
hue_order = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
df_data['SUB_NUM'] = pd.get_dummies(df_data['SUBSCRIPTION'], drop_first=True)

for col in data_col:
    df_data[col] = df_data[col].astype("category")

for col in data_col:
    plt.figure()
    graph = sns.countplot(x=col, hue='SUBSCRIPTION', data=df_data)
    graph.set_yscale("log")

fig,(ax1,ax2)= plt.subplots(nrows=2)
fig.set_size_inches(16,22)

#monthAggregated = pd.DataFrame(dailyData.groupby("month")["rented"].mean()).reset_index()
#monthSorted = monthAggregated.sort_values(by="rented",ascending=False)
#sn.barplot(data=monthSorted,x="month",y="rented",ax=ax1,order=sortOrder)
#ax1.set(xlabel='Month', ylabel='Avearage Rented',title="Average Rount By Month")

day_aggregated = pd.DataFrame(df_data.groupby(["day","month"],sort=True)["SUB_NUM"].sum()).reset_index()
sns.pointplot(x=day_aggregated["day"], y=day_aggregated["SUB_NUM"],hue=day_aggregated["month"], hue_order=sort_order, data=day_aggregated, join=True,ax=ax1)
ax1.set(xlabel='Days', ylabel='SUB_NUM',title="Average By Day Across month")
plt.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), ncol=1)

day_aggregated = pd.DataFrame(df_data.groupby(["day","weekday"],sort=True)["SUB_NUM"].sum()).reset_index()
sns.pointplot(x=day_aggregated["day"], y=day_aggregated["SUB_NUM"],hue=day_aggregated["weekday"],hue_order=hue_order, data=day_aggregated, join=True,ax=ax2)
ax2.set(xlabel='Days', ylabel='SUB_NUM',title="Average By Day Across Weekdays",label='big')



#df_data['SUB_NUM'] = pd.get_dummies(df_data['SUBSCRIPTION'], drop_first=True)
#df_data['SUB_NUM'] = df_data['SUB_NUM'].astype("int64")
#for col in data_col:
#    plt.figure()
#    sns.boxplot(x=col, y='SUB_NUM', data=df_data)
#    graph.set_yscale("log")
#sn.boxplot(data=dailyDataWithoutOutliers,y="rented",x="season",orient="v",ax=axes[0][1])

# =============================================================================
# Valeurs aberrantes
# =============================================================================
df_data.shape
for col in df_data.select_dtypes(include=[np.number]).columns:
    df_data = df_data[
            np.abs(df_data[col] - df_data[col].mean()) <= (3 * df_data[col].std())
    ]
df_data.shape
print(df_data.info())

# =============================================================================
# Train test split
# =============================================================================
ys = df_data['SUBSCRIPTION']
xs = df_data.drop(columns='SUBSCRIPTION')

x_train, x_test, y_train, y_test = train_test_split(
    xs, ys, test_size=0.2, random_state=42, stratify=ys
)


# =============================================================================
# Transformation des donnees
# =============================================================================
print(x_train.isnull().sum(axis=0) *100 / len(df_data))
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', MinMaxScaler())])
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])


preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_variables),
        ('cat', categorical_transformer, cat_variables)
    ]
)



# =============================================================================
#Pipeline and grid search
# =============================================================================
pca = PCA(whiten=True, random_state=42)
svc = SVC(kernel='rbf', class_weight='balanced')
#model = make_pipeline(preprocessor, pca, svc)
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('pca', pca),
                      ('svc', svc)])

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
param_grid = {
    'pca__n_components': [5, 13],
    'svc__C': [1, ],
    'svc__gamma': [0.0001, 0.001]}
grid = GridSearchCV(model, param_grid, n_jobs=-1, cv=skf)

y_train = pd.get_dummies(y_train, drop_first=True)

#%time grid.fit(x_train, y_train)
print(grid.get_params)
print(grid.best_params_)

model = grid.best_estimator_
y_pred = model.predict(x_test)

# =============================================================================
# Prediction
# =============================================================================

#x_test = pd.get_dummies(x_test, drop_first=True)
y_test = pd.get_dummies(y_test, drop_first=True)
#
#x_test = scaler.fit_transform(x_test)

#y_pred = classifier_trained.predict(x_test)


# =============================================================================
# Estimation de performance
# =============================================================================

# calculate precision-recall curve
precision, recall, thresholds = precision_recall_curve(y_test, y_pred)

# calculate F1 score
f1 = f1_score(y_test, y_pred)

# calculate precision-recall AUC
pr_auc = auc(recall, precision)

# calculate average precision score
ap = average_precision_score(y_test, y_pred)
print('f1=%.3f auc=%.3f ap=%.3f' % (f1, pr_auc, ap))
# plot no skill
plt.plot([0, 1], [0.5, 0.5], linestyle='--')
# plot the precision-recall curve for the model
plt.plot(recall, precision, marker='.')
# show the plot
plt.show()

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm,annot=True)
#classifier_trained.score(x_test, y_test)
#
#ys_rate = pd.get_dummies(ys, drop_first=True)
#print(f"Taux d'acceptation sur l'ensemble du dataset: {1 - ys_rate.sum() / len(df_data)}"\
#    f"Taux predit : {classifier_trained.score(x_test, y_test)}")

ys_rate = pd.get_dummies(ys, drop_first=True)
print(f"Taux d'acceptation sur l'ensemble du dataset: {1 - ys_rate.sum() / len(df_data)}"\
    f"Taux predit : {model.score(x_test, y_test)}")
