from forecast.infrastructure.Load import Load
import forecast.settings.base as sg

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class QuantitativeTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = self._add_AT_DEBIT(X)
        X = self._add_PRECARITY(X)
        X = self._treat_NaN_RESULT_LAST_CAMPAIGN(X)
        X = self._drop_DURATION_CONTACT(X)
        X = self._add_CAT_CONTACT_LAST_CAMPAIGN(X)
        X = self._add_CAT_CONTACT(X)
        return X

    def _add_AT_DEBIT(self, X):
        X['AT_DEBIT'] = 'No'
        AT_DEBIT_TRUE = X.query('{} < 0'.format(sg.BALANCE))\
                        .assign(AT_DEBIT=lambda x: 'YES').copy()
        INDEX = list(X.query('{} < 0'.format(sg.BALANCE)).index)
        X.loc[INDEX] = AT_DEBIT_TRUE
        return X

    def _add_PRECARITY(self, X):
        X['PRECARITY'] = 'No' 
        PRECARITY_TRUE = X.query('{} ==0 '.format(sg.BALANCE))\
                            .assign(PRECARITY=lambda x: 'Yes').copy()
        INDEX = list(X.query('{} ==0 '.format(sg.BALANCE)).index)
        X.loc[INDEX] = PRECARITY_TRUE
        return X

    def _treat_NaN_RESULT_LAST_CAMPAIGN(self, X):
        not_contacted = X.query('{} == -1'.format(sg.NB_DAY_LAST_CONTACT)).copy()
        not_contacted[sg.RESULT_LAST_CAMPAIGN] = not_contacted[sg.RESULT_LAST_CAMPAIGN].fillna("Not contacted")
        INDEX = list(not_contacted.index)
        X.loc[INDEX] = not_contacted

        contacted = X.query('{} != -1'.format(sg.NB_DAY_LAST_CONTACT)).copy()
        contacted[sg.RESULT_LAST_CAMPAIGN] = contacted[sg.RESULT_LAST_CAMPAIGN].fillna("Autre")
        INDEX = list(contacted.index)
        X.loc[INDEX] = contacted
        return X

    def _drop_DURATION_CONTACT(self, X):
        return X.drop(sg.DURATION_CONTACT, axis=1)

    def _discretisation_NB_CONTACT_LAST_CAMPAIGN(self, row):
        if row == 0:
            return 'Not contacted'
        elif row > 0 and row < 5:
            return 'Between 1 and 4 call'
        elif row >= 5 and row < 11:
            return 'Between 5 and 10 call'
        elif row >= 11 and row < 15:
            return 'Between 11 and 14 call'
        elif row >= 15:
            return 'More than 15 call'
        else:
            return np.NaN

    def _add_CAT_CONTACT_LAST_CAMPAIGN(self, X):
        X['CAT_CONTACT_LAST_CAMPAIGN'] = X[sg.NB_CONTACT_LAST_CAMPAIGN].apply(lambda row: self._discretisation_NB_CONTACT_LAST_CAMPAIGN(row))
        X = X.drop(sg.NB_CONTACT_LAST_CAMPAIGN,axis=1)
        return X

    def _discretisation_NB_CONTACT(self, row):
        if row == 1:
            return '1 call'
        elif row > 1 and row < 4:
            return '2 or 3 call'
        elif row >= 4 and row < 7:
            return 'Between 4 and 6 call'
        elif row >= 11 and row < 15:
            return 'Between 7 and 11 call'
        elif row >= 11:
            return 'More than 1 call'
        else:
            return np.NaN

    def _add_CAT_CONTACT(self, X):
        X['CAT_CONTACT'] = X[sg.NB_CONTACT].apply(lambda row: self._discretisation_NB_CONTACT(row))
        X = X.drop(sg.NB_CONTACT,axis=1)
        return X

if __name__ == "__main__": 
    df, df_soc_eco = Load().Download()
    df.head()
    df_treat = QuantitativeTransformer().fit_transform(df)
    df_treat.head()

