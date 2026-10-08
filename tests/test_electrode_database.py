
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 17:59:55 2025

@author: juleswolff
"""

import unittest
import os
from mw_gui_builder.core.xyz2inp import (
    extract_lines_as_a_list,
    formate_lines,
    convert_list_from_int_to_string,
    enlarge_box,
    mw_file_writting,
    sort_atom_by_species,
)

class TestConverterUtils(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_input.txt"
        with open(self.test_file, "w") as f:
            f.write("line 1\nline 2\nline 3")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("test_output.txt"):
            os.remove("test_output.txt")

    def test_extract_lines_as_a_list(self):
        lines = extract_lines_as_a_list(self.test_file)
        self.assertEqual(lines, ["line 1\n", "line 2\n", "line 3"])

    def test_formate_lines(self):
        input_lines = ["  H   0.0  0.1  0.2  ", "\tO  1.0 1.1 1.2\n"]
        result = formate_lines(input_lines)
        self.assertEqual(result, ["H 0.0 0.1 0.2", "O 1.0 1.1 1.2"])

    def test_convert_list_from_int_to_string(self):
        self.assertEqual(
            convert_list_from_int_to_string([1, 2, 3]), ["1", "2", "3"]
        )

    def test_enlarge_box(self):
        # Fake XYZ input list, with two header lines skipped
        input_atoms = [
            "comment line 1",
            "comment line 2",
            "H 1.0 1.0 1.0",
            "O 0.5 0.5 0.5",
        ]
        result = enlarge_box(input_atoms)
        self.assertEqual(len(result), 2)
        self.assertTrue(result[0].startswith("H"))
        self.assertIn("1.890", result[0])  # 1.0 * 1.89
        self.assertIn("0.945", result[1])  # 0.5 * 1.89

    def test_sort_atom_by_species(self):
        atoms = [
            "O 1.0 1.0 1.0",
            "H 0.0 0.0 0.0",
            "O 1.5 1.5 1.5",
            "H 0.5 0.5 0.5"
        ]
        sorted_atoms = sort_atom_by_species(atoms)
        # First all O, then all H
        self.assertEqual(sorted_atoms, [
            "O 1.0 1.0 1.0",
            "O 1.5 1.5 1.5",
            "H 0.0 0.0 0.0",
            "H 0.5 0.5 0.5"
        ])

    def test_mw_file_writting(self):
        coords = ["H 1.0 2.0 3.0", "O 4.0 5.0 6.0"]
        header = ["2", "0", "10.0", "10.0", "10.0"]
        mw_file_writting("fake_input", "test_output.txt", header, coords)
        with open("test_output.txt", "r") as f:
            lines = f.readlines()
        self.assertIn("H 1.0 2.0 3.0\n", lines)
        self.assertIn("O 4.0 5.0 6.0\n", lines)
        self.assertIn("num_atoms", lines[2])
        self.assertIn("num_electrode_atoms", lines[3])
        self.assertIn("10.0 10.0 10.0", lines[5])

if __name__ == "__main__":
    unittest.main()
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

from pathlib import Path

electrode_generator_path = (
    Path(__file__).parent.parent
    / "src"
    / "mw_gui_builder"
    / "core"
    / "electrode_generator.py"
)
exec(open(electrode_generator_path).read(), electrode_module.__dict__)

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


