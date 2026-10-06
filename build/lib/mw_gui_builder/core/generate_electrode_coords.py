#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 12:19:28 2025

@author: juleswolff
"""
import math 
import numpy as np
   


def pre_run(lattice_constant_a,lattice_constant_b,lattice_constant_c, size_x, size_y, size_z):

    # Calculate the number of unit cells in each direction
    nx = math.ceil(size_x / lattice_constant_a)
    ny = math.ceil(size_y / lattice_constant_a)
    nz = math.ceil(size_z / lattice_constant_c)
    
    
    return nx,ny,nz

def hexagonal(lattice_constant_a, lattice_constant_b, lattice_constant_c, size_x, size_y, size_z, z_position):

    nx,ny,nz = pre_run(lattice_constant_a, lattice_constant_a, lattice_constant_c, size_x, size_y, size_z)    

    # Distinguish electrode geometry types
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
                    i * a1[0] + j * a2[0] + k * a3[0] + lattice_constant_b,
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
                    i * a1[0] + j * a2[0] + k * a3[0] + d[0] - lattice_constant_b,
                    i * a1[1] + j * a2[1] + k * a3[1] + d[1],
                    i * a1[2] + j * a2[2] + k * a3[2] + d[2] + z_position
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

def CFC100(lattice_constant_a,lattice_constant_b, lattice_constant_c, size_x, size_y, size_z, z_position):
    
    
    nx,ny,nz = pre_run(lattice_constant_a, lattice_constant_a, lattice_constant_c, size_x, size_y, size_z)    

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
                    
def CFC111(lattice_constant_a,lattice_constant_b, lattice_constant_c, size_x, size_y, size_z, z_position):
    
    
    nx,ny,nz = pre_run(lattice_constant_a, lattice_constant_a, lattice_constant_c, size_x, size_y, size_z)    

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
                
                    
                    
                    
                    
def CFC110(lattice_constant_a,lattice_constant_b, lattice_constant_c, size_x, size_y, size_z, z_position):
    
    
    nx,ny,nz = pre_run(lattice_constant_a, lattice_constant_a, lattice_constant_c, size_x, size_y, size_z)   
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
                    
