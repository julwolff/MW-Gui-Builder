# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 22:48:46 2025

@author: jules
"""


import tkinter as tk
from core.electrode_generator import electrode_loading, determin_box_size, insert_electrode

import math

class GuiElectrodeBuilder:

    def __init__(self,master):
        
        #load electrode options
                
        self.electrodes = electrode_loading()
        
        
        self.master=master
        master.title("Electrode Generator")
    
        #Create Frame for Entry        
        self.entrance_frame=tk.Frame(master)
        self.entrance_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
        #Create label and entry for outputfile
        self.filename_label=tk.Label(self.entrance_frame, text="Enter output file name")
        self.filename_label.grid(row=0, column=0, columnspan=2)
        self.filename_entry=tk.Entry(self.entrance_frame)
        self.filename_entry.grid(row=1, column=0, columnspan=2)
    
        # Create a StringVar variable
        self.selected_electrode = tk.StringVar()
    
        # Create a list of options and initialize
        self.options = [i.name for i in self.electrodes]
        self.selected_electrode.set(self.options[0])
    
        # Create the OptionMenu widget
        self.option_label=tk.Label(self.entrance_frame, text="Choose electrode material")
        self.option_label.grid(row=2, column=0)
        self.option_menu = tk.OptionMenu(self.entrance_frame, self.selected_electrode, *self.options)
        self.option_menu.grid(row=2, column=1)
        
    
        
    
        
        
    
    
        #Create label and entry for electrode name
        self.electrode_name_label=tk.Label(self.entrance_frame, text="Give a name to the electrode")
        self.electrode_name_label.grid(row=8, column=0, columnspan=2)
        self.electrode_name_entry=tk.Entry(self.entrance_frame)
        self.electrode_name_entry.grid(row=9, column=0, columnspan=2)
    
        #Create a label and entry for the electrode position
        self.electrode_position_label=tk.Label(self.entrance_frame, text="Electrode position (z axes)")
        self.electrode_position_label.grid(row=10, column=0, columnspan=2)
        self.electrode_position_entry=tk.Entry(self.entrance_frame)
        self.electrode_position_entry.grid(row=11, column=0, columnspan=2)
    
    
        #Create label and entry for z dimension
        self.z_dimension_label=tk.Label(self.entrance_frame, text="Enter z dimension")
        self.z_dimension_label.grid(row=16, column=0, columnspan=2)
        self.z_dimension_entry=tk.Entry(self.entrance_frame)
        self.z_dimension_entry.grid(row=17, column=0, columnspan=2)
        
        #Create label and entry for buffzer
        self.buffer_label=tk.Label(self.entrance_frame, text="Enter buffer")
        self.buffer_label.grid(row=18, column=0, columnspan=2)
        self.buffer_entry=tk.Entry(self.entrance_frame)
        self.buffer_entry.grid(row=19, column=0, columnspan=2)
    
        #Create a launch button
        self.launch_button=tk.Button(self.entrance_frame, text = "Launch", command=self.launch)
        self.launch_button.grid(row=20, column=0, columnspan=2)
    
        #Create a done label 
        self.wip_label=tk.Label(self.entrance_frame, text='Done')
    
        # Bind the function to the variable
        self.selected_electrode.trace("w", self.option_selected)
        
                    
        self.size_x = 0
        self.size_y = 0
        
    
    def option_selected(self,*args):
        
        #Determined selected electrode
        
        
        electrode_index = [electrode.name for electrode in self.electrodes].index(self.selected_electrode.get())
        
        self.name = self.electrodes[electrode_index].name
        self.geom = self.electrodes[electrode_index].geom
        self.a = self.electrodes[electrode_index].a
        self.b = self.electrodes[electrode_index].b
        self.c = self.electrodes[electrode_index].c
        self.mass = self.electrodes[electrode_index].mass
        self.epsilon = self.electrodes[electrode_index].epsilon
        self.sigma = self.electrodes[electrode_index].sigma
        self.gaussian_width = self.electrodes[electrode_index].gaussian_width
        self.Tf = self.electrodes[electrode_index].Tf
        self.voronoi = self.electrodes[electrode_index].voronoi
    
            
    # Define the launch button function
    def launch(self):
        # Store electrode parameters in a file
        with open(f"molecules/electrode_{self.electrode_name_entry.get()}.els", 'w') as file:
            file.write(
                str(self.name) + " " +
                str(self.mass) + " " +
                str(self.gaussian_width) + " " +
                str(self.epsilon) + " " +
                str(self.sigma)
            )
    
        # Define functions needed for the operation
    
        def generate_electrode_coords(lattice_constant_a, lattice_constant_c, size_x, size_y, size_z, bond_length, z_position, geometry):
            """Generate the coordinates for a graphite crystal with a half-level layer between each graphite layer and write them to a file.
    
            Parameters:
                lattice_constant_a (float): The lattice constant in the xy plane (in angstroms).
                lattice_constant_c (float): The lattice constant in the z direction (in angstroms).
                size_x (float): The size of the crystal in the x direction (in angstroms).
                size_y (float): The size of the crystal in the y direction (in angstroms).
                size_z (float): The size of the crystal in the z direction (in angstroms).
    
            Returns:
                List of lists (x, y, z) with coordinates of each atom of the electrode
            """
    
            # Calculate the number of unit cells in each direction
            nx = math.ceil(size_x / lattice_constant_a)
            ny = math.ceil(size_y / lattice_constant_a)
            nz = math.ceil(size_z / lattice_constant_c)
            
            print("used geometry is ", geometry)
    
            # Distinguish electrode geometry types
            if geometry == "hexagonal":
                # Define the basis vectors
                a1 = [lattice_constant_a * (3**0.5) / 2, lattice_constant_a / 2, 0]
                a2 = [lattice_constant_a * (3**0.5) / 2, -lattice_constant_a / 2, 0]
                a3 = [0, 0, lattice_constant_c]
    
                # Define the half-level displacement vector
                d = [0, 0, lattice_constant_c / 2]
    
                # Generate the coordinates for the graphite crystal
                coords = []
                for i in range(2 * -nx, 2 * nx + 1):
                    for j in range(2 * -ny, 2 * ny + 1):
                        for k in range(2 * -nz, 2 * nz + 1):
                            # Add the atom at node
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + j * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + z_position
                            ])
                            # Add atom linked to the node-atom
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0] + bond_length,
                                i * a1[1] + j * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + z_position
                            ])
                            # Add equivalent in half-layer
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0] + d[0],
                                i * a1[1] + j * a2[1] + k * a3[1] + d[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + d[2] + z_position
                            ])
                            # Add atom linked to the half-layer node-atom
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0] + d[0] - bond_length,
                                i * a1[1] + j * a2[1] + k * a3[1] + d[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + d[2] + z_position
                            ])
            if geometry == "CFC(100)":
                # Define the basis vectors
                a1 = [lattice_constant_a, 0, 0]
                a2 = [0, lattice_constant_a, 0]
                a3 = [0, 0, lattice_constant_a]
    
                # Generate the coordinates for the graphite crystal
                coords = []
                for i in range(2 * -nx, 2 * nx + 1):
                    for j in range(2 * -ny, 2 * ny + 1):
                        for k in range(2 * -nz, 2 * nz + 1):
                            # Add the atom at node
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + j * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + z_position
                            ])
                            # Add atom of centered faces (XY)
                            coords.append([
                                (i + 1/2) * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + (j + 1/2) * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + z_position
                            ])
                            # Add atom of centered faces (XZ)
                            coords.append([
                                (i + 1/2) * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + j * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + (k + 1/2) * a3[2] + z_position
                            ])
                            # Add atom of centered faces (YZ)
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + (j + 1/2) * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + (k + 1/2) * a3[2] + z_position
                            ])
                            
            if geometry == "CFC(111)":
                # Define the basis vectors
                a1 = [lattice_constant_a, 0, 0]
                a2 = [lattice_constant_a*1/2, lattice_constant_a*(3**(1/2))/2, 0]
                a3 = [0, 0, lattice_constant_c]
    
                # Generate the coordinates for the graphite crystal
                coords = []
                for i in range(2 * -nx, 2 * nx + 1):
                    for j in range(2 * -ny, 2 * ny + 1):
                        for k in range(2 * -nz, 2 * nz + 1):
                            # Add the atom at node
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + j * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + z_position
                            ])
                            
                            # Add 2nd plan atom
                            coords.append([
                                (i + 1/3) * a1[0] + (j+1/3) * a2[0] + k * a3[0],
                                i * a1[1] + (j+1/3) * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + (k +1/3) * a3[2] + z_position
                            ])
                            
                            # Add 3nd plan atom
                            coords.append([
                                (i + 2/3) * a1[0] + (j+2/3) * a2[0] + k * a3[0],
                                i * a1[1] + (j+2/3) * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + (k +2/3) * a3[2] + z_position
                            ])
                            
                            
                            
                            
            if geometry == "CFC(110)":
                # Define the basis vectors
                a1 = [lattice_constant_a, 0, 0]
                a2 = [0, lattice_constant_a, 0]
                a3 = [0, 0, lattice_constant_a]
    
                # Generate the coordinates for the graphite crystal
                coords = []
                for i in range(2 * -nx, 2 * nx + 1):
                    for j in range(2 * -ny, 2 * ny + 1):
                        for k in range(2 * -nz, 2 * nz + 1):
                            # Add the atom at node
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + j * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + z_position
                            ])
                            # Add atom of centered faces (XY)
                            coords.append([
                                (i + 1/2) * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + (j + 1/2) * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + z_position
                            ])
                            # Add atom of centered faces (XZ)
                            coords.append([
                                (i + 1/2) * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + j * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + (k + 1/2) * a3[2] + z_position
                            ])
                            # Add atom of centered faces (YZ)
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + (j + 1/2) * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + (k + 1/2) * a3[2] + z_position
                            ])
                            
                            
            if geometry == "CC":
                # Define the basis vectors
                a1 = [lattice_constant_a, 0, 0]
                a2 = [0, lattice_constant_a, 0]
                a3 = [0, 0, lattice_constant_a]
    
                # Generate the coordinates for the graphite crystal
                coords = []
                for i in range(2 * -nx, 2 * nx + 1):
                    for j in range(2 * -ny, 2 * ny + 1):
                        for k in range(2 * -nz, 2 * nz + 1):
                            # Add the atom at node
                            coords.append([
                                i * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + j * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + k * a3[2] + z_position
                            ])
                            # Add central atom
                            coords.append([
                                (i + 1/2) * a1[0] + j * a2[0] + k * a3[0],
                                i * a1[1] + (j + 1/2) * a2[1] + k * a3[1],
                                i * a1[2] + j * a2[2] + (k + 1/2) * a3[2] + z_position
                            ])
    
            MARGIN = 1
            # Set the maximum allowed values for x, y, and z
            max_x = size_x + MARGIN
            max_y = size_y + MARGIN
            max_z = size_z + z_position
    
            # Initialize a list to store the modified lines
            modified_lines = []
    
            # Loop through the lines in the file
            for coord in coords:
                # Convert the values to floats
                x = coord[0]
                y = coord[1]
                z = coord[2]
                # If all of the coordinates are below the maximum allowed values,
                # add the line to the modified_lines list
                if x < max_x and y < max_y and z < max_z and x >= 0 and y >= 0 and z >= z_position:
                    modified_lines.append(coord)
    
            return modified_lines

        # Retrieve the user's input
        self.filename = str(self.filename_entry.get())
        self.z_position = float(self.electrode_position_entry.get())
        self.size_z = float(self.z_dimension_entry.get())
        self.electrode_position = float(self.electrode_position_entry.get())
        self.electrode_name = str(self.electrode_name_entry.get())
    
        # Determine box size
        if self.size_x == 0 and self.size_y == 0:
            self.size_x, self.size_y = determin_box_size(self.filename)
            print(f"Determination of the box size done:\nBox size is x = {self.size_x} and y = {self.size_y}")
    
        # Launch the two functions
        self.electrode_coords = generate_electrode_coords(
            float(self.a),
            float(self.c),
            self.size_x,
            self.size_y,
            self.size_z,
            float(self.b),
            self.electrode_position,
            self.geom
        )
    
        insert_electrode(self.filename, self.electrode_coords, self.electrode_name)
    
        self.wip_label.grid(row=15, column=0, columnspan=2)