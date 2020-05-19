#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to make predictions.

Example
-------
Script could be run with the following command line

    $ streamlit run ../masked_face/interface/streamlit_interface.py
"""
import streamlit as st

from masked_face.application.predict import main


def streamlit_interface():
    """Face Detection App"""

    st.title("Masked Face Detection ")
    st.text("Build by Bénédicte and Jérôme")

    type_detection = ["image", "video", "webcam"]
    td_choice = st.sidebar.selectbox("Select your support", type_detection)

    classifier_type = ['MobileNetV2', 'VGG16', 'Xception']
    ct_choice = st.sidebar.selectbox("Select your support", classifier_type)

    if td_choice == 'image':
        st.subheader("Image Detection")
        path = st.text_input('Enter a file path:')
        if path is not None and st.button("Process"):
            args = {
                'type_detection': td_choice, 'classifier_type': ct_choice,
                'confidence': 0.5, 'devmode': False, 'path_image': path,
                'path_video': None, 'streamlit': True
            }
            main(args)

    elif td_choice == 'video':
        st.subheader("Video Detection")
        path = st.text_input('Enter a file path:')
        if path is not None and st.button("Process"):
            args = {
                'type_detection': td_choice, 'classifier_type': ct_choice,
                'confidence': 0.5, 'devmode': False, 'path_image': None,
                'path_video': path, 'streamlit': True
            }
            main(args)

    elif td_choice == 'webcam':
        st.subheader("Webcam Detection")
        args = {
            'type_detection': td_choice, 'classifier_type': ct_choice,
            'confidence': 0.5, 'devmode': False, 'path_image': None,
            'path_video': None, 'streamlit': True
        }
        main(args)


if __name__ == '__main__':
    streamlit_interface()
