# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 22:20:32 2025

@author: jules
"""

# main.py

import tkinter as tk
from tkinter import ttk
from gui.box_generator import GuiBoxGenerator
from gui.converter import GuiConverter
from gui.electrode_builder import GuiElectrodeBuilder
from gui.parameter_generator import GuiParameterGenerator

class ElecSimGui:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("GUI Builder")

        # Create a frame to center the buttons
        self.button_frame = tk.Frame(self.window, padx=20, pady=20)
        self.button_frame.pack(expand=True)

        # Create buttons without images, stacked vertically
        self.button1 = tk.Button(self.button_frame, text="Box Generation",
                                 command=self.launch_box_generator, width=30, height=2)
        self.button2 = tk.Button(self.button_frame, text="Format for MetalWalls",
                                 command=self.launch_converter, width=30, height=2)
        self.button3 = tk.Button(self.button_frame, text="Electrode Generator",
                                 command=self.launch_electrode_builder, width=30, height=2)
        self.button4 = tk.Button(self.button_frame, text="Parameter Generator",
                                 command=self.launch_parameter_generator, width=30, height=2)

        # Stack buttons vertically using pack
        self.button1.pack(pady=5)
        self.button2.pack(pady=5)
        self.button3.pack(pady=5)
        self.button4.pack(pady=5)

        self.window.mainloop()

    def launch_box_generator(self):
        window = tk.Toplevel(self.window)
        GuiBoxGenerator(window)

    def launch_converter(self):
        window = tk.Toplevel(self.window)
        GuiConverter(window)

    def launch_electrode_builder(self):
        window = tk.Toplevel(self.window)
        GuiElectrodeBuilder(window)

    def launch_parameter_generator(self):
        window = tk.Toplevel(self.window)
        notebook = ttk.Notebook(window)
        notebook.pack(expand=True, fill='both')
        GuiParameterGenerator(notebook)

if __name__ == "__main__":
    ElecSimGui()
