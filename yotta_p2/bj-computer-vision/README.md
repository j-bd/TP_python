# Masked Face Detection Project : Bénédicte and Jérome

Our work for this second project is to use some tools about computer vision, we decided mask detection for COVID-19 as a theme. The aim to this project is to detect if one wears or not a mask on several supports like an image, a video or a webcam.

## Architecture 
```
├── assignment                              <- File .PDF Project
│
├── data                                    <- Folder for input
│   ├── masked_face                         <- Folder containing images with masked face
│   └──  nude_face                          <- Folder containing images with unmasked face
│
├── logs                                    <- Folder with log files
│    ├── interpretability                   <- File for interpretabily of models
│    └── .gitignore                         <- Files .log ignored by git
│
├── masked_face                             <- Source code for use in this project
│   ├── application                         <- Folder containing the main project files
│   │    ├── predict.py                     <- File to make prediction
│   │    └── train.py                       <- File to make training data
│   │
│   ├── domain                              <- Folder containing the main project files
│   │    ├── data_augmentation.py           <- File to make data augmentation processing
│   │    ├── data_preparation.py            <- File to make basic transformations
│   │    ├── frame_detection.py             <- File to realize masked faces detection
│   │    ├── frame_preparation.py           <- File to make basic transformations
│   │    ├── model_evaluation.py            <- File to analyse model performance
│   │    ├── model_interpretability.py      <- File to produce interpretability of the model
│   │    ├── pipeline_detection.py          <- File to organize detection processing
│   │    └── run_selection.py               <- File to realize a training with validation/full dataset
│   │
│   ├── infrastructure                      <- Folder containing infrastructure part of the code
│   │    ├── command_line_parser.py         <- File to parse command line
│   │    ├── loader.py                      <- File to feed pipeline with initial data
│   │    ├── model_creation.py              <- File to create model structure and an other model to monitor training
│   │    └── predict_models_loading.py      <- File to retrieve models
│   │
│   ├── interface                           <- Folder to visualize prediction
│   │    └── streamlit.py                   <- Mini App to visualize some images, video
│   │
│   └── settings                            <- Folder containing variables
│        └── base.py                        <- Contains path/to/file images, models.
│
├── models                                  <- Folder for models
│   ├── classifier                          <- Folder containing models for classification
│   └── detector                            <- Folder containing prototext/caffemodel file for detection
│
│
├── .gitignore                              <- Files that should be ignored by git.
│
├── activate.sh                             <- Activate the python environment.
│
├── init.sh                                 <- Create a virtual environment.
│
├── Makefile                                <- Makefile with commands like `make init` or `make install`.
│
├── README.md                               <- The top-level README for developers using this project.
│
├── requirements.txt                        <- The requirements file for reproducing analysis environment,
│                                               e.g. generated with `pip freeze > requirements.txt`.
│
└── setup.py                                <- Makes project pip installable `pip install -e .`
                                               so forecast can be imported.
```

## Getting Starting

### 0. Clone this repository
```
$ git clone https://gitlab.com/yotta-academy/cohort-2020/projects/dl-projects/bj-computer-vision.git
$ cd bj-computer-vision
```
### 1. Setup your virtual environment and activate it
Before setting up your virtual environment, you must check your current **python version**. 
```
$ python3 --version
# examples of outputs:
Python 3.6.2 :: Anaconda, Inc.
Python 3.7.2
```
```
$ which python3
/Users/benedicte/anaconda3/bin/python3
/usr/bin/python3
```

Now that python3 is installed create your environment and activate it:
```
$ source init.sh
$ source activate.sh
```

### 2. Run for installing dependencies
```
$ make install

```
### 3. Check that everything is running properly.

The `Makefile` comes with useful features:

```
$ make help
help                           Show this help.
init                           initiate virtual environment
install                        install project dependencies (requirements.txt)
```

### 4. Training model
A list of command line options can be obtained with the -h (--help) option:

```
$ python masked_face/application/train.py -h
```

The training could be launched with the following command line:
```
$ python masked_face/application/train.py --data_input 'path/to/dir' --step_training True --model_type 'MobileNetV2'
```

**--data_input**: the directory must contains two directory gathering images. One
called 'masked_face' and the other one 'nude_face'. By default, the master
directory is 'raw' in 'data'.

**--step_training**: offer the possibility to train with train, validation and test
dataset. If set to 'False', training will be done on the full dataset

**--model_type**: 3 types of models are offered 'MobileNetV2', 'VGG16', 'Xception'.
If you want to add an other keras model, please add the new model entry images
size in the constant 'IMAGE_SIZE' located in 'masked_face/settings/base.py'

### 5. Predict model
A list of command line options can be obtained with the -h (--help) option:

```
$ python masked_face/application/predict.py -h

```

The prediction could be launched with the following command line:
```
$ python masked_face/application/predict.py --type_detection 'video'
    --path_video 'path/to/video.mp4' --classifier_type 'MobileNetV2

```
```
$ python masked_face/application/predict.py --type_detection 'image'
    --path_image 'path/to/image.jpg' --classifier_type 'MobileNetV2'
```
**--type_detection**: 3 types of detection are offered 'image', 'video', 'webcam'.

**--path_video**: full path to your video

**--classifier_type**: 3 types of classifiers are offered 'MobileNetV2', 'VGG16',
'Xception'.


### 6. Mini App : Streamlit
This application could be run with the following command line:
```
$ streamlit run masked_face/interface/streamlit_interface.py
```




