import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from forecast.domain.NbContactTransformer import NbContactTransformer
import forecast.settings.base as sg
from forecast.infrastructure.Load import Load

class MultiLabelEncoder(BaseEstimator, TransformerMixin):
    """
    Use LabelEncoder() on multiple column
    """
    def __init__(self, columns = None):
        self.columns = columns 

    def fit(self, X, y=None):
        return self 

    def transform(self, X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(list(output[col]))
        else:
            for colname in list(output.columns):
                output[colname] = LabelEncoder().fit_transform(output)
        return output

if __name__ == "__main__": 
    df, df_soc_eco = Load().Download()
    df.head()
    col_to_treat = [sg.NB_CONTACT, sg.NB_CONTACT_LAST_CAMPAIGN]
    df_treat = NbContactTransformer().fit_transform(df[col_to_treat])
    df_treat.head()
    df_treat_label = MultiLabelEncoder(['CAT_CONTACT_LAST_CAMPAIGN', 'CAT_CONTACT']).fit_transform(df_treat)
    df_treat_label.head()

