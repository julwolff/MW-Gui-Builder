# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 22:51:23 2025

@author: jules
"""

from tkinter import ttk
from core.parameter_writer import search_molecule, instancie_molecules, instancie_species, instancie_electrodes, add_electrode_to_species,add_parameters,instancie_lj_pair, write_param_files

class GuiParameterGenerator:
    def __init__(self, master):
        
        
        self.notebook = master
        self.sim_type = 'NVT'
        
        #Generate tab for input and output separately


        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text='Input')
        self.notebook.add(self.tab2, text='Output')
        
        #INPUT
        
        #Label and entry

        self.temperature_label = ttk.Label(self.tab1, text='Enter temperature:')
        self.temperature_entry = ttk.Entry(self.tab1)

        self.timestep_label = ttk.Label(self.tab1, text='Enter number of step (1fs):')
        self.timestep_entry = ttk.Entry(self.tab1)
        
        self.filein_label = ttk.Label(self.tab1, text='Enter file to read:')
        self.filein_entry = ttk.Entry(self.tab1)
        
        self.pressure_label = ttk.Label(self.tab1, text='Enter pressure applied (no need if not NPT')
        self.pressure_entry = ttk.Entry(self.tab1)

        # Positioning the widgets using grid() method
        self.temperature_label.grid(row=0, column=0)
        self.temperature_entry.grid(row=0 , column=2)
        self.timestep_label.grid(row=1, column=0)
        self.timestep_entry.grid(row=1 , column=2)
        self.filein_entry.grid(row=0, column = 5)
        self.filein_label.grid(row=0, column = 3)
        self.pressure_label.grid(row=1, column = 3)
        self.pressure_entry.grid(row=1, column = 5)
        
        #Button to choose simtype

        self.button1 = ttk.Button(
            self.tab1, text='NVE', command=lambda: self.toggle_button(self.button1))
        self.button2 = ttk.Button(
            self.tab1, text='NVT', command=lambda: self.toggle_button(self.button2))
        self.button3 = ttk.Button(self.tab1, text='NPT', command=lambda: self.toggle_button(self.button3))

        # Launch button to write the param file
        self.launch_button = ttk.Button(self.tab1, text = 'Launch', command = self.launch)

        # Positioning the buttons using grid() method
        self.button1.grid(row=2,column = 0, columnspan=2)
        self.button2.grid(row=2, column = 2, columnspan=2)
        self.button3.grid(row = 2, column = 4, columnspan=2)
        self.launch_button.grid(row = 3, column = 2, columnspan=2)


        


    def toggle_button(self, button):
        # function to toggle the state of the buttons
        self.button1.state(['!pressed'])
        self.button2.state(['!pressed'])
        self.button3.state(['!pressed'])
        button.state(['pressed'])
        self.sim_type = button['text']

    def launch(self):
        
    
        # Retrieve user input for input
        
        filein = str(self.filein_entry.get())
        temperature = str(self.temperature_entry.get())
        pressure_applied = str(self.pressure_entry.get())
        time_step = str(self.timestep_entry.get())
        sim_type = str(self.sim_type)
        
        mols = search_molecule(filein)
        molecules = instancie_molecules(mols)
        species = instancie_species(molecules)
        electrodes = instancie_electrodes(mols, molecules)
        species = add_electrode_to_species(electrodes, species, filein)
        species, molecules=add_parameters(molecules, species, electrodes)
        lj_pairs = instancie_lj_pair(species)

        
        write_param_files(filein = filein,
                          pressure_applied= pressure_applied,
                          time_step = time_step,
                          sim_type = sim_type,
                          temperature=temperature, 
                          molecules=molecules, 
                          species=species,
                          electrodes=electrodes,
                          lj_pairs=lj_pairs,
                          output_list=[])

        print ("file written")
