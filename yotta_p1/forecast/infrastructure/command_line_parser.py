#!/usr/bin/env python
# coding: utf-8

import os
import argparse

import forecast.settings as stg

class TrainCommandLineParser():

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--data_input",
            help="path to input data file",
            default=os.path.join(stg.RAW_DATA_DIR, "data.csv"),
            )
        self.parser.add_argument(
            "--socio_eco_input",
            help="path to input socio eco file",
            default=os.path.join(stg.RAW_DATA_DIR, "socio_eco.csv"),
            )
        self.parser.add_argument(
            "--merge_output",
            help="path to preprocessed file output",
            default=os.path.join(stg.INTERIM_DATA_DIR, "data_socio_merged.csv"),
            )
        self.parser.add_argument(
            "--model_output",
            help="path to model file output",
            default=os.path.join(stg.MODELS_DIR, "model.joblib"),
            )
        self.parser.add_argument(
            "--optimisation",
            help="Bayesian optimisation process activation",
            default=False,
            )

    def parse_args(self):
        return self.parser.parse_args()

class PredictCommandLineParser():

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--data_input",
            help="path to input data file",
            default=os.path.join(stg.RAW_DATA_DIR, "data.csv"),
            )
        self.parser.add_argument(
            "--socio_eco_input",
            help="path to input socio eco file",
            default=os.path.join(stg.RAW_DATA_DIR, "socio_eco.csv"),
            )
        self.parser.add_argument(
            "--merge_output",
            help="path to preprocessed file output",
            default=os.path.join(stg.INTERIM_DATA_DIR, "data_socio_merged.csv"),
            )
        self.parser.add_argument(
            "--model_input",
            help="path to input model file",
            default=os.path.join(stg.MODELS_DIR, "model.joblib"),
            )

    def parse_args(self):
        return self.parser.parse_args()
