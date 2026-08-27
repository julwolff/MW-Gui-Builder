#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 17:58:52 2025

@author: juleswolff
"""

import unittest
from core.generate_electrode_coords import pre_run, hexagonal, CFC100, CFC110, CFC111

class TestStructureGenerator(unittest.TestCase):

    def test_pre_run(self):
        nx, ny, nz = pre_run(2.0, 2.0, 3.0, 10, 12, 15)
        self.assertEqual(nx, 5)
        self.assertEqual(ny, 6)
        self.assertEqual(nz, 5)

    def test_hexagonal_output_range(self):
        coords = hexagonal(2.0, 1.0, 3.0, 5.0, 5.0, 5.0, 0.0)
        for x, y, z in coords:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertGreaterEqual(z, 0)
            self.assertLess(x, 6.0)
            self.assertLess(y, 6.0)
            self.assertLess(z, 5.0)

    def test_CFC100_output_range(self):
        coords = CFC100(2.0, 1.0, 2.0, 5.0, 5.0, 5.0, 0.0)
        for x, y, z in coords:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertGreaterEqual(z, 0)
            self.assertLess(x, 6.0)
            self.assertLess(y, 6.0)
            self.assertLess(z, 5.0)

    def test_CFC110_output_range(self):
        coords = CFC110(2.0, 1.0, 2.0, 5.0, 5.0, 5.0, 0.0)
        for x, y, z in coords:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertGreaterEqual(z, 0)
            self.assertLess(x, 6.0)
            self.assertLess(y, 6.0)
            self.assertLess(z, 5.0)

    def test_CFC111_output_range(self):
        coords = CFC111(2.0, 1.0, 2.0, 5.0, 5.0, 5.0, 0.0)
        for x, y, z in coords:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertGreaterEqual(z, 0)
            self.assertLess(x, 6.0)
            self.assertLess(y, 6.0)
            self.assertLess(z, 5.0)

    def test_atom_count_small_box(self):
        coords_100 = CFC100(2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 0.0)
        coords_110 = CFC110(2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 0.0)
        coords_111 = CFC111(2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 0.0)
        self.assertGreater(len(coords_100), 0)
        self.assertGreater(len(coords_110), 0)
        self.assertGreater(len(coords_111), 0)

if __name__ == '__main__':
    unittest.main()
