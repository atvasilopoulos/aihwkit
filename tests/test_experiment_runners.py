# -*- coding: utf-8 -*-

# (C) Copyright 2020, 2021 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for Experiment Runners."""

from io import StringIO
from unittest import skipIf
from unittest.mock import patch

from torch import device as torch_device
from aihwkit.experiments.runners.local import LocalRunner
from aihwkit.simulator.rpu_base import cuda

from .helpers.decorators import parametrize_over_models
from .helpers.experiments import (
    FullyConnectedFashionMNIST, FullyConnectedFashionMNISTTikiTaka,
    LeNet5FashionMNIST,
)
from .helpers.testcases import AihwkitTestCase


@parametrize_over_models([
    FullyConnectedFashionMNIST, FullyConnectedFashionMNISTTikiTaka,
    LeNet5FashionMNIST,
])
class TestLocalRunner(AihwkitTestCase):
    """Test LocalRunner."""

    def test_run_example_cpu(self):
        """Test running the example using a local runner."""
        training_experiment = self.get_experiment()
        local_runner = LocalRunner(device=torch_device('cpu'))

        with patch('sys.stdout', new=StringIO()) as captured_stdout:
            result = local_runner.run(training_experiment, max_elements_train=10)

        # Asserts over stdout.
        self.assertIn('Epoch: ', captured_stdout.getvalue())

        # Asserts over the returned results.
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['epoch'], 0)
        self.assertIn('train_loss', result[0])
        self.assertIn('accuracy', result[0])

    @skipIf(not cuda.is_compiled(), 'not compiled with CUDA support')
    def test_run_example_gpu(self):
        """Test running the example using a local runner."""
        training_experiment = self.get_experiment()
        local_runner = LocalRunner(device=torch_device('cuda'))

        with patch('sys.stdout', new=StringIO()) as captured_stdout:
            result = local_runner.run(training_experiment, max_elements_train=10)

        # Asserts over stdout.
        self.assertIn('Epoch: ', captured_stdout.getvalue())

        # Asserts over the returned results.
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['epoch'], 0)
        self.assertIn('train_loss', result[0])
        self.assertIn('accuracy', result[0])
