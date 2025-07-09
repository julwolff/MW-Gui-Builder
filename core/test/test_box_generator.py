#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 18:03:11 2025

@author: juleswolff
"""

import unittest
import os
import shutil
from io import StringIO
import sys

from core.generate_box import (
    distinct_species,
    change_len_box,
    elongate_box,
    communicate_box_data
)


class TestBoxUtils(unittest.TestCase):

    def setUp(self):
        os.makedirs("molecules", exist_ok=True)
        # Create dummy molecule packed files
        self.mol_files = ["mol1.xyz", "mol2.xyz"]
        content = "6\ncomment\nC 0 0 0\nC 1 1 1\nH 2 2 2\nH 3 3 3\nO 4 4 4\nO 5 5 5\n"
        for mol in self.mol_files:
            with open(f"molecules/{mol.split('.')[0]}_pack.xyz", "w") as f:
                f.write(content)

        # Create a dummy pack.inp file
        self.pack_inp_content = (
            "structure mol1.xyz\n"
            "  number 2\n"
            "  inside box 1.5000 1.5000 1.5000 15.0 15.0 15.0\n"
            "structure mol2.xyz\n"
            "  number 2\n"
            "  inside box 1.5000 1.5000 1.5000 15.0 15.0 15.0\n"
        )
        with open("pack.inp", "w") as f:
            f.write(self.pack_inp_content)


    def test_distinct_species(self):
        distinct_species(self.mol_files)
        # Check that new species names were written (e.g., C0, C1, H0, etc.)
        with open("molecules/mol1_pack.xyz", "r") as f:
            content = f.read()
            self.assertIn("C0", content)
            self.assertIn("H0", content)

    def test_change_len_box(self):
        change_len_box()
        with open("pack.inp", "r") as f:
            content = f.read()
        # Expected values from box length conversion
        self.assertIn("31.5", content)
        self.assertIn(".", content)  # Floating point presence

    def test_elongate_box(self):
        elongate_box(4)
        with open("pack.inp", "r") as f:
            content = f.read()
        self.assertIn("50.4", content)
        self.assertIn(".", content)

    def test_communicate_box_data(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        communicate_box_data()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("A box with dimensions", output)
        self.assertIn("place it at", output)
        
    # def tearDown(self):
    #     if os.path.exists("pack.inp"):
    #         os.remove("pack.inp")
    #     if os.path.exists("molecules"):
    #         shutil.rmtree("molecules")


if __name__ == "__main__":
    unittest.main()
