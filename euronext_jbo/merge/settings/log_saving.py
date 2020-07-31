#!/usr/bin/env python
# coding: utf-8

"""
Module to save log report of process execution.

Function
-------
enable_logging

"""
import os
import logging

from merge.settings import base


def enable_logging(log_filename, logging_level=logging.DEBUG):
    """Set loggings parameters.

    Parameters
    ----------
    log_filename: str
    logging_level: logging.level

    """
    with open(os.path.join(base.LOGS_DIR, log_filename), 'a') as file:
        file.write('\n')
        file.write('\n')

    logging_format = '[%(asctime)s][%(levelname)s][%(module)s] - %(message)s'
    logging_date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        format=logging_format,
        datefmt=logging_date_format,
        level=logging_level,
        filename=os.path.join(base.LOGS_DIR, log_filename)
    )
