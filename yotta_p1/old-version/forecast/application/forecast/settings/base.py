"""
Contains all configurations for the projectself.
Should NOT contain any secrets.

>>> import settings
>>> settings.DATA_DIR
"""
import os

# By default the data is stored in this repository's "data/" folder.
# You can change it in your own settings file.
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DATA_DIR = os.path.join(REPO_DIR, 'data')
EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, 'external')
INTERIM_DATA_DIR = os.path.join(DATA_DIR, 'interim')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
MODELS_DIR = os.path.join(REPO_DIR, 'models')
# OUTPUTS_DIR = os.path.join(REPO_DIR, 'outputs')
# LOGS_DIR = os.path.join(REPO_DIR, 'logs')
# TESTS_DIR = os.path.join(REPO_DIR, 'tests')
# TESTS_DATA_DIR = os.path.join(TESTS_DIR, 'fixtures')

# Add the names of the data
name_file_data = 'data.csv'
name_file_socio_eco = 'socio_eco.csv'

# Socio eco columns
DATE_SOCIO_COL = 'DATE'
IDX_CONSUMER_PRICE_COL = 'IDX_CONSUMER_PRICE'
IDX_CONSUMER_CONFIDENCE_COL = 'IDX_CONSUMER_CONFIDENCE'
EMPLOYMENT_VARIATION_RATE_COL = 'EMPLOYMENT_VARIATION_RATE'
NB_EMPLOYE_COL = 'NB_EMPLOYE'
SOCIO_ECO_MONTH_COLS = [IDX_CONSUMER_PRICE_COL, IDX_CONSUMER_CONFIDENCE_COL]
SOCIO_ECO_TRIMESTER_COLS = [EMPLOYMENT_VARIATION_RATE_COL, NB_EMPLOYE_COL]
SOCIO_ECO_COLS = [IDX_CONSUMER_PRICE_COL, IDX_CONSUMER_CONFIDENCE_COL,
                  EMPLOYMENT_VARIATION_RATE_COL, NB_EMPLOYE_COL]

# Columns from Data File
DATE_DATA = 'DATE'
AGE = 'AGE'
JOB_TYPE = 'JOB_TYPE'
STATUS = 'STATUS'
EDUCATION = 'EDUCATION'
HAS_DEFAULT = 'HAS_DEFAULT'
BALANCE = 'BALANCE'
HAS_HOUSING_LOAN = 'HAS_HOUSING_LOAN'
HAS_PERSO_LOAN = 'HAS_PERSO_LOAN'
CONTACT = 'CONTACT'
DURATION_CONTACT = 'DURATION_CONTACT'
NB_CONTACT = 'NB_CONTACT'
NB_DAY_LAST_CONTACT = 'NB_DAY_LAST_CONTACT'
NB_CONTACT_LAST_CAMPAIGN = 'NB_CONTACT_LAST_CAMPAIGN'
RESULT_LAST_CAMPAIGN = 'RESULT_LAST_CAMPAIGN'
SUBSCRIPTION = 'SUBSCRIPTION'

# Date columns
DATA_DATE_FORMAT = '%Y-%m-%d'
DAY_SELECTED_COL = "DAY_SELECTED"
WEEKEND = ["Saturday", "Sunday"]
MONTH_LAB = 'MONTH_LABELS'
MONTH_ENCODING = {'January' : 0, 'February' : 2, 'March' : 5, 'April' : 2,
                  'May' : 2, 'June' : 2, 'July' : 2, 'August' : 2,
                  'September' : 5, 'October' : 5, 'November' : 2, 'December' : 0}
DATE_COLS = [MONTH_LAB, DAY_SELECTED_COL]


# Age
AGE_BINS = [18, 25, 30, 35, 40, 45, 50, 55, 60, 70, 120, 130]
AGE_LABELS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
AGE_LAB = "AGE_LABELS"

# Job type
JOB_LAB = "JOB_LABELS"
JOB_ENCODING = {'Col bleu' : 6, 'Manager' : 9, 'Technicien' : 8, 'Admin' : 7,
                'Services' : 4, 'Retraité' : 5, 'Indépendant' : 2, 'Entrepreuneur' : 1,
                'Chomeur' : 2, 'Employé de ménage' : 1, 'Etudiant' : 3}

# Status
STATUS_LAB = "STATUS_LABELS"
STATUS_ENCODING = {'Marié' : 1, 'Célibataire' : 2, 'Divorcé' : 0}

# Education
EDUCATION_LAB = "EDUCATION_LABELS"
EDUCATION_ENCODING = {'Primaire' : 0, 'Secondaire' : 1, 'Tertiaire' : 2}

# Bank status
BANK_STATUS_COL = [HAS_DEFAULT, HAS_HOUSING_LOAN, HAS_PERSO_LOAN]
BANK_STATUS_LAB = "BANK_STATUS"

# NB_DAY_LAST_CONTACT features
MONTH_LAST_CONTACT ='MONTH_LAST_CONTACT'
WEEK_LAST_CONTACT = 'WEEK_LAST_CONTACT'
GAP_IN_MONTH = 'GAP_IN_MONTH'
