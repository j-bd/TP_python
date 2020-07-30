#!/usr/bin/env python
# coding: utf-8

"""
Module to add vigeo key to corresponding universe row.

Classes
-------
VigeoKeysMerging

"""

import os

import pandas as pd

from merge.settings import base


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

        For each rul we need to have V_CUTOFF equal or closest above U_CUTOFF


        Returns
        -------
        universe_df: pandas.DataFrame
        """
        counter = 0
        size = len(self.universe_df)
        for u_index, u_row in self.universe_df.iterrows():
            print(counter, '/', size)
            for v_index, v_row in self.vigeo_df.iterrows():
                if u_row[base.DATE] <= v_row[base.DATE]:
                    # print(i)
                    if u_row[base.U_ISIN] == v_row[base.V_ISIN]:
                        self.universe_df.loc[u_index, base.U_VIGEO_KEY] = v_row[base.V_VIGEO_KEY]
                        print('ISIN')
                        print(
                            f"True, universe: {u_row['date']}, vigeo {v_row['date']}, vig index: {v_index}, isin {v_row['ISIN']}"
                        )
                        print(v_row['Vigeo_Key'])
                        print(u_row[base.U_VIGEO_KEY])
                        break
                    elif u_row[base.U_HISTORICAL_ISIN] == v_row[base.V_ISIN]:
                        self.universe_df.loc[u_index, base.U_VIGEO_KEY] = v_row[base.V_VIGEO_KEY]
                        print('Historical_ISIN')
                        print(
                            f"True, universe: {u_row['date']}, vigeo {v_row['date']}, vig index: {v_index}, isin {v_row['ISIN']}"
                        )
                        print(v_row['Vigeo_Key'])
                        print(u_row[base.U_VIGEO_KEY])
                        break
                    elif u_row[base.U_ISIN] == v_row[base.V_VIGEO_KEY]:
                        self.universe_df.loc[u_index, base.U_VIGEO_KEY] = v_row[base.V_VIGEO_KEY]
                        print('ISIN - Vigeo_Key')
                        print(
                            f"True, universe: {u_row['date']}, vigeo {v_row['date']}, vig index: {v_index}, isin {v_row['ISIN']}"
                        )
                        print(v_row['Vigeo_Key'])
                        print(u_row[base.U_VIGEO_KEY])
                        break
                    elif u_row[base.U_HISTORICAL_ISIN] == v_row[base.V_VIGEO_KEY]:
                        self.universe_df.loc[u_index, base.U_VIGEO_KEY] = v_row[base.V_VIGEO_KEY]
                        print('Historical_ISIN - Vigeo_Key')
                        print(
                            f"True, universe: {u_row['date']}, vigeo {v_row['date']}, vig index: {v_index}, isin {v_row['ISIN']}"
                        )
                        print(v_row['Vigeo_Key'])
                        print(u_row[base.U_VIGEO_KEY])
                        break
                    # else:
                    #     for f_index, f_row in self.filter_df.iterrows():
                    #         if u_row[base.U_FACTSET_ENTITY_ID] == f_row[base.F_FACTSET_ENTITY_ID] and f_row[base.F_ISIN] == v_row[base.V_ISIN]:
                    #              u_row[base.U_VIGEO_KEY] = v_row[base.V_VIGEO_KEY]
                    #              print('filter')
                    #              print(
                    #                  f"True, universe: {u_row['date']}, vigeo {v_row['date']}, vig index: {v_index}, isin {v_row['ISIN']}"
                    #              )
                    #              print(v_row['Vigeo_Key'])
                    #              print(u_row[base.U_VIGEO_KEY])
                    #              break
                    #         break

            counter += 1
            if counter == 10:
                break
        return self.universe_df
