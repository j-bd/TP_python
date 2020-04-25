from forecast.infrastructure.Load import Load
import forecast.settings.base as sg

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class NbContactTransformer(BaseEstimator, TransformerMixin):
    """
    Discretization of NB_CONTACT and NB_CONTACT_LAST_CAMPAIGN
    Methods
    -------
    fit
    transform
    _discretisation_NB_CONTACT_LAST_CAMPAIGN
    _add_CAT_CONTACT_LAST_CAMPAIGN
    _discretisation_NB_CONTACT
    _add_CAT_CONTACT
    """
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
        self: NbContactTransformer
        """
        return self

    def transform(self, X, y=None):
        """ 
        Transform method that return transformed DataFrame.
        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing the columns NB_CONTACT and NB_CONTACT_LAST_CAMPAIGN
        y: None, default None
            Parameter not used in transformer transform method
        Returns
        -------
        X: pandas.DataFrame
        """
        X = self._add_CAT_CONTACT_LAST_CAMPAIGN(X)
        X = self._add_CAT_CONTACT(X)
        return X[['CAT_CONTACT_LAST_CAMPAIGN', 'CAT_CONTACT']]

    def get_feature_names(self):
        return ['CAT_CONTACT_LAST_CAMPAIGN', 'CAT_CONTACT']

    def _discretisation_NB_CONTACT_LAST_CAMPAIGN(self, row):
        """
        Method that discretize the column NB_CONTACT_LAST_CAMPAIGN
        Parameters
        ----------
        row: pandas.DataFrame
            DataFrame containing one row
        Returns
        -------
        str in function of the value
        """
        if row == 0:
            return 1
        elif row > 0 and row < 5:
            return 2
        elif row >= 5 and row < 11:
            return 3
        elif row >= 11 and row < 15:
            return 4
        elif row >= 15:
            return 5
        else:
            return np.NaN

    def _add_CAT_CONTACT_LAST_CAMPAIGN(self, X):
        """
        Method that aplly the discretization on the column NB_CONTACT_LAST_CAMPAIGN
        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing the columns NB_CONTACT and NB_CONTACT_LAST_CAMPAIGN
        Returns
        -------
        X: pandas.DataFrame
        """
        copy_X = X.copy()
        copy_X['CAT_CONTACT_LAST_CAMPAIGN'] = copy_X[sg.NB_CONTACT_LAST_CAMPAIGN].apply(lambda row: self._discretisation_NB_CONTACT_LAST_CAMPAIGN(row))
        copy_X = copy_X.drop(sg.NB_CONTACT_LAST_CAMPAIGN, axis=1)
        return copy_X

    def _discretisation_NB_CONTACT(self, row):
        """
        Method that discretize the column NB_CONTACT
        Parameters
        ----------
        row: pandas.DataFrame
            DataFrame containing one row
        Returns
        -------
        str in function of the value
        """
        if row == 1:
            return 1
        elif row > 1 and row < 4:
            return 2
        elif row >= 4 and row < 7:
            return 3
        elif row >= 11 and row < 15:
            return 4
        elif row >= 11:
            return 5
        else:
            return np.NaN

    def _add_CAT_CONTACT(self, X):
        """
        Method that aplly the discretization on the column NB_CONTACT
        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing the columns NB_CONTACT and NB_CONTACT_LAST_CAMPAIGN
        Returns
        -------
        X: pandas.DataFrame
        """
        copy_X = X.copy()
        copy_X['CAT_CONTACT'] = copy_X[sg.NB_CONTACT].apply(lambda row: self._discretisation_NB_CONTACT(row))
        copy_X = copy_X.drop(sg.NB_CONTACT,axis=1)
        return copy_X

if __name__ == "__main__": 
    df, df_soc_eco = Load().Download()
    df.head()
    col_to_treat = [sg.NB_CONTACT, sg.NB_CONTACT_LAST_CAMPAIGN]
    df_treat = NbContactTransformer().fit_transform(df[col_to_treat])
    df_treat.head()

    # add to train
    #nb_contact_transformer = Pipeline(steps=[
    #    ('transformer', NbContactTransformer()),
    #    ('imputer', SimpleImputer(missing_values= np.NaN, strategy='most_frequent')),
    #    ('label', MultiLabelEncoder(list(nb_contact_features)))])
