from forecast.infrastructure.Load import Load
import forecast.settings.base as sg
import datetime
from datetime import datetime as dt
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split


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
        month_last_contact, week_of_the_year_last_contact, gap_last_contact_month = self.add_new_columns(X_copy)
        X_add = self.concatenate_new_columns(X_copy, month_last_contact, week_of_the_year_last_contact, gap_last_contact_month)
        return X_add[[sg.MONTH_LAST_CONTACT, sg.WEEK_LAST_CONTACT, sg.GAP_IN_MONTH]] # sg.WEEK_LAST_CONTACT pas forcément utile à voir

    def get_feature_names(self):
        return [sg.MONTH_LAST_CONTACT, sg.WEEK_LAST_CONTACT, sg.GAP_IN_MONTH]

    def add_new_columns(self, X):
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

    def concatenate_new_columns(self, X, month_last_contact, week_of_the_year_last_contact, gap_last_contact_month):
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


