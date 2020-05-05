#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from face_detection.infrastructure.loader import Loader
from face_detection.data_preparation import ImagePreparation, LabelClassifier


def main():
    """Launch the main process of algorithm training"""
    path = '/home/latitude/Documents/Yotta/2-Data_Science/Projet_2-CV_NLP/data/nude_face'  # TODO replace by args
    training_opt = True  # TODO replace by args

    loader = Loader(path)
    raw_images, raw_labels = loader.get_raw_input()

    # Images preprocessing
    preprocessing = ImagePreparation(raw_images)
    images = preprocessing.process()

    # Labels Encoding
    encoder = LabelClassifier(raw_labels)
    labels = encoder.process()

    # Training to optimise the classifier
    if training_opt:


if __name__ == "__main__":
    main()
