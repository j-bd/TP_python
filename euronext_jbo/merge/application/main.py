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


def main():
    """Launch main steps of model training."""
    # Command line parser
    parser = MergeCommandLineParser()
    args = parser.parse_args()
    print(args)  # TODO Removed


if __name__ == "__main__":
    main()
