#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:54:10 2020

@author: j-bd
"""

from datasetformatter import DatasetFormatter
import datasetprocess as dp
import constants as c


def main():
    """Launch main steps"""
    formatter = DatasetFormatter()
    df_format = formatter.process

    sub_df = dp.DataframeFilter(df_format)

    aggregate = dp.DataframeAggregator(sub_df.sub_df)
    aggregate.aggregate_data([c.COL_KEY["equip"]], "M")

    sales = dp.SalesRevenue(sub_df.sub_df)
    sales_df = sales.process

    calendar = dp.CalendarInformation(sales_df)
    calendar_df = calendar.process

    dp.export_data(calendar_df)

if __name__ == "__main__":
    main()
