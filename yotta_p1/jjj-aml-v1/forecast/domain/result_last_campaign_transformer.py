import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

import forecast.settings.base as sg

class ResultLastCampaignTransformer(BaseEstimator, TransformerMixin):
    """
    Treat the NaN of RESULT_LAST_CAMPAIGN

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
        X_copy = X.copy()
        # not_contacted = X_copy.query('{} == -1'.format(sg.NB_DAY_LAST_CONTACT)).copy()
        # not_contacted[sg.RESULT_LAST_CAMPAIGN] = not_contacted[sg.RESULT_LAST_CAMPAIGN].fillna("Not contacted")
        # INDEX = list(not_contacted.index)
        # X_copy.loc[INDEX] = not_contacted

        # contacted = X_copy.query('{} != -1'.format(sg.NB_DAY_LAST_CONTACT)).copy()
        # contacted[sg.RESULT_LAST_CAMPAIGN] = contacted[sg.RESULT_LAST_CAMPAIGN].fillna("Autre")
        # INDEX = list(contacted.index)
        # X_copy.loc[INDEX] = contacted

        X_copy[sg.RESULT_LAST_CAMPAIGN_succes] = X_copy.RESULT_LAST_CAMPAIGN.apply(lambda x: self.get_value(x,'Succes'))
        X_copy[sg.RESULT_LAST_CAMPAIGN_echec] = X_copy.RESULT_LAST_CAMPAIGN.apply(lambda x: self.get_value(x,'Echec'))
        return X_copy[sg.RLC_COLS]

    def get_feature_names(self):
        """
        Return features name.
        """
        return sg.RLC_COLS

    def get_value(self, row, value):
        if row == value:
            return 1
        else:
            return 0


if __name__ == "__main__": 
    df, df_soc_eco = Load().Download()
    df.head()
    columns = [sg.NB_DAY_LAST_CONTACT, sg.RESULT_LAST_CAMPAIGN]
    df_treat = ResultLastCampaignTransformer().fit_transform(df[columns])
    df_treat.head()
    df_treat.shape
    df_treat.RESULT_LAST_CAMPAIGN_echec.value_counts()
    df_treat.RESULT_LAST_CAMPAIGN_succes.value_counts()

    # add to train
    #result_last_campaign_transformer = Pipeline(steps=[
    #    ('transformer', ResultLastCampaignTransformer()),
    #    ('label', LabelEncoder())])
