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

from merge.infrastructure.command_line_parser import MergeCommandLineParser
from merge.infrastructure.universe_preprocessing import UniversePreprocessing
from merge.infrastructure.isin_eid_preprocessing import IsinEidPreprocessing
from merge.infrastructure.vigeo_preprocessing import VigeoPreprocessing
from merge.domain.vigeo_keys_merging import VigeoKeysMerging
from merge.settings import base


def main():
    """Launch main steps of model training."""
    # Command line parser
    parser = MergeCommandLineParser()
    args = parser.parse_args()
    print(args)  # TODO Removed

    # Raw data preprocessing
    u_preprocess = UniversePreprocessing(args.universe_input)
    universe_df = u_preprocess.do_preprocessing()
    print(universe_df.info())  # TODO Removed
    f_preprocess = IsinEidPreprocessing(args.filter_input)
    filter_df = f_preprocess.do_preprocessing()
    print(filter_df.info())  # TODO Remove
    v_preprocess = VigeoPreprocessing(args.vigeo_input)
    vigeo_df = v_preprocess.do_preprocessing()
    print(vigeo_df.info())  # TODO Removed
    print(vigeo_df.head(5))  # TODO Removed

    # Merging Vigeo_key to Universe
    merging_data = VigeoKeysMerging(universe_df, filter_df, vigeo_df)
    final_data = merging_data.merge_vigeo_key()

    # Save data
    final_data.to_csv(base.UNIVERSE_VIGEO_FILE)


if __name__ == "__main__":
    main()
