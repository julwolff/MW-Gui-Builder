# -*- coding: utf-8 -*-
"""
GUI Tool to generate parameter files for MetalWalls

Refactored on Mon Jun 30 2025 by ChatGPT
"""

import tkinter as tk
from tkinter import ttk, messagebox

from core.parameter_writer import (
    search_molecule,
    instancie_molecules,
    instancie_species,
    instancie_electrodes,
    add_electrode_to_species,
    add_parameters,
    instancie_lj_pair,
    write_param_files,
)


class GuiParameterGenerator:
    """Graphical interface to generate MetalWalls parameter files."""

    def __init__(self, master: ttk.Notebook):
        self.notebook = master
        self.sim_type = "NVT"

        self._init_tabs()
        self._build_input_tab()

    def _init_tabs(self):
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Input")
        self.notebook.add(self.tab2, text="Output")

    def _build_input_tab(self):
        # Labels & entries
        self.temperature_var = tk.StringVar()
        self.timestep_var = tk.StringVar()
        self.filein_var = tk.StringVar()
        self.pressure_var = tk.StringVar()

        ttk.Label(self.tab1, text="Temperature (K):").grid(row=0, column=0, sticky="w")
        ttk.Entry(self.tab1, textvariable=self.temperature_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.tab1, text="Simulation steps (1 fs):").grid(row=1, column=0, sticky="w")
        ttk.Entry(self.tab1, textvariable=self.timestep_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.tab1, text="Input file:").grid(row=0, column=2, sticky="w")
        ttk.Entry(self.tab1, textvariable=self.filein_var).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.tab1, text="Pressure (bar) [if NPT]:").grid(row=1, column=2, sticky="w")
        ttk.Entry(self.tab1, textvariable=self.pressure_var).grid(row=1, column=3, padx=5, pady=5)

        # Simulation type buttons
        ttk.Label(self.tab1, text="Simulation type:").grid(row=2, column=0, sticky="w", pady=10)

        self.sim_buttons = {}
        for i, mode in enumerate(["NVE", "NVT", "NPT"]):
            btn = ttk.Button(self.tab1, text=mode, command=lambda m=mode: self.toggle_sim_type(m))
            btn.grid(row=2, column=1 + i, padx=5)
            self.sim_buttons[mode] = btn

        self.toggle_sim_type("NVT")  # default

        # Launch button
        ttk.Button(self.tab1, text="Generate Parameters", command=self.launch).grid(
            row=3, column=1, columnspan=2, pady=15
        )

    def toggle_sim_type(self, sim_type: str):
        """Highlights the selected simulation type and stores it."""
        self.sim_type = sim_type
        for mode, btn in self.sim_buttons.items():
            btn.state(["!pressed"])
        self.sim_buttons[sim_type].state(["pressed"])

    def launch(self):
        """Collects user input and writes the parameter files."""

        filein = self.filein_var.get().strip()
        temperature = self.temperature_var.get().strip()
        pressure_applied = self.pressure_var.get().strip()
        time_step = self.timestep_var.get().strip()

        # Basic validation
        if not all([filein, temperature, time_step]):
            messagebox.showerror("Error", "Please fill in the required fields (file, temperature, timestep).")
            return

        try:
            
            print('Searching molecules')
            mols = search_molecule(filein)
            print('Instancie the molecules')
            molecules = instancie_molecules(mols)
            print('Instancie species')
            species = instancie_species(molecules)
            print('Instancie electrodes')
            electrodes = instancie_electrodes(mols, molecules)
            print('Add electrode to species list')
            species = add_electrode_to_species(electrodes, species, filein)
            print('Add parameters')
            species, molecules = add_parameters(molecules, species, electrodes)
            print('Write Lennard-Jones parameters')
            lj_pairs = instancie_lj_pair(species)
            
            print('Write runtime.inpt file')

            write_param_files(
                filein=filein,
                pressure_applied=pressure_applied,
                time_step=time_step,
                sim_type=self.sim_type,
                temperature=temperature,
                molecules=molecules,
                species=species,
                electrodes=electrodes,
                lj_pairs=lj_pairs,
                output_list=[],
            )

            messagebox.showinfo("Success", "The parameter file was successfully generated.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
