# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 22:48:46 2025
@author: jules
"""

from tkinter import ttk
from tkinter import StringVar
from core.electrode_generator import electrode_loading, determin_box_size, insert_electrode
from core.generate_electrode_coords import hexagonal, CFC100, CFC111, CFC110

class GuiElectrodeBuilder:
    """
    GUI for generating electrode files based on user-selected material, dimensions, and geometry.
    """

    def __init__(self, master):
        """
        Initialize the GUI components and load available electrode materials.
        """
        self.master = master
        master.title("Electrode Generator")

        self.electrodes = electrode_loading()
        self.options = [e.name for e in self.electrodes]
        self.selected_electrode = StringVar(value=self.options[0])
        self.selected_electrode.trace("w", self.option_selected)

        self.size_x = 0
        self.size_y = 0

        # Frame to group all input widgets
        self.frame = ttk.Frame(master, padding=10)
        self.frame.grid(row=0, column=0, columnspan=2)

        # Output filename
        ttk.Label(self.frame, text="Output file name:").grid(row=0, column=0, columnspan=2)
        self.filename_entry = ttk.Entry(self.frame)
        self.filename_entry.grid(row=1, column=0, columnspan=2)

        # Electrode material selection
        ttk.Label(self.frame, text="Choose electrode material:").grid(row=2, column=0)
        self.option_menu = ttk.OptionMenu(self.frame, self.selected_electrode, self.options[0], *self.options)
        self.option_menu.grid(row=2, column=1)

        # Electrode name
        ttk.Label(self.frame, text="Electrode name:").grid(row=3, column=0, columnspan=2)
        self.electrode_name_entry = ttk.Entry(self.frame)
        self.electrode_name_entry.grid(row=4, column=0, columnspan=2)

        # Electrode position
        ttk.Label(self.frame, text="Electrode position (Z-axis):").grid(row=5, column=0, columnspan=2)
        self.electrode_position_entry = ttk.Entry(self.frame)
        self.electrode_position_entry.grid(row=6, column=0, columnspan=2)

        # Z-dimension
        ttk.Label(self.frame, text="Z dimension:").grid(row=7, column=0, columnspan=2)
        self.z_dimension_entry = ttk.Entry(self.frame)
        self.z_dimension_entry.grid(row=8, column=0, columnspan=2)

        # Buffer (currently unused but kept for potential future use)
        ttk.Label(self.frame, text="Buffer:").grid(row=9, column=0, columnspan=2)
        self.buffer_entry = ttk.Entry(self.frame)
        self.buffer_entry.grid(row=10, column=0, columnspan=2)

        # Launch button
        self.launch_button = ttk.Button(self.frame, text="Launch", command=self.launch)
        self.launch_button.grid(row=11, column=0, columnspan=2)

        # Success label (hidden initially)
        self.done_label = ttk.Label(self.frame, text="✅ Electrode inserted successfully!")

    def option_selected(self, *args):
        """
        Called when a new electrode material is selected. Updates the internal parameters accordingly.
        """
        index = self.options.index(self.selected_electrode.get())
        elec = self.electrodes[index]
        self.name = elec.name
        self.geom = elec.geom
        self.a = elec.a
        self.b = elec.b
        self.c = elec.c
        self.mass = elec.mass
        self.epsilon = elec.epsilon
        self.sigma = elec.sigma
        self.gaussian_width = elec.gaussian_width
        self.Tf = elec.Tf
        self.voronoi = elec.voronoi
        print(f"[INFO] Selected electrode: {self.name}, geometry: {self.geom}")

    def launch(self):
        """
        Collect user inputs, compute electrode geometry, and write output files.
        """
        try:
            filename = self.filename_entry.get()
            electrode_name = self.electrode_name_entry.get()
            z_position = float(self.electrode_position_entry.get())
            z_dimension = float(self.z_dimension_entry.get())
            buffer = float(self.buffer_entry.get())

            # Save .els file
            with open(f"molecules/electrode_{electrode_name}.els", 'w') as file:
                file.write(f"{self.name} {self.mass} {self.gaussian_width} {self.epsilon} {self.sigma} {self.Tf} {self.voronoi}")
            print(f"[INFO] .els file written for {electrode_name}")

            # Get box size from coordinate file
            if self.size_x == 0 and self.size_y == 0:
                self.size_x, self.size_y = determin_box_size(filename)
                print(f"[INFO] Box size determined: x = {self.size_x}, y = {self.size_y}")

            # Prepare geometry parameters
            elec_params = (
            float(self.a), float(self.b), float(self.c), 
            self.size_x, self.size_y, z_dimension, z_position
            )

            # Generate coordinates based on geometry
            if self.geom == "hexagonal":
                coords = hexagonal(*elec_params)
            elif self.geom == "CFC(100)":
                coords = CFC100(*elec_params)
            elif self.geom == "CFC(111)":
                coords = CFC111(*elec_params)
            elif self.geom == "CFC(110)":
                coords = CFC110(*elec_params)
            else:
                raise ValueError(f"Unknown geometry: {self.geom}")

            # Insert electrode into file
            insert_electrode(filename, coords, electrode_name, buffer)
            print(f"[SUCCESS] Electrode '{electrode_name}' inserted into '{filename}'")

            # Show done label
            self.done_label.grid(row=12, column=0, columnspan=2)

        except Exception as e:
            print(f"[ERROR] Failed to insert electrode: {e}")
