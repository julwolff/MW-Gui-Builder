# -*- coding: utf-8 -*-
"""
Box Generator GUI for ElecSim
Author: Jules
Date: 2025-06

This interface allows the user to:
- Select molecules and number of each
- Choose between density or box size input
- Generate a PACKMOL-ready input file using fftool
- Modify the resulting box size or elongate the z dimension
"""

import tkinter as tk
import subprocess
from core.generate_box import communicate_box_data, distinct_species, elongate_box, change_len_box


class GuiBoxGenerator:
    """Tkinter GUI for generating molecular boxes using fftool and packmol."""

    def __init__(self, master):
        self.master = master
        master.title("Box Generator")

        self.molecule_list = []
        self.number_list = []
        self.molecule_display = ""

        # Create GUI layout
        self.create_input_section()
        self.create_display_section()
        self.create_mode_buttons()
        self.create_size_inputs()
        self.create_box_shape_buttons()
        self.create_launch_button()

        # Mode and shape flags
        self.density_selected = False
        self.border_selected = False
        self.box_selected = False
        self.cube_selected = False
        self.quarter_selected = False

    def create_input_section(self):
        """Input fields for molecule name and count."""
        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack()

        tk.Label(self.input_frame, text="Enter molecule name:").pack(side='left')
        self.molecule_entry = tk.Entry(self.input_frame)
        self.molecule_entry.pack(side='left')

        tk.Label(self.input_frame, text="Enter molecule number:").pack(side='left')
        self.number_entry = tk.Entry(self.input_frame)
        self.number_entry.pack(side='left')

        tk.Button(self.input_frame, text="Add Item", command=self.add_number).pack(side='left')
        tk.Button(self.input_frame, text="Remove Item", command=self.remove_item).pack(side='left')

    def create_display_section(self):
        """Display list of added molecules."""
        self.display_frame = tk.Frame(self.master)
        self.display_frame.pack()
        self.molecule_list_label = tk.Label(self.display_frame, text="")
        self.molecule_list_label.pack(side='right')
        self.number_list_label = tk.Label(self.display_frame, text="")
        self.number_list_label.pack(side='left')

    def create_mode_buttons(self):
        """Choose between density or box size input."""
        self.operation_frame = tk.Frame(self.master)
        self.operation_frame.pack()

        self.indication_frame = tk.Frame(self.master)
        self.indication_frame.pack()
        self.indication_message = tk.Label(self.indication_frame, text="Please select your mode")
        self.indication_message.pack()

        tk.Button(self.operation_frame, text="Density", command=self.select_density).pack(side='left')
        tk.Button(self.operation_frame, text="Border", command=self.select_border).pack(side='left')

    def create_size_inputs(self):
        tk.Label(self.master, text="Enter size or density value:").pack()
        self.size_entry = tk.Entry(self.master)
        self.size_entry.pack()

    def create_box_shape_buttons(self):
        tk.Button(self.operation_frame, text="double z", command=self.select_box).pack()
        tk.Button(self.operation_frame, text="cube", command=self.select_cube).pack()
        tk.Button(self.operation_frame, text="1:5", command=self.select_quarter).pack()

    def create_launch_button(self):
        self.launch_button = tk.Button(self.master, text="Launch", command=self.launch)
        self.launch_button.pack()

    def add_number(self):
        """Add molecule and number to the internal list and update display."""
        mol = self.molecule_entry.get()
        num = self.number_entry.get()

        if not mol or not num:
            print("Error: Molecule name and number must be provided.")
            return

        self.molecule_list.append(mol)
        self.number_list.append(num)
        self.molecule_display += f"\n{mol} {num}"
        self.molecule_list_label.config(text=self.molecule_display)
        self.molecule_entry.delete(0, 'end')
        self.number_entry.delete(0, 'end')

    def remove_item(self):
        """Remove the last added molecule from the list and update display."""
        if self.molecule_list:
            self.molecule_list.pop()
            self.number_list.pop()
            lines = self.molecule_display.strip().split('\n')
            lines.pop()
            self.molecule_display = "\n".join(lines)
            self.molecule_list_label.config(text=self.molecule_display)

    def select_density(self):
        self.density_selected = True
        self.border_selected = False
        self.indication_message.config(text="Write density in mol/L")

    def select_border(self):
        self.border_selected = True
        self.density_selected = False
        self.indication_message.config(text="Write box dimensions in angströms")

    def select_cube(self):
        self.cube_selected = True
        self.box_selected = False
        self.quarter_selected = False

    def select_box(self):
        self.box_selected = True
        self.cube_selected = False
        self.quarter_selected = False

    def select_quarter(self):
        self.quarter_selected = True
        self.box_selected = False
        self.cube_selected = False

    def launch(self):
        """Run fftool and packmol based on selected options."""
        self.wip_label = tk.Label(self.master, text='Running...')
        self.wip_label.pack()
        print("Starting fftool process...")

        # Build fftool command
        command = "./fftool"
        for mol, num in zip(self.molecule_list, self.number_list):
            command += f" {num} molecules/{mol}"

        if self.density_selected:
            command += f" -r {self.size_entry.get()}"
        elif self.border_selected:
            command += f" -b {self.size_entry.get()}"

        print(f"Running: {command}")
        subprocess.call(command, shell=True)

        # Post-process
        distinct_species(self.molecule_list)

        if self.box_selected:
            print("Applying double z box...")
            change_len_box()
        elif self.quarter_selected:
            print("Applying 5x elongation in z...")
            elongate_box(5)

        print("Running packmol...")
        subprocess.call("packmol < pack.inp", shell=True)

        communicate_box_data()

        self.wip_label.config(text='Done')
        print("Box generation complete.")
