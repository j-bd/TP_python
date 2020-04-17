"""
Contains all configurations for the projectself.
Should NOT contain any secrets.

>>> import settings
>>> settings.DATA_DIR
"""
# import os
# import logging

# By default the data is stored in this repository's "data/" folder.
# You can change it in your own settings file.
# REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
# DATA_DIR = os.path.join(REPO_DIR, 'data')
# OUTPUTS_DIR = os.path.join(REPO_DIR, 'outputs')
# LOGS_DIR = os.path.join(REPO_DIR, 'logs')
# TESTS_DIR = os.path.join(REPO_DIR, 'tests')
# TESTS_DATA_DIR = os.path.join(TESTS_DIR, 'fixtures')


# # Logging
# def enable_logging(log_filename, logging_level=logging.DEBUG):
#     """Set loggings parameters.

#     Parameters
#     ----------
#     log_filename: str
#     logging_level: logging.level

#     """
#     with open(os.path.join(LOGS_DIR, log_filename), 'a') as file:
#         file.write('\n')
#         file.write('\n')

#     LOGGING_FORMAT = '[%(asctime)s][%(levelname)s][%(module)s] - %(message)s'
#     LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

#     logging.basicConfig(
#         format=LOGGING_FORMAT,
#         datefmt=LOGGING_DATE_FORMAT,
#         level=logging_level,
#         filename=os.path.join(LOGS_DIR, log_filename)
#     )


# LIST_PRODUCTS_TO_KEEP = ['ordinateur', 'telephone']
# STR_START_DATE = '2017-01-01'
# STR_END_DATE = '2019-12-31'
# BANK_HOLIDAYS_DATE_COL = 'date'
# BANK_HOLIDAYS_NAME_COL = 'name'
# SCHOOL_HOLIDAYS_A_RAW_COL = 'vacances_zone_a'
# SCHOOL_HOLIDAYS_B_RAW_COL = 'vacances_zone_b'
# SCHOOL_HOLIDAYS_C_RAW_COL = 'vacances_zone_c'
# SCHOOL_HOLIDAYS_NAME_RAW_COL = 'nom_vacances'
# SCHOOL_HOLIDAYS_A_COL = 'bool_school_holiday_A'
# SCHOOL_HOLIDAYS_B_COL = 'bool_school_holiday_B'
# SCHOOL_HOLIDAYS_C_COL = 'bool_school_holiday_C'
# SCHOOL_HOLIDAYS_NAME_COL = 'school_holiday_name'
# LIST_SCHOOL_HOLIDAYS_COLS = [SCHOOL_HOLIDAYS_A_COL, SCHOOL_HOLIDAYS_B_COL, SCHOOL_HOLIDAYS_C_COL]
# EQUIPMENT_COL = 'equipment'
# CITY_COL = 'city'
# DATE_COL = 'date'
# SALES_COL = 'ca'
# SALES_LAST_YEAR_COL = 'ca_last_year'
# SALES_LAST_YEAR_SAME_WEEKDAY = 'ca_last_year_same_weekday'
# WEEKDAY_COL = 'weekday'
# IS_WEEKEND_COL = 'is_weekend'
# IS_BANK_HOLIDAY_COL = 'is_bankholiday'
# DISTANCE_CLOSEST_BANK_HOLIDAY_COL = 'distance_between_closest_bank_holiday'
# IS_SCHOOL_HOLIDAY_COL = 'is_schoolholiday'


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