#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from face_detection.infrastructure.loader import Loader


def main():
    """Launch the main process of algorithm training"""
    path = '/home/latitude/Documents/Yotta/2-Data_Science/Projet_2-CV_NLP/data/nude_face' # TODO replace by args
    loader = Loader(path)
    raw_images, labels = loader.get_raw_input()


if __name__ == "__main__":
    main()
