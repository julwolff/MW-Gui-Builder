# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 09:31:58 2025

@author: jules
"""

def extract_lines_as_a_list(file_text):
    """Take a text file in input and return lines as a list"""
    with open(file_text, 'r') as r_file:
        lines = r_file.readlines()
        return lines

def formate_lines(list_of_atom_coordinates):
    """Take a list of strings in input and return the same list without the n first characters"""
    formated_list = []
    for i in range(len(list_of_atom_coordinates)):
        temp_lines = list_of_atom_coordinates[i].split()
        formated_list.append(" ".join(temp_lines))
    return formated_list

def convert_list_from_int_to_string(list_of_int):
    """Convert a list in input into the same list with all items in string format"""
    list_of_string = []
    for i in list_of_int:
        list_of_string.append(str(i))
    return list_of_string

def enlarge_box(atom_coordinates):
    new_box = []
    ESP = 1 * " "
    ANG_TO_BOHR_CONV = 1.890
    for i in range(2, len(atom_coordinates)):
        namexyz = atom_coordinates[i].split()
        name = namexyz[0]
        x = float(namexyz[1]) * ANG_TO_BOHR_CONV
        y = float(namexyz[2]) * ANG_TO_BOHR_CONV
        z = float(namexyz[3]) * ANG_TO_BOHR_CONV
        new_box.append(name + ESP + str(format(x, '.15f')) + ESP + str(format(y, '.15f')) + ESP + str(format(z, '.15f')))
    return new_box

def mw_file_writting(packmol_file, mw_file, header_data, list_of_atom_coordinates):
    """Rewrite the simbox as the mw file ready for simulation,
    take input file, output file, header and list of atoms with coordinates in arguments
    give a file ready for mw"""
    with open(mw_file, 'w') as w_file:
        w_file.write("# header\nstep" + 25 * " " + "0\n"
                     "num_atoms" + 20 * " " + header_data[0] + "\n"
                     + "num_electrode_atoms" + 10 * " " + header_data[1] + "\n"
                     + "# box\n"
                     + " {} {} {}".format(header_data[2], header_data[3], header_data[4]) + "\n# coordinates\n")
        for i in list_of_atom_coordinates:
            w_file.write(i + "\n")

def sort_atom_by_species(coordinates_files):
    species = []
    sorted_coordinates = []
    for i in range(len(coordinates_files)):
        # Take the species name as the first word of
        # the list from the method split
        species_name = coordinates_files[i].split()[0]
        if species_name not in species:
            species.append(species_name)
    for i in range(len(species)):
        for j in range(len(coordinates_files)):
            coor_test = coordinates_files[j].split()[0]
            if species[i] == coor_test:
                sorted_coordinates.append(coordinates_files[j])
    return sorted_coordinates

def mw_writting(filin, filout, formated_atom_list, formated_header):

    # RUN
    formated_atom_list_in_bohr = enlarge_box(formated_atom_list)
    sorted_coordinates = sort_atom_by_species(formated_atom_list_in_bohr)
    mw_file_writting(filin, filout, formated_header, sorted_coordinates)