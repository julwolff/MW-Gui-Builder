# -*- coding: utf-8 -*-
"""
GUI Tool to convert .xyz files to MetalWalls .inp format

Created on Wed Jun  4 22:44:59 2025
@author: jules

This script creates a tkinter-based GUI that allows the user to input a `.xyz` file,
automatically compute box dimensions, format the data, and output a MetalWalls-compatible `.inp` file.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Core functions for processing
from core.xyz2inp import mw_file_writting
from core.xyz2inp import extract_lines_as_a_list
from core.xyz2inp import formate_lines
from core.xyz2inp import convert_list_from_int_to_string

class GuiConverter:
    def __init__(self, master):
        self.master = master
        master.title("Converter to MetalWalls (.inp)")

        # Frame for input fields
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=10)

        # Input file label + entry
        self.file_label_1 = tk.Label(self.input_frame, text="Input .xyz file:")
        self.file_label_1.pack()
        self.file_entry_1 = tk.Entry(self.input_frame, width=50)
        self.file_entry_1.pack()
        
        # Output file label + entry
        self.file_label_2 = tk.Label(self.input_frame, text="Output .inp file name:")
        self.file_label_2.pack()
        self.file_entry_2 = tk.Entry(self.input_frame, width=50)
        self.file_entry_2.pack()

        # Launch button
        self.operation_frame = tk.Frame(master)
        self.operation_frame.pack(pady=10)
        self.launch_button = tk.Button(self.operation_frame, text="Convert", command=self.launch)
        self.launch_button.pack()

    def launch(self):
        """
        Called when user clicks the "Convert" button.
        Parses the input file, calculates the simulation box, formats the data,
        and writes the output .inp file.
        """
        ANG_TO_BOHR_CONV = 1.890
        MARGIN = 1.0

        # Get file paths from input
        input_file = self.file_entry_1.get().strip()
        output_file = self.file_entry_2.get().strip()

        # Check for empty fields
        if not input_file or not output_file:
            messagebox.showerror("Error", "Please provide both input and output file names.")
            return

        # Check if input file exists
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"Input file '{input_file}' not found.")
            return

        try:
            # Read atomic coordinates from input file
            with open(input_file, 'r') as file:
                lines = file.readlines()

            x, y, z = [], [], []
            for i in range(2, len(lines)):
                tokens = lines[i].split()
                if len(tokens) < 4:
                    raise ValueError(f"Line {i+1} does not contain valid atomic coordinates.")
                x.append(float(tokens[1]))
                y.append(float(tokens[2]))
                z.append(float(tokens[3]))

            # Calculate box dimensions
            x_box = (max(x) + MARGIN) * ANG_TO_BOHR_CONV
            y_box = (max(y) + MARGIN) * ANG_TO_BOHR_CONV
            z_box = (max(z) + MARGIN) * ANG_TO_BOHR_CONV

            atom_number = int(lines[0].split()[0])

            try:
                electrode_atom_number = int(lines[1].split()[8])
            except (IndexError, ValueError):
                messagebox.showwarning("Warning", "Electrode atom number not found. Defaulting to 0.")
                electrode_atom_number = 0

            # Prepare header and formatted data
            formated_header = convert_list_from_int_to_string([atom_number,
                                                               electrode_atom_number,
                                                               x_box,
                                                               y_box,
                                                               z_box])

            list_of_atom_coordinates = extract_lines_as_a_list(input_file)
            formated_atom_list = formate_lines(list_of_atom_coordinates)

            # Write the .inp file
            mw_file_writting(input_file, output_file, formated_header, formated_atom_list)

            # Notify user
            messagebox.showinfo("Success", f"File converted successfully to '{output_file}'.")
        
        except Exception as e:
            messagebox.showerror("Conversion Error", f"An error occurred during conversion:\n{e}")
            return
