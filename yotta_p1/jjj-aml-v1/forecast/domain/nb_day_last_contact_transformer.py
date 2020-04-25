import datetime
from datetime import datetime as dt

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split

import forecast.settings.base as sg

class NbDayLastContactTransformer(BaseEstimator, TransformerMixin):
    """
    Add new columns related to the last contact.
    Methods
    -------
    fit
    transform
    _discretisation_NB_CONTACT_LAST_CAMPAIGN
    _add_CAT_CONTACT_LAST_CAMPAIGN
    _discretisation_NB_CONTACT
    _add_CAT_CONTACT
    """
    nb_month = 12

    def fit(self, X, y=None):
        """ 
        Fit method that return the object itself.
        Parameters
        ----------
        X: pandas.DataFrame
            Parameter not used in transformer fit method
        y: None, default None
            Parameter not used in transformer fit method
        Returns
        -------
        self: NbDayLastContactTransformer
        """
        return self

    def transform(self, X, y=None):
        """ 
        Transform method that return transformed DataFrame.
        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing the columns DATE and NB_DAY_LAST_CONTACT
        y: None, default None
            Parameter not used in transformer transform method
        Returns
        -------
        X: pandas.DataFrame
        """
        X_copy = X.copy()
        X_copy[sg.DATE_DATA] = X_copy[sg.DATE_DATA].astype('datetime64[ns]')
        X_copy = self._add_contacted_before(X_copy)
        month_last_contact, week_of_the_year_last_contact, gap_last_contact_month = self._add_new_columns(X_copy)
        X_add = self._concatenate_new_columns(X_copy, month_last_contact, week_of_the_year_last_contact, gap_last_contact_month)
        return X_add[sg.NB_DAY_LAST_CONTACT_COLS] 

    def get_feature_names(self):
        """ 
        Returns the created columns in a list.
        """
        return sg.NB_DAY_LAST_CONTACT_COLS

    def _add_new_columns(self, X):
        """ 
        Create the month_last_contact, week_of_the_year_last_contact and  gap_last_contact_month list
        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing the columns DATE_DATA and NB_DAY_LAST_CONTACT
        Returns
        -------
        X: pandas.DataFrame
        """
        month_last_contact = []
        week_of_the_year_last_contact = []
        gap_last_contact_month = []
        X_copy = X.copy()
        X_copy.index = range(X_copy.shape[0])

        for row in range(X_copy.shape[0]):

            if X_copy[sg.NB_DAY_LAST_CONTACT].iloc[row] == -1 or X_copy[sg.NB_DAY_LAST_CONTACT].iloc[row] == np.NaN:
                month_last_contact.append(0)
                week_of_the_year_last_contact.append(0)
                gap_last_contact_month.append(0)

            else:
                date = X_copy[sg.DATE_DATA].iloc[row]
                date_before = date - datetime.timedelta(days = int(X_copy[sg.NB_DAY_LAST_CONTACT].iloc[row]))

                month_last_contact.append(date_before.month)
                week_of_the_year_last_contact.append(date_before.isocalendar()[1])
                gap_last_contact_month.append((date.year - date_before.year) * self.nb_month + (date.month - date_before.month))
        
        return month_last_contact, week_of_the_year_last_contact, gap_last_contact_month

    def _concatenate_new_columns(self, X, month_last_contact, week_of_the_year_last_contact, gap_last_contact_month):
        """ 
        Create the month_last_contact, week_of_the_year_last_contact and  gap_last_contact_month columns
        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing the columns DATE_DATA and NB_DAY_LAST_CONTACT
        month_last_contact: list
            List containing the value of MONTH_LAST_CONTACT
        week_of_the_year_last_contact: list
            List containing the value of WEEK_LAST_CONTACT
        gap_last_contact_month: list
            List containing the value of GAP_IN_MONTH
        Returns
        -------
        X: pandas.DataFrame
        """
        X_copy = X.copy()
        INDEX = list(X_copy.index)

        series_month_last_contact = pd.Series(month_last_contact)
        series_month_last_contact.index = INDEX
        X_copy.loc[INDEX, sg.MONTH_LAST_CONTACT] = series_month_last_contact

        series_week_of_the_year_last_contact = pd.Series(week_of_the_year_last_contact)
        series_week_of_the_year_last_contact.index = INDEX
        X_copy.loc[INDEX, sg.WEEK_LAST_CONTACT] = series_week_of_the_year_last_contact

        series_gap_last_contact_month = pd.Series(gap_last_contact_month)
        series_gap_last_contact_month.index = INDEX
        X_copy.loc[INDEX, sg.GAP_IN_MONTH] = series_gap_last_contact_month
        return X_copy

    def _add_contacted_before(self, X):
        """ 
        Create the column CONTACTED_BEFORE.
        ----------
        X: pandas.DataFrame
            DataFrame containing the columns DATE_DATA and NB_DAY_LAST_CONTACT
        Returns
        -------
        X_copy: pandas.DataFrame
        """
        X_copy = X.copy()
        X_copy[sg.CONTACTED_BEFORE] = 0
        restricted_value = X_copy.query('{} > -1'.format(sg.NB_DAY_LAST_CONTACT))\
                                .assign(**{sg.CONTACTED_BEFORE : lambda x: 1}).copy()
        INDEX = list(restricted_value.index)
        X_copy.loc[INDEX, sg.CONTACTED_BEFORE] = restricted_value
        return X_copy


if __name__ == "__main__": 
    df, df_soc_eco = Load().Download()
    df.head()
    X = df.drop(columns = [sg.SUBSCRIPTION, sg.DURATION_CONTACT])
    y = df[sg.SUBSCRIPTION].astype("category").cat.codes
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    col_to_treat = [sg.DATE_DATA, sg.NB_DAY_LAST_CONTACT]
    df_treat = NbDayLastContactTransformer().fit_transform(X_train)
    df_treat.tail()
    df_treat['index'] = df_treat.index
    df_treat.query('index > {}'.format(X_train.shape[0]))
    df_treat.head()
    df_treat.isnull().sum()
    X_train.NB_DAY_LAST_CONTACT.value_counts()
    df_treat.CONTACTED_BEFORE.value_counts()

