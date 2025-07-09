# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 11:17:03 2025

@author: jules

Module for electrode options management and insertion into coordinate files.
"""

import numpy as np
import os

class Electrode_options:
    def __init__(self, field):
        """
        Initialize an Electrode_options instance from a list of parameters.

        Parameters:
        - field (list): List of electrode parameters in order:
          [name, geom, a, b, c, mass, epsilon, sigma, gaussian_width, Tf, voronoi]
        """
        if len(field) < 11:
            raise ValueError("Field list must contain at least 11 elements")
        self.name = field[0]
        self.geom = field[1]
        self.a = field[2]
        self.b = field[3]
        self.c = field[4]
        self.mass = field[5]
        self.epsilon = field[6]
        self.sigma = field[7]
        self.gaussian_width = field[8]
        self.Tf = field[9]
        self.voronoi = field[10]

def electrode_loading():
    """
    Load electrode data from 'ressources/electrode.txt' file.

    Returns:
    - electrodes (list): List of Electrode_options objects loaded from file.

    Raises:
    - FileNotFoundError: If the electrode data file does not exist.
    """
    filepath = 'ressources/electrode.txt'
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Electrode data file '{filepath}' not found.")
    dat = np.loadtxt(filepath, dtype=str, skiprows=1)

    electrodes = []
    for i in range(len(dat[:, 0])):
        electrode = Electrode_options([j for j in dat[i, :]])
        electrodes.append(electrode)

    print(f"Loaded {len(electrodes)} electrodes from '{filepath}'.")
    return electrodes

def insert_electrode(filename, coords, electrode_name, buffer):
    """
    Insert electrode coordinates into a coordinate file and shift atoms if needed.

    Parameters:
    - filename (str): Path to the input coordinate file.
    - coords (list of tuples): List of (x, y, z) tuples for electrode coordinates.
    - electrode_name (str): Name of the electrode species to insert.
    - buffer (float or str): Buffer distance to add between electrodes and atoms.

    Returns:
    - None

    Raises:
    - FileNotFoundError: If the input file does not exist.
    - ValueError: If coordinates are invalid or buffer cannot be converted to float.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Input file '{filename}' not found.")
    try:
        margin = float(buffer)
    except Exception as e:
        raise ValueError(f"Buffer parameter must be convertible to float. Error: {e}")

    mols = []
    n_moles = 0
    species = []
    species_recensed = []

    with open(filename, 'r') as file:
        values = file.readlines()
        for i in range(2, len(values)):
            species.append(values[i].split()[0])

    # Identify molecules and species grouping
    mols, n_moles, species_recensed = search_pattern(mols, n_moles, species, species_recensed)

    # Flatten mols list to species_recensed
    temp_species = []
    for group in mols:
        temp_species += group
    species_recensed = temp_species

    # Second pass to find single species
    mols, n_moles, species_recensed = search_pattern(mols, n_moles, species, species_recensed, first_time=False)

    elec_z_coord = [coord[2] for coord in coords]
    shift_amount = max(elec_z_coord) - min(elec_z_coord) + margin
    min_z = min(elec_z_coord) - margin

    with open(filename, "r") as file:
        lines = file.readlines()

    # Check if electrodes already exist in file header line 2
    try:
        electrode_existing = int(lines[1].split()[8])
    except (IndexError, ValueError):
        electrode_existing = 0
        print("First electrode detected (no existing electrode count found).")

    z_affected = []
    idx_affected = []

    # Identify atoms above min_z and their molecule groups
    for i in range(2, len(lines)):
        values = lines[i].split()
        try:
            z = float(values[3])
        except (IndexError, ValueError):
            print(f"Skipping line {i}: cannot parse z coordinate.")
            continue
        if z >= min_z:
            for group in mols:
                if values[0] in group:
                    pos = group.index(values[0])
                    for j in range(-pos, len(group) - pos):
                        idx = i + j
                        if 0 <= idx < len(lines):
                            vals = lines[idx].split()
                            try:
                                z_affected.append(float(vals[3]))
                                idx_affected.append(idx)
                            except (IndexError, ValueError):
                                print(f"Skipping line {idx}: cannot parse z coordinate.")
                    idx_affected = list(set(idx_affected))

    if idx_affected:
        shift_amount += min(elec_z_coord) - min(z_affected)
        for idx in idx_affected:
            values = lines[idx].split()
            try:
                values[3] = str(float(values[3]) + shift_amount)
            except (IndexError, ValueError):
                print(f"Failed to update z-coordinate at line {idx}.")
                continue
            lines[idx] = " ".join(values) + "\n"
        print(f"{len(idx_affected)} atoms moved by {shift_amount:.3f} in z-direction.")
    else:
        print("No electrolyte atoms were moved.")

    # Clean up whitespace
    for i in range(len(lines)):
        lines[i] = " ".join(lines[i].split()) + "\n"

    filename_tmp = filename.rsplit('.', 1)
    filout = filename_tmp[0] + "_electrode." + filename_tmp[1]

    with open(filout, "w") as file:
        file.write(str(len(lines) - 2 + len(coords)) + "\n")
        file.write(f"Atom number : {len(lines) - 2 + len(coords)} Electrode Atom number : {len(coords) + electrode_existing}\n")
        for i in range(2, len(lines)):
            file.write(lines[i])
        for coord in coords:
            coord_line = f"{electrode_name} {coord[0]} {coord[1]} {coord[2]}\n"
            file.write(coord_line)

    print(f"Electrode added in {filout}")

def determin_box_size(file):
    """
    Determine the box size based on x and y coordinates in a file.

    Parameters:
    - file (str): Path to the coordinate file.

    Returns:
    - tuple: (max_x + 1.5, max_y + 1.5) as floats representing box dimensions.

    Raises:
    - FileNotFoundError: If the file does not exist.
    - ValueError: If the coordinate lines cannot be parsed correctly.
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(f"File '{file}' not found.")

    x = []
    y = []

    with open(file, 'r') as files:
        lines = files.readlines()

    for i in range(2, len(lines)):
        try:
            x.append(float(lines[i].split()[1]))
            y.append(float(lines[i].split()[2]))
        except (IndexError, ValueError):
            raise ValueError(f"Error parsing coordinates on line {i+1} in file '{file}'")

    max_x = max(x) + 1.5
    max_y = max(y) + 1.5
    print(f"Determined box size: x={max_x:.2f}, y={max_y:.2f}")
    return max_x, max_y

def search_pattern(mols, n_moles, species, species_recensed, first_time=True):
    """
    Search and group molecule species patterns from a species list.

    Parameters:
    - mols (list): Current list of molecule groups (list of lists).
    - n_moles (int): Number of molecules/groups found so far.
    - species (list): List of species names from the file.
    - species_recensed (list): List of species already accounted for.
    - first_time (bool): If True, initialize species_recensed with unique species.

    Returns:
    - tuple: (mols, n_moles, species_recensed)
    """
    if first_time:
        for i in range(len(species)):
            if species.count(species[i]) == 1:
                species_recensed.append(species[i])

    for k in range(len(species)):
        if species[k] not in species_recensed:
            mols.append([])
            mols[n_moles].append(species[k])
            species_recensed.append(species[k])
            j = k + 1
            while j < len(species) and species[j] not in species_recensed:
                mols[n_moles].append(species[j])
                species_recensed.append(species[j])
                j += 1
            n_moles += 1
    return mols, n_moles, species_recensed
