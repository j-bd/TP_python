#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from tf_explain.core.activations import ExtractActivations
from tf_explain.core.vanilla_gradients import VanillaGradients
from tf_explain.core.gradients_inputs import GradientsInputs
from tf_explain.core.occlusion_sensitivity import OcclusionSensitivity
from tf_explain.core.grad_cam import GradCAM
from tf_explain.core.smoothgrad import SmoothGrad
from tf_explain.core.integrated_gradients import IntegratedGradients

from masked_face.settings import base
from masked_face.domain.data_preparation import DataPreprocessing


class Interpretability:
    """
    """
    def __init__(self, model, x_set, y_set, args):
        """
        """
        self.model = model
        self.x_set = x_set
        self.y_set = y_set
        self.args = args
        self.dir = base.INTERPRETABILITY

    def get_interpretability_results(self):
        """
        """
        preprocess = DataPreprocessing(self.x_set[0:6], self.y_set[0:6], self.args)
        self.x_val, self.y_val, self.label_cl = preprocess.apply_preprocessing()

        explainer = ExtractActivations()
        # Compute Activations of layer activation_1
        grid = explainer.explain(
            (self.x_val, self.y_val), self.model, 'Conv_1'
        )
        explainer.save(grid, self.dir, "activations.png")

        class_index = [0, 1]
        for idx in class_index:
            explainer = VanillaGradients()
            # Compute VanillaGradients on VGG16
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, idx)
            explainer.save(grid, self.dir, str(idx) + "vanilla_gradients.png")

        class_index = [0, 1]
        for idx in class_index:
            explainer = GradientsInputs()
            # Compute GradientsInputs on VGG16
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, idx)
            explainer.save(grid, self.dir, str(idx) + "gradients_inputs.png")

        class_index = [0, 1]
        for idx in class_index:
            explainer = OcclusionSensitivity()
            # Compute Occlusion Sensitivity for patch_size 20
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, idx, 20)
            explainer.save(grid, self.dir, str(idx) + "occlusion_sensitivity_20.png")
            # Compute Occlusion Sensitivity for patch_size 10
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, idx, 10)
            explainer.save(grid, self.dir, str(idx) + "occlusion_sensitivity_10.png")

        class_index = [0, 1]
        for idx in class_index:
            explainer = GradCAM()
            # Compute GradCAM on VGG16
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, class_index=idx,
                layer_name="Conv_1"
            )
            explainer.save(grid, self.dir, str(idx) + "grad_cam.png")

        class_index = [0, 1]
        for idx in class_index:
            explainer = SmoothGrad()
            # Compute SmoothGrad on VGG16
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, idx, 20, 1.0)
            explainer.save(grid, self.dir, str(idx) + "smoothgrad.png")

        class_index = [0, 1]
        for idx in class_index:
            explainer = IntegratedGradients()
            # Compute SmoothGrad on VGG16
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, idx, n_steps=15)
            explainer.save(grid, self.dir, str(idx) + "integrated_gradients.png")
