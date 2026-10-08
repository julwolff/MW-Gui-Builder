#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 17:58:52 2025

@author: juleswolff
"""

import unittest
from mw_gui_builder.core.generate_electrode_coords import pre_run, hexagonal, CFC100, CFC110, CFC111
from mw_gui_builder.core.electrode_generator import electrode_loading
from importlib.resources import files

class TestElectrodeDatabase(unittest.TestCase):

    def setUp(self):
        self.electrodes = electrode_loading()

    def test_database_is_not_empty(self):
        """The electrode database must contain at least one electrode."""
        self.assertGreater(len(self.electrodes), 0)

    def test_required_electrodes_are_available(self):
        """Check that the default electrode database contains the supported electrodes."""
        expected = [
            "C",
            "Pt(100)",
            "Pt(110)",
            "Pt(111)",
        ]

        available = [electrode.name for electrode in self.electrodes]

        for name in expected:
            self.assertIn(name, available)

    def test_electrode_parameters_are_positive(self):
        """All physical and model parameters must be positive."""
        for electrode in self.electrodes:
            self.assertGreater(float(electrode.a), 0)
            self.assertGreater(float(electrode.b), 0)
            self.assertGreater(float(electrode.c), 0)
            self.assertGreater(float(electrode.mass), 0)
            self.assertGreater(float(electrode.epsilon), 0)
            self.assertGreater(float(electrode.sigma), 0)
            self.assertGreater(float(electrode.gaussian_width), 0)
            self.assertGreater(float(electrode.Tf), 0)
            self.assertGreater(float(electrode.voronoi), 0)

    def test_fcc_electrodes_have_supported_geometry(self):
        """FCC electrodes must use one of the supported surface geometries."""
        supported = {
            "CFC(100)",
            "CFC(110)",
            "CFC(111)",
        }

        for electrode in self.electrodes:
            if electrode.name != "C":
                self.assertIn(electrode.geom, supported)

    def test_platinum_parameters(self):
        """Check the reference lattice and mass values for platinum."""
        expected = {
            "Pt(100)": (3.923, 106.42),
            "Pt(110)": (3.923, 106.42),
            "Pt(111)": (3.923, 106.42),
        }

        for name, (lattice, mass) in expected.items():
            electrode = next(
                electrode
                for electrode in self.electrodes
                if electrode.name == name
            )

            self.assertAlmostEqual(float(electrode.a), lattice)
            self.assertAlmostEqual(float(electrode.mass), mass)

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

class TestPackagedData(unittest.TestCase):

    def test_electrode_database_file_is_packaged(self):
        """The electrode database must be available from the installed package."""
        electrode_file = files(
            "mw_gui_builder"
        ).joinpath("data", "electrode.txt")

        self.assertTrue(electrode_file.is_file())

if __name__ == '__main__':
    unittest.main()

