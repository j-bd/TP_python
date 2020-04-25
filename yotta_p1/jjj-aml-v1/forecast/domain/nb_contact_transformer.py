import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

import forecast.settings.base as sg

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
    def __init__(self, pow_NB_CONTACT, pow_NB_CONTACT_LC, pow_CROSS):
        self.pow_NB_CONTACT = pow_NB_CONTACT
        self.pow_NB_CONTACT_LC = pow_NB_CONTACT_LC
        self.pow_CROSS = pow_CROSS

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
        X[sg.CROSS_CONTACT] = X[sg.CAT_CONTACT] * X[sg.CAT_CONTACT_LAST_CAMPAIGN]
        X[sg.CROSS_CONTACT] = X[sg.CROSS_CONTACT].apply(lambda row: row*self.pow_CROSS)
        X[sg.CAT_CONTACT] = X[sg.CAT_CONTACT].apply(lambda row: row*self.pow_NB_CONTACT)
        X[sg.CAT_CONTACT_LAST_CAMPAIGN] = X[sg.CAT_CONTACT_LAST_CAMPAIGN].apply(lambda row: row*self.pow_NB_CONTACT_LC)
        return X[sg.CONTACT_COLS] 

    def get_feature_names(self):
        """
        Get the names of the features used in the model
        """
        return sg.CONTACT_COLS 

    def _discretisation_NB_CONTACT_LAST_CAMPAIGN(self, row):
        """
        Method that discretize the column NB_CONTACT_LAST_CAMPAIGN
        Parameters
        ----------
        row: int value
            One value from the column NB_CONTACT_LAST_CAMPAIGN
        Returns
        -------
        str in function of the value
        """
        if row == 0:
            return 1#'Not contacted'
        elif row > 0 and row < 5:
            return 2#'Between 1 and 4 call'
        elif row >= 5 and row < 11:
            return 4#'Between 5 and 10 call'
        elif row >= 11 and row < 15:
            return 3#'Between 10 and 14 call'
        elif row >= 15:
            return 0#'More than 14'
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
        copy_X[sg.CAT_CONTACT_LAST_CAMPAIGN] = copy_X[sg.NB_CONTACT_LAST_CAMPAIGN].apply(lambda row: self._discretisation_NB_CONTACT_LAST_CAMPAIGN(row))
        copy_X = copy_X.drop(sg.NB_CONTACT_LAST_CAMPAIGN, axis=1)
        return copy_X

    def _discretisation_NB_CONTACT(self, row):
        """
        Method that discretize the column NB_CONTACT
        Parameters
        ----------
        row: int value
            One value from the column NB_CONTACT
        Returns
        -------
        str in function of the value
        """
        if row == 1:
            return 6#'1 call'
        elif row > 1 and row < 4:
            return 5#'2 or 3 call'
        elif row >= 4 and row < 7:
            return 4#'Between 4 and 6 call'
        elif row >= 7 and row < 11:
            return 3#'Between 4 and 6 call'    
        elif row >= 11 and row < 15:
            return 2#'Between 11 and 14 call'
        elif row >= 15:
            return 1#'More than 15 call'
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
        copy_X[sg.CAT_CONTACT] = copy_X[sg.NB_CONTACT].apply(lambda row: self._discretisation_NB_CONTACT(row))
        copy_X = copy_X.drop(sg.NB_CONTACT,axis=1)
        return copy_X

if __name__ == "__main__": 
    df, df_soc_eco = Load().Download()
    df.head()
    col_to_treat = [sg.NB_CONTACT, sg.NB_CONTACT_LAST_CAMPAIGN]
    df_treat = NbContactTransformer(2,2,2).fit_transform(df[col_to_treat])
    df_treat.head()


    # add to train
    #nb_contact_transformer = Pipeline(steps=[
    #    ('transformer', NbContactTransformer()),
    #    ('imputer', SimpleImputer(missing_values= np.NaN, strategy='most_frequent')),
    #    ('label', MultiLabelEncoder(list(nb_contact_features)))])
