# forecast Project (jjj-aml) Repository

Code to solve forecast assignment


# Project Organization

------------

    ├── data                <- Contains data files.
    │   ├── external        <- Data from third party sources.
    │   ├── interim         <- Intermediate data that has been transformed.
    │   ├── processed       <- The final, canonical data sets for modeling and predictions.
    │   └── raw             <- The original, immutable data dump.
    │
    ├── forecast            <- Source code for use in this project.
    │   │
    │   ├── application     <- Scripts to train models and make predictions.
    │   │   ├── __init__.py <- Makes application a Python module.
    │   │   ├── predict.py  <- Script to make predictions.
    │   │   └── train.py    <- Script to train models.
    │   │
    │   ├── domain          <- Contains domain related part of the code.
    │   │   ├── __init__.py <- Makes domain a Python module.
    │   │   ├── *_transformer.py
    │   │   │               <- Sklearn data transformers.
    │   │   ├── bayesian_optimisation.py
    │   │   │               <- Perform bayesian optimisations.
    │   │   ├── model_evaluation.py
    │   │   │               <- Model evaluations.
    │   │   ├── model_train.py
    │   │   │               <- Train function.
    │   │   ├── over_sampling.py
    │   │   │               <- Over sampling class (use e.g. RandomOverSampler or SMOTE).
    │   │   └── pipeline.py <- Transformer pipeline.
    │   │
    │   ├── infrastructure  <- Contains infrastructure part of the code.
    │   │   ├── __init__.py <- Makes infrastructure a Python module.
    │   │   ├── command_line_parser.py
    │   │   │               <- Command line parser for `predict.py` and `train.py`.
    │   │   └── preprocessing.py
    │   │                   <- Perform first operations, e.g. load data or merge dataframes.
    │   │
    │   ├── settings        <- Contains variables.
    │   │   ├── __init__.py <- Makes settings a Python module, and load `base.py`.
    │   │   └── base.py     <- Contains path/to/file variables and dataframe column names.
    │   │
    │   └── __init__.py     <- Makes forecast a Python module.
    │
    ├── models              <- Trained and serialized models.
    │
    ├── notebooks           <- Jupyter notebooks for data exploration and interpretability.
    │
    ├── reports             <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures         <- Generated graphics and figures to be used in reporting
    │
    ├── activate.sh         <- Activate the python environment.
    │
    ├── init.sh             <- Create a virtual environment.
    │
    ├── Makefile            <- Makefile with commands like `make init` or `make install`.
    │
    ├── README.md           <- The top-level README for developers using this project.
    │
    ├── requirements.txt    <- The requirements file for reproducing analysis environment,
    │                          e.g. generated with `pip freeze > requirements.txt`.
    │
    └── setup.py            <- Makes project pip installable `pip install -e .`
                               so forecast can be imported.

--------


# Getting Started


## 0. Clone this repository and checkout the v1 branch
```
$ git clone https://gitlab.com/yotta-academy/cohort-2020/projects/ml-project/jjj-aml.git
$ cd jjj-aml
$ git checkout v1
```

## 1. Setup your virtual environment and activate it

Goal : create a local virtual environment in the folder `./.venv/`.

- First: check your python3 version:

    ```
    $ python3 --version
    # examples of outputs:
    Python 3.6.2 :: Anaconda, Inc.
    Python 3.7.2

    $ which python3
    /Users/benjamin/anaconda3/bin/python3
    /usr/bin/python3
    ```

    - If you don't have python3 and you are working on your mac: install it from [python.org](https://www.python.org/downloads/)
    - If you don't have python3 and are working on an ubuntu-like system: install from package manager:

        ```
        $ apt-get update
        $ apt-get -y install python3 python3-pip python3-venv
        ```

- Now that python3 is installed create your environment and activate it:

    ```
    $ make init
    $ source activate.sh
    ```

    You should **always** activate your environment when working on the project.

    If it fails with one of the following message :
    ```
    "ERROR: failed to create the .venv : do it yourself!"
    "ERROR: failed to activate virtual environment .venv! ask for advice on #dev "
    ```

## 2. Install the project requirements

```
$ make install
```

## 3. Check that everything is running properly.

The `Makefile` comes with useful features:

```
$ make help
help                           Show this help.
init                           initiate virtual environment
install                        install project dependencies (requirements.txt)
```

## 4. Train the model

The training could be launched with the following command line:

```
$ python forecast/application/train.py
```

Input datasets localizations can be specified with the -d (--DATA_INPUT) and -s (--SOCIO_ECO_INPUT) options:

```
$ python forecast/application/train.py -d path/to/data_file -s path/to/socio_eco_file
```

By default, datasets are read from `data/raw/data.csv` and `data/raw/socio_eco.csv` (see `forecast/settings/base.py`).

Model localization can be specified with the -m (--MODEL_OUTPUT) option:

```
$ python forecast/application/train.py -m path/to/model_file
```

By default, models are written to `models/model.joblib` (see `forecast/settings/base.py`).

A list of command line options can be obtained with the -h (--help) option:

```
$ python forecast/application/train.py -h
```

## 5. Make predictions

The predictions could be obtained with the following command line:

```
$ python forecast/application/predict.py
```

Input datasets localizations can be specified with the -d (--DATA_INPUT) and -s (--SOCIO_ECO_INPUT) options:

```
$ python forecast/application/predict.py -d path/to/data_file -s path/to/socio_eco_file
```

By default, datasets are read from `data/raw/data_without_target.csv` and `data/raw/socio_eco.csv` (see `forecast/settings/base.py`).

Model localization can be specified with the -m (--MODEL_INPUT) option:

```
$ python forecast/application/predict.py -m path/to/model_file
```

By default, models are read from `models/model.joblib` (see `forecast/settings/base.py`).

Predict dataset localization can be specified with the -p (--PREDICT__OUTPUT) option:

```
$ python forecast/application/predict.py -p path/to/predict_file
```

By default, predictions are written to `data/processed/data_socio_predict.csv` (see `forecast/settings/base.py`).

A list of command line options can be obtained with the -h (--help) option:

```
$ python forecast/application/predict.py -h
```
