# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 11:37:41 2025

@author: jules
"""

import math
from itertools import combinations


def write_param_files(filein            = "simbox.xyz",
                      fileout           = 'runtime.inpt',
                      temperature       = 298,
                      sim_type          ='NVT',
                      pressure_applied  = 0,
                      cutoff            = 17.005,
                      amplitude         = 0,
                      mols              = [],
                      molecules         = [],
                      species           = [],
                      electrodes        = [],
                      lj_pairs          = [],
                      time_step         = 10000,
                      output_list       = []):

    
            
    
    with open(fileout,"w") as file:
        
        file.write("# System configuration\n")
        file.write("# ====================\n\n")
        file.write("# Global simulation parameters\n")
        file.write("# ----------------------------\n")
        file.write("num_steps     {} # number of steps in the run\n".format(time_step))
        file.write("timestep     41.341 # timestep (a.u)\n")
        file.write("temperature   {} # temperature (K)\n\n".format(temperature))
        file.write("# Periodic boundary conditions\n")
        file.write("# ----------------------------\n")
        file.write("num_pbc  3\n\n")
        
        if sim_type == 'NVT' or sim_type == 'NPT':
            
            file.write("# Thermostat:\n")
            file.write("# -----------\n")
            file.write("thermostat\n")
            file.write("  chain_length  5\n")
            file.write("  relaxation_time 4134.1\n")
            file.write("  tolerance  1.0e-17\n")
            file.write("  max_iteration  100\n\n")
            
        if sim_type == 'NPT':
            
            file.write("\n# Barostat:\n")
            file.write("# ---------\n")
            file.write("barostat\n")
            file.write("  pressure        {}   # pressure in a.u.\n".format(pressure_applied))
            file.write("  chain_length    5\n")
            file.write("  relaxation_time 20670.5\n\n")
            
        file.write("species\n")
        
        for i in species:
            file.write(i.file_print())
            if i.name == "Mw0":
                file.write("    fourth_site_atom\n\n")
            
        file.write("\n\n")
        
        file.write("molecules\n")
        
        for i in molecules:
            if len(i.sites) > 1:
                file.write(i.file_print())
            if "Mw0" in i.sites:
                file.write("    fourth_site 0.283458898 # distance OM\n")
                
        file.write("\n\n")
        
        if len(electrodes)>=1:
        
            file.write("electrodes\n")
            
            for i in electrodes:
                file.write(i.file_print())
                
            file.write("  electrode_charges matrix_inversion\n")
            
        file.write("\n# Interactions definition\n")
        file.write("# -----------------------\n")
        file.write("interactions\n")
        file.write("  coulomb\n")
        file.write("    coulomb_rtol 2.0e-5    # coulomb rtol\n")
        file.write("    coulomb_rcut {}    # coulomb cutoff (bohr)\n".format(cutoff))
        file.write("    coulomb_ktol 1.0e-7    # coulomb ktol\n\n")
        file.write("  lennard-jones\n")
        file.write("    lj_rcut  {}         # lj cutoff (bohr)\n".format(cutoff))
        file.write("    # lj parameters: epsilon in kJ/mol, sigma in angstrom\n\n")
    
        for i in lj_pairs:
            file.write(f"    lj_pair    {i[0]} {i[1]} {i[2]} {i[3]} \n")
        
        file.write("\n# Output section\n")
        file.write("# ----------------------\n")
        file.write("output\n")
        file.write("  default 0")

        for i in output_list:

            file.write(f"\n  {i}  10".lower())
            

            
class Species:
            def __init__(self, name, count, group, mobile, mass=0, charge_type = 'Neutral',charge = None, lj_epsilon = None, lj_sigma = None):
                
                self.name = name
                self.count = count
                self.group = group
                self.mobile = mobile
                self.mass = mass
                self.charge_type = charge_type
                self.charge = charge
                self.lj_epsilon = lj_epsilon
                self.lj_sigma = lj_sigma
                self.gro_attype = name
                

                
            def file_print(self):
                
                self.mass = str(self.mass)
                
                return f"  species_type\n    name          {self.name}\n    count         {self.count}\n    mass          {self.mass}\n    mobile        {self.mobile}\n    charge {self.charge_type} {self.charge} \n\n".ljust(2)
            
            def atty_print(self):
                
                self.mass = str(self.mass)
                
                if type(self.lj_sigma) != None :
                    self.lj_sigma = float(self.lj_sigma) *0.1                   
                
                else:
                    
                    self.lj_sigma = 0
                    self.lj_epsilon = 0
                    
                
                return f"    {self.name}     {self.mass}        {self.charge}     A {self.lj_sigma}    {self.lj_epsilon} \n".ljust(2)

            
            def ty_print(self):
                
                self.mass = str(self.mass)
                    
                return f"    {self.name}     1     {(self.group.upper())}     {self.name}      1       {self.charge}"

            
class Molecule:
    def __init__(self, name, count, sites, parameters =[]):
        
        self.name = name
        self.count = count
        self.sites = sites
        self.parameters = parameters
        
    def file_print(self):
        
        printable_site = " ".join(self.sites)
        printable_parameters = "".join(self.parameters)
        return f"\n  molecule_type\n    name          {self.name}\n    count          {self.count}\n    sites {printable_site}\n\n{printable_parameters}\n".ljust(2)
    
class Electrode:
    def __init__(self, name, sites):
        
        self.name = name
        self.sites = sites
        
    def file_print(self):
        printable_site = " ".join(self.sites)        
        return f"  electrode_type\n    name {self.name}\n    species  {printable_site}\n    potential  0.00\n    thomas_fermi_length\n    voronoi_volume"
    
    
class Constraint_parameters:
    def __init__(self, i, j, value):
        self.i = i
        self.j = j
        self.values = value
        
    def line_print(self):
        
        if self.i != "algorithm":
        
            return f"    constraint {self.i} {self.j} {self.values}\n"
        
        else:
            return f"    constraints_algorithm rattle {self.j} {self.values}\n"
    
class Bond_parameters:
    def __init__(self,i, j, strength, length):
        self.i = i
        self.j = j
        self.strength = strength
        self.length = length

    def line_print(self):
        return f"    harmonic_bond {self.i} {self.j} {self.strength} {self.length}\n"
    
class Angle_parameters:
    def __init__ (self, i, j, k, strength, value):
        self.i = i
        self.j = j
        self.k = k
        self.strength = strength
        self.value = value
        
    def line_print(self):
        return f"    harmonic_angle {self.i} {self.j} {self.k} {self.strength} {self.value}\n"

class Dihedral_parameters:
    def __init__(self, i, j, k, l, i_factor, j_factor, k_factor, l_factor):
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.i_factor = i_factor
        self.j_factor = j_factor
        self.k_factor = k_factor
        self.l_factor = l_factor
        
    def line_print(self):
        return f"    dihedral {self.i} {self.j} {self.k} {self.l} {self.i_factor} {self.j_factor} {self.k_factor} {self.l_factor}\n" 
    
class Improper_parameters:
    def __init__(self, i, j, k, l, i_factor, j_factor, k_factor, l_factor):
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.i_factor = i_factor
        self.j_factor = j_factor
        self.k_factor = k_factor
        self.l_factor = l_factor
        
    def line_print(self):
        return f"    improper {self.i} {self.j} {self.k} {self.l} {self.i_factor} {self.j_factor} {self.k_factor} {self.l_factor}\n" 
    
    
        
def search_molecule(filename='simbox.xyz'):
    
    # Set variables
    
    mols = []
    n_moles = 0
    species =[]
    species_recensed=[]

    # Read the file
    
    with open (filename, 'r') as file:
        values=file.readlines()
        
        for i in range(2,len(values)):
            
            species.append(values[i].split()[0])
            
    
    
    

    # Launch the search pattern function

    mols, n_moles, species_recensed = search_pattern(mols, n_moles, species, species_recensed)
    
    # Create a variable to stock temporary all species effectively recensed

    temp_species = []

    # Join mols files to recensed all effective species

    for i in mols:
        
        temp_species += i 
        
    # Restore the variable
        
    species_recensed = temp_species

    # Launch a second time to recensed also alone species if all species wasnot recensed first time

    if len(species_recensed) == len(species):
        
        mols, n_moles, species_recensed = search_pattern(mols, n_moles, species, species_recensed, first_time= False)
    
    
    return mols

def search_pattern(mols, n_moles, species, species_recensed, first_time = True):
    
    
    
    
    # Prepare the species_recensed list to avoid infinite molecule
    
    if first_time == True:
        
        for i in range(len(species)) :
            
            if species.count(species[i]) == 1:
                species_recensed.append(species[i])
                
        # print ('alone_species =',  species_recensed)
            
    for k in range(len(species)):
        
        
        # Check if the species were already seen
        
        if species[k] not in species_recensed :
            
            # If the species was never seen so a new molecule is created
            # and this species is added to the molecule
            
            mols.append([])
            mols[n_moles].append(species[k])
            
            # As the species was seen it is now considered as a recensed_species
            
            species_recensed.append(species[k])
            
            # A while loop is done to see all atom after the first atom of the new molecule
            
            j = k + 1
            
            # While the species was not already seen
            
            while species[j] not in species_recensed :
                
                # This one is append to the current molecule
                
                mols[n_moles].append(species[j])
                
                # And appenned to the list of already seen molecule 
                
                species_recensed.append(species[j])
                j += 1
                
            # Once all new species are added to the molecule we pass to the next molecule
                
            n_moles += 1
            
    return mols, n_moles, species_recensed


def instancie_molecules(mols):
    
    # Set variables
    
    list_of_mol=[]
    number_of_mol=[]
    molecules = []
    
    # Open pack.inp that contains all non-electrode molecules

    with open("pack.inp",'r') as packfile:
        
        lines=packfile.readlines()
        
    # Check if the name is a molecule or a number name
        
    for i in lines:
        if "structure" in i and "end" not in i :
            
            name_of_mol = i.split('_')[0]
            name_of_mol = name_of_mol.split('/')[1]

            
            list_of_mol.append(name_of_mol)
        elif "number" in i:
            number_of_mol.append(int(i.split()[1]))
            
    # Instancie all molecules that succed the test
    
            
    for i in range(len(list_of_mol)):
        molecule = Molecule(list_of_mol[i], number_of_mol[i], mols[i])
        
        
        molecules.append(molecule)
        
        
    return molecules

def instancie_species(molecules):
    
    
    # Set variables
    
    species = []
    
    # Open the mass ressources file
    
    with open("ressources/mass.txt",'r') as mass_file:
        lines = mass_file.readlines()
        
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            
    # Instancie the mass of each species
    
    # For each sites in each molecules
    
    for molecule in molecules:               
        
        for site in molecule.sites:
            
            
            name_for_mass = site
            
            # Retire les chiffres du nom de l'espece pour
            # determiner sa masse dans le tableau
            
            
            for i in name_for_mass:
                if not i.isalpha():
                    name_for_mass = name_for_mass.replace(i, "")
                    
            for i in range(len(lines)):
                if name_for_mass == lines[i][0]:
                    mass = lines[i][1]
                    
                elif i == len(lines):
                    print(f"no mass found for {site}")
                
        
            # Crée l'espèce
                    
            specie = Species(site, molecule.count, molecule.name, "True", mass)
            species.append(specie)
            
            

            
            
            
    return species


def instancie_electrodes(mols, molecules):
    
    compar_mols =[]
    electrodes = []
    
    for i in molecules:
        compar_mols.append(i.sites)
        
    for j in mols:
        if j not in compar_mols:

            electrode = Electrode(j[0], j)
            electrodes.append(electrode)
        
    return electrodes

def add_parameters(molecules,species,electrodes):
    
    # Stock all textual values
    
    biblio_electro = []
    
    # For each molecule extract electro data
    
    for molecule in molecules:
        
        bn_parameters = []
        
        with open(f"./molecules/{molecule.name}.els") as file:
            lines = file.readlines()
            
            # Determine the length of the electrostat table
            # with the keyword parameters1
            
# =============================================================================
#                     WARNING : IT IS IMPORTANT TO NOT A FREE LINES BEFORE THE WORD PARAMETERS
# =============================================================================

# =============================================================================
#                   SECOND WARNING : THIS BOUCLE IS NOOOOOT OPTIMIZED AT ALL 
#                   THE BEST SHOULD BE TO ASSOCIATE NAME TO THE FIRST INDEX OF
#                   ELECTROSTAT PART 
# =============================================================================
            
            for i in range(len(lines)):
                if "PARAMETERS" in lines[i]:
                    size_elec = i
                     
                    # Store bounded parameters into molecule
                    
                    for j in range(size_elec + 1,len(lines)):
                        
                    # Consider all the posibilities
                        print(lines[j].split()) 
                        if "constraint" in lines[j].split():
                            
                            # Add to the parameteres a contraint parameters with the two sites corresponding to the 2 index in the param file
                            
                            bn_parameters.append(Constraint_parameters(molecule.sites[int(lines[j].split()[1])],
                                                                       molecule.sites[int(lines[j].split()[2])],
                                                                       float(lines[j].split()[3])))
                            
                            if "constraint" not in lines[j+1].split():
                                
                                bn_parameters.append(Constraint_parameters('algorithm', 1e-9, 100))
                            
                        elif "harmonic_bond" in lines[j].split():
                            
                            bn_parameters.append(Bond_parameters(molecule.sites[int(lines[j].split()[1])],
                                                                 molecule.sites[int(lines[j].split()[2])],
                                                                 float(lines[j].split()[3]),
                                                                 float(lines[j].split()[4])))
                            
                        elif "harmonic_angle" in lines[j].split():
                            
                            bn_parameters.append(Angle_parameters(molecule.sites[int(lines[j].split()[1])],
                                                                  molecule.sites[int(lines[j].split()[2])],
                                                                  molecule.sites[int(lines[j].split()[3])],
                                                                  float(lines[j].split()[4]),
                                                                  float(lines[j].split()[5])))
                        
                        elif "dihedral" in lines[j].split():
                            
                            bn_parameters.append(Dihedral_parameters(molecule.sites[int(lines[j].split()[1])],
                                                                     molecule.sites[int(lines[j].split()[2])],
                                                                     molecule.sites[int(lines[j].split()[3])],
                                                                     molecule.sites[int(lines[j].split()[4])],
                                                                     float(lines[j].split()[5]),
                                                                     float(lines[j].split()[6]),
                                                                     float(lines[j].split()[7]),
                                                                     float(lines[j].split()[8])))
                        
                        elif "improper" in lines[j].split():
                            
                            bn_parameters.append(Improper_parameters(molecule.sites[int(lines[j].split()[1])],
                                                                     molecule.sites[int(lines[j].split()[2])],
                                                                     molecule.sites[int(lines[j].split()[3])],
                                                                     molecule.sites[int(lines[j].split()[4])],
                                                                     float(lines[j].split()[5]),
                                                                     float(lines[j].split()[6]),
                                                                     float(lines[j].split()[7]),
                                                                     float(lines[j].split()[8])))
                            
                        else:
                            
                            print(f"lines :  '' {lines[j]} '' in file ''{molecule.name}.els'' does not correspond to any parameters")
                            
                            
                    # Add it in molecules
                    
                    molecule.parameters = [i.line_print() for i in bn_parameters] #Don't know why it works but it works, don't touch it except if you are skilled
                    
                    
                    # Stop the research
                    
                    break
                
            # Displays information if there is no parameters
                
            else:
                print(f"No bounded parameters for {molecule.name}")
                size_elec = len(lines)
            
            # Compare to the number of required parameters and send a message if there is a doubt
                
            if size_elec != len(molecule.sites):
                print(f"Some electrostat parameters are missing for {molecule.name}")      
            
            # And store in a table
                
            for i in range(size_elec):
                biblio_electro.append(lines[i].split())
                
    # Add electrode parameters
    
    for electrode in electrodes:
        
        with open(f"molecules/electrode_{electrode.name}.els") as elecfile:
            
            lines = elecfile.readlines()
            
            for i in lines:
                
                biblio_electro.append(i.split())            

                
                                    
    # for each species
    

    for n in range(len(species)):
        
        #Instancie attribut      
        

        
        # Teste if the specie is an electrode or not
        
        if species[n].mobile =='False':
            species[n].mass = biblio_electro[n][1]
            species[n].charge_type = "gaussian"
            species[n].charge = str(biblio_electro[n][2]) + " " + str(0)
            species[n].lj_epsilon = biblio_electro[n][3]
            species[n].lj_sigma = biblio_electro[n][4]
        
        else:
            species[n].charge_type = biblio_electro[n][1]
            
            species[n].charge = biblio_electro[n][2]
            
            # Check if lj parameters are here
            
            if len(biblio_electro[n]) == 3:
                
                print("no lj_parameters found for {}".format(species[n].name))
                
            else:
                species[n].lj_epsilon = biblio_electro[n][3]
                species[n].lj_sigma = biblio_electro[n][4]
            
    return species,molecules


def instancie_lj_pair(species):
    
    # Extract species that impact lj
    
    species_lj = []
    
    for specie in species:
        if specie.lj_epsilon is not None and specie.lj_sigma is not None:
            
            species_lj.append(specie)
       

    # Do combinations of all the species    
    
    lj_pairs_tmp = list(combinations(species_lj,2))
    
    # Rewrite them in a list
    
    lj_pairs= []
    
    for i in lj_pairs_tmp:
        lj_pairs.append((i[0].name,
                        i[1].name,
                        math.sqrt(float(i[0].lj_epsilon)*float(i[1].lj_epsilon)),       #Formula to compute epsilon of hetero lj
                        (float(i[0].lj_sigma)+float(i[1].lj_sigma))/2))                            #Formula to compute sigma of hetero lj
                        
    
    
    
    
    # Add self application lj
    
    for i in species_lj:
        lj_pairs.append((i.name,i.name,i.lj_epsilon,i.lj_sigma))
        
    return lj_pairs

    
def add_electrode_to_species(electrodes, species, filename):
    
    with open(filename,'r') as file:
        text = file.read()
    
        
    for i in electrodes:

        electrode = Species(i.name,text.count(str(i.name)),i.sites, "False", 0, 'gaussian')
        species.append(electrode)
            
    return species