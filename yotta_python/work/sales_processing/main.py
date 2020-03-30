#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:54:10 2020

@author: j-bd
"""

from datasetformatter import DatasetPreparation
import datasetprocess as dp
import constants as c


def main():
    """Launch main steps"""
    formatter = DatasetPreparation()
    df_format = formatter.prepare_data

    sub_df = dp.DataframeFilter(df_format)

    aggregate = dp.DataSelection(sub_df.sub_df)
    aggregate.aggregate_data([c.COL_KEY["equip"]], "M")

    sales = dp.SalesRevenue(sub_df.sub_df)
    sales_df = sales.provide_past_figures

    calendar = dp.CalendarInformation(sales_df)
    calendar_df = calendar.provide_calendar_information

    dp.export_data(calendar_df)

if __name__ == "__main__":
    main()
