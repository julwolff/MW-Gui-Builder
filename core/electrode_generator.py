# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 11:17:03 2025

@author: jules
"""

import numpy as np

class Electrode_options:
    def __init__(self, field):
        
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
    
    dat = np.loadtxt('ressources/electrode.txt', dtype=str, skiprows=1)
    
    electrodes = []
    for i in range(len(dat[:,0])):
        
        electrode = Electrode_options([j for j in dat[i,:]])
        electrodes.append(electrode)
        
    return electrodes
    
def insert_electrode(filename, coords, electrode_name, buffer):
    """
    Inserts electrode coordinates into a file.

    Parameters:
    - filename (str): The name of the file that you want to read and write to.
    - coords (list): A list of tuples containing the (x, y, z) coordinates of the electrodes that you want to insert into the file.
    - electrode_name (str): A string containing the name of the electrodes you want to insert.

    Returns:
    None
    """

    mols = []
    n_moles = 0
    species = []
    species_recensed = []

    with open(filename, 'r') as file:
        values = file.readlines()

        for i in range(2, len(values)):
            species.append(values[i].split()[0])


    # Launch the search pattern function
    mols, n_moles, species_recensed = search_pattern(mols, n_moles, species, species_recensed)

    # Create a variable to store temporarily all species effectively recensed
    temp_species = []
    # Join mols files to recense all effective species
    for i in mols:
        temp_species += i
    # Restore the variable
    species_recensed = temp_species

    # Launch a second time to recense also alone species
    mols, n_moles, species_recensed = search_pattern(mols, n_moles, species, species_recensed, first_time=False)

    # Define the shift amount
    elec_z_coord = []
    for i in range(len(coords)):
        elec_z_coord.append(coords[i][2])
    # The shift amount is the real size of the electrode that is different from the size proposed in input    
    # A margin is added to guarantee that no atom is too near to the electrode
    margin = float(buffer)
    shift_amount = max(elec_z_coord) - min(elec_z_coord) + margin
    min_z = min(elec_z_coord) - margin

    # Open the file
    with open(filename, "r") as file:
        # Read the lines in the file
        lines = file.readlines()

        # Look if there is already some electrodes in the file
        try:
            electrode_existing = lines[1].split()[8]
        except IndexError:
            electrode_existing = 0
            print("first electrode detected")

    # Loop through the lines in the file after passing the 2 first comment lines

    # Create a list to store all z sensible positions
    z_affected = []
    idx_affected = []

    for i in range(2, len(lines)):
        # Split the line into a list of values
        values = lines[i].split()
        # Convert the z value to a float
        z = float(values[3])
        # If the z value is above the minimum, identify the molecule group, identify atoms in the molecule, modify the z values of these atoms
        if z >= min_z:
            # In for each molecule group
            for group in mols:
                # We check if the atom is in the group
                if values[0] in group:
                    # Define the position of the atom in the group (often it is 0)
                    pos = group.index(values[0])
                    # Note all values that have to be moved
                    for j in range(-pos, len(group) - pos):
                        values = lines[i+j].split()
                        z_affected.append(float(values[3]))
                        idx_affected.append(i+j)
                        idx_affected = list(set(idx_affected))

    # Check if there is sensible z positions
    if len(idx_affected) != 0:
    
        # Update the shift amount
        shift_amount += min(elec_z_coord) - min(z_affected)
    
    
    
        
        #Modify all positions by the shift amount
        for i in idx_affected:
            values = lines[i].split()
            values[3] = str(float(values[3]) + shift_amount)
            lines[i+j] = " ".join(values)
        
        print (f"{len(idx_affected)} were moved")
        
    else:
        
        print ("no electrolytes atoms were moved")
        
    for i in range(len(lines)):
        lines[i] = " ".join(lines[i].split())
        
    # Determine new file name 
    
    filename_tmp = filename.split('.')
    filout = filename_tmp[0] + "_electrode." + filename_tmp[1]
    
    # Open the file for writing
    with open(filout, "w") as file:
        # Rewrite the two first lines with the number of atoms updated
        file.write(str(len(lines) - 2 + len(coords)) + "\n")
        file.write("Atom number : {} Electrode Atom number : {}".format(len(lines) - 2 + len(coords), int(len(coords)) + int(electrode_existing)) + "\n")
        # Rewrite each line
        for i in range(2, len(lines)):
            file.write(lines[i] + "\n")
        # Write electrode coordinates
        for j in range(len(coords)):
            coord = electrode_name + " " + " ".join([str(coords[j][0]), str(coords[j][1]), str(coords[j][2])]) + "\n"
            file.write(coord)
            
    print ('electrode add in ', filout)

def determin_box_size(file):
    
    x = []
    y = []

    with open(file, 'r') as files:
        lines = files.readlines()

    for i in range(2, len(lines)):
        x.append(float(lines[i].split()[1]))
        y.append(float(lines[i].split()[2]))

    return max(x) + 1.5, max(y) + 1.5

    x = []
    y = []

    with open(file, 'r') as files:
        lines = files.readlines()

    for i in range(2, len(lines)):
        x.append(float(lines[i].split()[1]))
        y.append(float(lines[i].split()[2]))

    return max(x) + 1.5, max(y) + 1.5

    

def search_pattern(mols, n_moles, species, species_recensed, first_time=True):
    # Prepare the species_recensed list to avoid infinite molecule
    if first_time:
        for i in range(len(species)):
            if species.count(species[i]) == 1:
                species_recensed.append(species[i])

    for k in range(len(species)):
        # Check if the species were already seen
        if species[k] not in species_recensed:
            # If the species was never seen, a new molecule is created
            # and this species is added to the molecule
            mols.append([])
            mols[n_moles].append(species[k])
            # As the species was seen it is now considered as a recensed_species
            species_recensed.append(species[k])
            # A while loop is done to see all atoms after the first atom of the new molecule
            j = k + 1
            # While the species was not already seen
            while species[j] not in species_recensed:
                # This one is appended to the current molecule
                mols[n_moles].append(species[j])
                # And appended to the list of already seen molecules
                species_recensed.append(species[j])
                j += 1
            # Once all new species are added to the molecule, we pass to the next molecule
            n_moles += 1
    return mols, n_moles, species_recensed
    