# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 09:26:27 2025

@author: jules
"""

def distinct_species(mols):
    
     

     species = []

     # List all the species contained in _pack.xyz
     for mol in range(len(mols)):
         file_pack = "molecules/" + mols[mol].split('.')[0] + "_pack.xyz"
         with open(file_pack, 'r') as rfile:
             lines = rfile.readlines()
             for i in range(2, len(lines)):
                 species.append(lines[i].split()[0])

     # Distinguish different species
     for i in range(len(species)):
         j = 0
         while species[i] + str(j) in species != True:
             j += 1
         species[i] = species[i] + str(j)

     # Rewrite each file
     i = 2
     for mol in range(len(mols)):
         file_pack = "molecules/" + mols[mol].split('.')[0] + "_pack.xyz"
         with open(file_pack, 'r') as rfile:
             lines = rfile.readlines()
             for j in range(2, len(lines)):
                 lines[j] = lines[j].replace(lines[j].split()[0], species[i - 2])
                 i += 1

         # Rewrite in the files
         with open(file_pack, 'w') as wfile:
             for k in range(len(lines)):
                 wfile.write(lines[k])
                     
                 
    
                 
                     

 # Function to change the length of the box
def change_len_box():
     # Open the input file
     with open("pack.inp", 'r') as inp:
         # Read lines
         lines = inp.readlines()
         xy_box, z_box = None, None
         for i in lines:
             # Isolate molecule position ranges lines
             if "inside" in i:
                 # Find l_box
                 l_box = float((i.split()[-1])) + 1.5
                 # Define x, y, and z length of the box
                 xy_box = l_box / 2 ** (0.5) - 1.5
                 z_box = l_box * 2 - 1.5
         for i in range(len(lines)):
             # Isolate molecule position ranges lines
             if "inside" in lines[i]:
                 range_box = lines[i].split()
                 range_box[5] = str(xy_box)
                 range_box[6] = str(xy_box)
                 range_box[7] = str(z_box)
                 lines[i] = " ".join(range_box) + "\n"
     with open("pack.inp", 'w') as inp:
         inp.writelines(lines)
         

 # Function to elongate the box
def elongate_box(multiplier):
     with open("pack.inp", 'r') as inp:
         # Read lines
         lines = inp.readlines()
         for i in lines:
             # Isolate molecule position ranges lines
             if "inside" in i:
                 # Find l_box
                 l_box = float((i.split()[-1])) + 1.5
                 # Define basis
                 a = (l_box ** 3 / multiplier) ** (1 / 3)
                 # Define x, y, and z length of the box
                 xy_box = a - 1.5
                 z_box = 5 * a - 1.5
         for i in range(len(lines)):
             # Isolate molecule position ranges lines
             if "inside" in lines[i]:
                 range_box = lines[i].split()
                 range_box[5] = str(xy_box)
                 range_box[6] = str(xy_box)
                 range_box[7] = str(z_box)
                 lines[i] = " ".join(range_box) + "\n"
     with open("pack.inp", 'w') as inp:
         inp.writelines(lines)
         
         
def communicate_box_data():
     
     with open('pack.inp','r') as inp:
         file = inp.readlines()
         
         x,y,z = [], [], []
         
         for i in file:
             if 'inside box' in i:
                 z.append(float(i.split()[-1]))
                 y.append(float(i.split()[-2]))
                 x.append(float(i.split()[-3]))
                 
 
         
     
     print("A box with dimensions", max(x), 'x', max(y),'x', max(z), 'A. If you want to put an electrode without moving any electrolyte, place it at', max(z)+2.2,"A")

