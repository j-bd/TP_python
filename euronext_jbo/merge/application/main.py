#!/usr/bin/env python
# coding: utf-8

"""
Module to lauch main steps for Universe and Vigeo files

Example
-------
Script could be run with the following command line

    $ python merge/application/main.py

Input datasets localizations can be specified with

    $ python fmerge/application/main.py -u path/to/universe_file
    -v path/to/vigeo_file -f path/to/filter_file
"""
import logging
from os.path import basename

from merge.settings import base, log_saving
from merge.domain.vigeo_keys_merging import VigeoKeysMerging
from merge.infrastructure.save_final_file import ProcessedDataSave
from merge.infrastructure.vigeo_preprocessing import VigeoPreprocessing
from merge.infrastructure.command_line_parser import MergeCommandLineParser
from merge.infrastructure.isin_eid_preprocessing import IsinEidPreprocessing
from merge.infrastructure.universe_preprocessing import UniversePreprocessing


def main():
    """Launch main steps of model training."""
    # log saving setup
    log_saving.enable_logging(
        log_filename=f'{basename(__file__)}.log',
        logging_level=logging.DEBUG
    )
    logging.info('----------------------------------')
    logging.info(f'Script {basename(__file__)}')
    logging.info('----------------------------------')

    # Command line parser
    parser = MergeCommandLineParser()
    args = parser.parse_args()

    # Raw data preprocessing
    logging.info(" Raw data preprocessing on going...")
    u_preprocess = UniversePreprocessing(args.universe_input)
    universe_df = u_preprocess.do_preprocessing()
    f_preprocess = IsinEidPreprocessing(args.filter_input)
    filter_df = f_preprocess.do_preprocessing()
    v_preprocess = VigeoPreprocessing(args.vigeo_input)
    vigeo_df = v_preprocess.do_preprocessing()
    logging.info(" Raw data preprocessing done.")

    # Merging Vigeo_key to Universe
    logging.info(" Merging Vigeo_key to Universe on going...")
    merging_data = VigeoKeysMerging(universe_df, filter_df, vigeo_df)
    final_data = merging_data.merge_vigeo_key()
    logging.info(" Merging Vigeo_key to Universe done.")

    # Save data
    save_processed_data = ProcessedDataSave(
        final_data, base.UNIVERSE_VIGEO_FILE
    )
    save_processed_data.save_file()
    logging.info(" File saved.")

    logging.info(f'End of script {basename(__file__)}')


if __name__ == "__main__":
    main()
