"""
Contains all configurations for the projectself.
Should NOT contain any secrets.

"""

import os

# Path variables
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DATA_DIR = os.path.join(REPO_DIR, 'data')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
LOGS_DIR = os.path.join(REPO_DIR, 'logs')

UNIVERSE_FILE = os.path.join(RAW_DATA_DIR, 'Universe.csv')
VIGEO_FILE = os.path.join(RAW_DATA_DIR, 'Vigeo_keys.xlsx')
ISIN_EID_FILTER_FILE = os.path.join(RAW_DATA_DIR, 'F7_ISIN_to_EID_Filter.csv')
UNIVERSE_VIGEO_FILE = os.path.join(PROCESSED_DATA_DIR, 'universe_vigeo.csv')

# Universe file
U_HISTORICAL_ISIN = 'Historical_ISIN'
U_ISIN = 'ISIN'
U_SHORT_NAME = 'Short Name'
U_CUTOFF = 'cutoff'
U_FACTSET_ENTITY_ID = 'factset_entity_id'
U_COLUMNS = [
    U_HISTORICAL_ISIN, U_ISIN, U_SHORT_NAME, U_CUTOFF, U_FACTSET_ENTITY_ID
]
U_COLUMNS_CAST = {
    U_HISTORICAL_ISIN: 'category', U_ISIN: 'category', U_SHORT_NAME: 'object',
    U_CUTOFF: 'datetime64', U_FACTSET_ENTITY_ID: 'category'
}
U_VIGEO_KEY = 'Vigeo_Key'

# Vigeo file
V_VIGEO_KEY = 'Vigeo_Key'
V_CUTOFF = 'Cutoff_dates'
V_ISIN = 'ISIN'
V_TITLE = 'Title'
V_COLUMNS = [V_VIGEO_KEY, V_CUTOFF, V_ISIN, V_TITLE]
V_COLUMNS_CAST = {
    V_VIGEO_KEY: 'category', V_CUTOFF: 'datetime64', V_ISIN: 'category',
    V_TITLE: 'category'
}

# F7_ISIN_to_EID_Filter file
F_ISIN = 'isin'
F_FACTSET_ENTITY_ID = 'factset_entity_id'
F_COLUMNS = [F_ISIN, F_FACTSET_ENTITY_ID]
F_COLUMNS_CAST = {F_ISIN: 'category', F_FACTSET_ENTITY_ID: 'category'}

# Global
DATE = 'date'
