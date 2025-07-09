#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 18:15:58 2025

@author: juleswolff
"""

import unittest
import numpy as np
from unittest.mock import patch, mock_open
from io import StringIO

# Import the original functions and classes (assuming saved as electrode_module.py)
import sys
import types
import os

# Simulate loading the module
electrode_module = types.ModuleType("electrode_module")
exec(open("../electrode_generator.py").read(), electrode_module.__dict__)


class TestElectrodeModule(unittest.TestCase):
    
    def setUp(self):
        with open("dummy.xyz", "w") as f:
            f.write("2\nComment\nH 0.0 0.0 0.0\nO 1.0 1.0 1.0\n")

    def tearDown(self):
        os.remove("dummy.xyz")

    
    def test_Electrode_options(self):
        """Test the initialization of Electrode_options class."""
        fields = ["Au", "sphere", "1", "2", "3", "196.97", "0.1", "2.5", "0.3", "300", "yes"]
        electrode = electrode_module.Electrode_options(fields)
        self.assertEqual(electrode.name, "Au")
        self.assertEqual(electrode.geom, "sphere")
        self.assertEqual(electrode.mass, "196.97")
        self.assertEqual(electrode.voronoi, "yes")

    def test_determin_box_size(self):
        """Test box size determination from mock file."""
        mock_data = "2\nComment\nH 0.0 0.0 0.0\nO 1.0 1.0 1.0\n"
        with patch.object(electrode_module, "open", mock_open(read_data=mock_data)):
            xmax, ymax = electrode_module.determin_box_size("dummy.xyz")
        self.assertAlmostEqual(xmax, 1.0 + 1.5)
        self.assertAlmostEqual(ymax, 1.0 + 1.5)


    def test_search_pattern(self):
        """Test molecular pattern recognition."""
        species = ["H0", "O0", "H1", "H0", "O0", "H1", "Na0", "Cl0","Na0", "Cl0"]
        mols, n_moles, species_recensed = electrode_module.search_pattern([], 0, species, [], first_time=True)
        # Expecting: one water molecule (H-O-H), one NaCl molecule
        self.assertEqual(n_moles, 2)
        self.assertIn("O0", mols[0])
        self.assertIn("Cl0", mols[1])

unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestElectrodeModule))

