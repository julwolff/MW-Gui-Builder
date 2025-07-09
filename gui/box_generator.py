# -*- coding: utf-8 -*-
"""
Modern GUI for ElecSim Box Generator
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from core.generate_box import communicate_box_data, distinct_species, elongate_box, change_len_box


class GuiBoxGenerator:
    """Modern ttk GUI for generating molecular boxes."""

    def __init__(self, master):
        self.master = master
        master.title("ElecSim – Box Generator")

        self.molecule_list = []
        self.number_list = []

        # Setup ttk style
        style = ttk.Style()
        style.theme_use("clam")

        # Create GUI sections
        self.create_input_section()
        self.create_display_section()
        self.create_mode_buttons()
        self.create_size_input()
        self.create_box_shape_buttons()
        self.create_launch_button()

        # Flags
        self.density_selected = False
        self.border_selected = False
        self.box_selected = False
        self.cube_selected = False
        self.quarter_selected = False

    def create_input_section(self):
        frame = ttk.LabelFrame(self.master, text="Add Molecule")
        frame.pack(padx=10, pady=5, fill='x')

        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.molecule_entry = ttk.Entry(frame)
        self.molecule_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Count:").grid(row=0, column=2, padx=5)
        self.number_entry = ttk.Entry(frame)
        self.number_entry.grid(row=0, column=3)

        ttk.Button(frame, text="Add", command=self.add_number).grid(row=0, column=4, padx=5)
        ttk.Button(frame, text="Remove Last", command=self.remove_item).grid(row=0, column=5, padx=5)

    def create_display_section(self):
        frame = ttk.LabelFrame(self.master, text="Molecule List")
        frame.pack(padx=10, pady=5, fill='both')

        self.molecule_display = tk.Text(frame, height=5, state='disabled', wrap='none')
        self.molecule_display.pack(fill='both', padx=5, pady=5)

    def create_mode_buttons(self):
        frame = ttk.LabelFrame(self.master, text="Input Mode")
        frame.pack(padx=10, pady=5, fill='x')

        self.indication_message = ttk.Label(frame, text="Choose input mode:")
        self.indication_message.pack(pady=2)

        button_frame = ttk.Frame(frame)
        button_frame.pack()

        ttk.Button(button_frame, text="Density", command=self.select_density).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Box Size", command=self.select_border).pack(side='left', padx=5)

    def create_size_input(self):
        frame = ttk.Frame(self.master)
        frame.pack(padx=10, pady=5)

        ttk.Label(frame, text="Value (Density in mol/L or Dimensions in Å):").pack()
        self.size_entry = ttk.Entry(frame)
        self.size_entry.pack(fill='x', padx=5)

    def create_box_shape_buttons(self):
        frame = ttk.LabelFrame(self.master, text="Box Shape")
        frame.pack(padx=10, pady=5, fill='x')

        ttk.Button(frame, text="Double Z", command=self.select_box).pack(side='left', padx=5)
        ttk.Button(frame, text="Cube", command=self.select_cube).pack(side='left', padx=5)
        ttk.Button(frame, text="1:5 (Elongated Z)", command=self.select_quarter).pack(side='left', padx=5)

    def create_launch_button(self):
        self.launch_button = ttk.Button(self.master, text="Launch Generation", command=self.launch)
        self.launch_button.pack(pady=10)

    def add_number(self):
        mol = self.molecule_entry.get().strip()
        num = self.number_entry.get().strip()

        if not mol or not num:
            messagebox.showerror("Input Error", "Please provide both molecule name and quantity.")
            return
        try:
            int(num)
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a number.")
            return

        self.molecule_list.append(mol)
        self.number_list.append(num)

        self.update_molecule_display()
        self.molecule_entry.delete(0, 'end')
        self.number_entry.delete(0, 'end')

    def remove_item(self):
        if not self.molecule_list:
            messagebox.showinfo("Info", "No molecules to remove.")
            return

        removed = self.molecule_list.pop()
        self.number_list.pop()
        self.update_molecule_display()
        messagebox.showinfo("Removed", f"Removed last entry: {removed}")

    def update_molecule_display(self):
        self.molecule_display.config(state='normal')
        self.molecule_display.delete("1.0", "end")
        for mol, num in zip(self.molecule_list, self.number_list):
            self.molecule_display.insert("end", f"{mol} : {num}\n")
        self.molecule_display.config(state='disabled')

    def select_density(self):
        self.density_selected = True
        self.border_selected = False
        self.indication_message.config(text="Enter density in mol/L")

    def select_border(self):
        self.border_selected = True
        self.density_selected = False
        self.indication_message.config(text="Enter box size in Å (e.g., 40x40x40)")

    def select_cube(self):
        self.cube_selected = True
        self.box_selected = False
        self.quarter_selected = False
        messagebox.showinfo("Shape", "Cube shape selected.")

    def select_box(self):
        self.box_selected = True
        self.cube_selected = False
        self.quarter_selected = False
        messagebox.showinfo("Shape", "Double Z box selected.")

    def select_quarter(self):
        self.quarter_selected = True
        self.box_selected = False
        self.cube_selected = False
        messagebox.showinfo("Shape", "1:5 Z elongation selected.")

    def launch(self):
        if not self.molecule_list:
            messagebox.showerror("Error", "No molecules added.")
            return

        if not (self.density_selected or self.border_selected):
            messagebox.showerror("Error", "Please select an input mode (density or box size).")
            return

        # Construct fftool command
        command = "core/fftool"
        for mol, num in zip(self.molecule_list, self.number_list):
            command += f" {num} molecules/{mol}"

        if self.density_selected:
            command += f" -r {self.size_entry.get()}"
        elif self.border_selected:
            command += f" -b {self.size_entry.get()}"

        try:
            messagebox.showinfo("Running", "Generating box with fftool...")
            subprocess.call(command, shell=True)
            distinct_species(self.molecule_list)

            if self.box_selected:
                change_len_box()
            elif self.quarter_selected:
                elongate_box(5)

            messagebox.showinfo("Packmol", "Launching packmol...")
            subprocess.call("packmol < pack.inp", shell=True)
            communicate_box_data()

            messagebox.showinfo("Success", "Box generation complete.")
        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred:\n{str(e)}")
