#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:34:17 2020

@author: j-bd
"""
import cv2

from masked_face.domain.frame_detection import FrameDetection


class Pipeline:
    def __init__(self, model_detector, model_classifier, args):
        self.face_detection = model_detector
        self.face_classifier = model_classifier
        self.args = args

    def webcam_detection(self):
        detection = FrameDetection(
            self.face_detection, self.face_classifier, self.args
        )
        video_capture = cv2.VideoCapture(0)
        while True:
            # Read webcam capture
            ret, frame = video_capture.read()

            detection.launch_detection(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
