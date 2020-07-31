#!/usr/bin/env python
# coding: utf-8

"""
Module to add vigeo key to corresponding universe row.

Classes
-------
VigeoKeysMerging

"""
import logging
from os.path import basename

from merge.settings import base, log_saving


class VigeoKeysMerging:
    """
        Return a DataFrame with added values.

        Attributes
        ----------
        universe_df: pandas.DataFrame
        filter_df: pandas.DataFrame
        vigeo_df: pandas.DataFrame

        Methods
        -------
        __init__
        merge_vigeo_key
    """
    def __init__(self, universe_df, filter_df, vigeo_df):
        """Initialize class"""
        self.universe_df = universe_df
        self.filter_df = filter_df
        self.vigeo_df = vigeo_df

    def merge_vigeo_key(self):
        """Perform merging following five rules.
        1. ISIN (in Vigeo) = ISIN in universe
        2. ISIN (in Vigeo) = Historical ISIN in universe
        3. Vigeo Key = ISIN in universe
        4. Vigeo Key = Historical ISIN in universe
        5. ISIN (in Vigeo) = ISIN in F7_ISIN_to_EID_Filter and
        facset_entity_id = factset_entity_id In Universe.

        For each rule we need to have V_CUTOFF equal or closest above U_CUTOFF

        Returns
        -------
        universe_df: pandas.DataFrame
        """
        # log saving setup
        # log_saving.enable_logging(
        #     log_filename=f'{basename(__file__)}.log',
        #     logging_level=logging.DEBUG
        # )
        logging.info('----------------------------------')
        logging.info(f'Script {basename(__file__)}')
        logging.info('----------------------------------')

        # local variable initialization
        counter = 0
        c1, c2, c3, c4, c5, no_value = [0] * 6
        size = len(self.universe_df)
        for u_index, u_row in self.universe_df.iterrows():
            # Displays progress
            counter += 1
            logging.info(f" {counter}/{size}")
            logging.info(f" Historical_ISIN: {u_row[base.U_HISTORICAL_ISIN]}")

            first_condition = self.vigeo_df.loc[(self.vigeo_df[base.DATE] >= u_row[base.DATE]) & (self.vigeo_df[base.V_ISIN] == u_row[base.U_ISIN])].head(1)
            if len(first_condition) != 0:
                self.universe_df.loc[u_index, base.U_VIGEO_KEY] = first_condition[base.V_VIGEO_KEY].values[0]
                logging.info(f" Condition number 1 valid. Value Added")
                c1 += 1
                continue

            second_condition = self.vigeo_df.loc[(self.vigeo_df[base.DATE] >= u_row[base.DATE]) & (self.vigeo_df[base.V_ISIN] == u_row[base.U_HISTORICAL_ISIN])].head(1)
            if len(second_condition) != 0:
                self.universe_df.loc[u_index, base.U_VIGEO_KEY] = second_condition[base.V_VIGEO_KEY].values[0]
                logging.info(f" Condition number 2 valid. Value Added")
                c2 += 1
                continue

            third_condition = self.vigeo_df.loc[(self.vigeo_df[base.DATE] >= u_row[base.DATE]) & (self.vigeo_df[base.V_VIGEO_KEY] == u_row[base.U_ISIN])].head(1)
            if len(third_condition) != 0:
                self.universe_df.loc[u_index, base.U_VIGEO_KEY] = third_condition[base.V_VIGEO_KEY].values[0]
                logging.info(f" Condition number 3 valid. Value Added")
                c3 += 1
                continue

            fourth_condition = self.vigeo_df.loc[(self.vigeo_df[base.DATE] >= u_row[base.DATE]) & (self.vigeo_df[base.V_VIGEO_KEY] == u_row[base.U_HISTORICAL_ISIN])].head(1)
            if len(fourth_condition) != 0:
                self.universe_df.loc[u_index, base.U_VIGEO_KEY] = fourth_condition[base.V_VIGEO_KEY].values[0]
                logging.info(f" Condition number 4 valid. Value Added")
                c4 += 1
                continue

            fifth_condition = self.filter_df.loc[(self.filter_df[base.F_FACTSET_ENTITY_ID] == u_row[base.U_FACTSET_ENTITY_ID])]
            if len(fifth_condition) != 0:
                fifth_condition = self.vigeo_df.loc[(self.vigeo_df[base.V_ISIN] == fifth_condition[base.F_ISIN].values[0]) & (self.vigeo_df[base.DATE] >= u_row[base.DATE])].head(1)
                if len(fifth_condition) != 0:
                    self.universe_df.loc[u_index, base.U_VIGEO_KEY] = fifth_condition[base.V_VIGEO_KEY].values[0]
                    logging.info(f" Condition number 5 valid. Value Added")
                    c5 += 1
                    continue

            logging.info(" No condition is matching. No value will be add")
            no_value += 1

        logging.info('----------------------------------')
        logging.info('Results:')
        logging.info(
            f'Number of condition 1: {c1}, Number of condition 2: {c2},'
            f'Number of condition 3: {c3}, Number of condition 4: {c4},'
            f'Number of condition 5: {c5}, Number of empty values: {no_value}'
        )
        logging.info('----------------------------------')
        logging.info(f'End of script {basename(__file__)}')
        return self.universe_df
