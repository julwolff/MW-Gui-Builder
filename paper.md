---
title: 'Gala: A Python package for galactic dynamics'
tags:
  - Python
  - Molecular Dynamics
  - Modelling
  - Electrochemistry
authors:
  - name: Wolff Jules
    orcid: 0009-0002-3222-4159
    equal-contrib: true
    affiliation: "1, 2" # 
affiliations:
  - name: "Institut de Chimie et Procédés pour l'Energie, l'Environnement et la Santé, UMR 7515 CNRS-University of Strasbourg, France"
    index: 1
  - name: "Laboratoire d'Electrochimie et de Chimie Physique du corps solide, Institut de Chimie de Strasbourg, UMR 7177 CNRS-University of Strasbourg, France"
    index: 2
date: 18 November 2025
bibliography: paper.bib
---


# "MW-Gui-Builder": An interface for simplified preparation for Metalwalls package application

Jules Wolff<sup>1,2</sup>

<sup>1</sup>Institut de Chimie et Procédés pour l'Energie, l'Environnement et la
Santé, UMR 7515 CNRS-University of Strasbourg

<sup>2</sup>Laboratoire d'Electrochimie et de Chimie Physique du corps solide,
Institut de Chimie de Strasbourg, UMR 7177 CNRS-University of Strasbourg

##

## Summary

MW-Gui-Builder is an open-source Python package with a graphical
interface for preparing simulations using the MetalWalls molecular
dynamics engine. It streamlines the creation of structure and parameter
files for electrochemical systems, including electrode construction and
ion packing, making it accessible for both new and advanced users.
Mw-Gui-Builder reduces the barrier to entry for accurate
constant-potential simulations.

## Statement of need

The molecular dynamics simulations have been proved to be a reliable and
useful tool throughout the year to investigate chemical and biological
systems without experimental limitations<sup>1</sup>. The setup of the system for
those simulations however can be fastidious and complex especially for
beginners. The development of new MD software allows to study always
more realistic and complete system but also required to adapt the used
method to the current problematic<sup>2</sup>. The Metalwalls software released
in 2020 by the Phoenix lab revealed very quick its potential by taking
an important place in the electrochemical simulations<sup>3,4</sup>. The constant
potential method used by the software successfully overpass previous
method and allows to describe accurately any electrochemical system.
However, the additional solid phase represented by the electrode
presents new challenges for the system set up. The specific format of
structure and parameters files relative to this new software make the
former builder unusable. This paper describes "MW-Gui-Builder", a
builder developed and used for Metalwalls simulations at constant
potential. Generating both parameters and structure file in the adapted
format, this code is used with python environment, allowing
modifications and extensions. The plugin provides a graphical user
interface (GUI), which makes it immediate to setup computations.

## Graphical User interface

The graphical user interface developed in the package is user-friendly
and contains error and progression message box to make it readable and
understandable for all users.

## Example

All the examples are tutorial detailed in the GitHub repository of the
project. The molecules and electrode files are already written in the
molecules/ directrory.

### Water between graphene

The structure of **Figure 1** is made with 5000 TIP4P/2005 water
molecules packed in a cubic way. Two graphene electrode are added at z=0
and z=58 Å. The used buffer is 2 Å and the length used for electrode is
8 Å. The software automatically brings the length of the electrode to
the closest inferior value (6.7 Å here).

![Image 1](./exemple/Water_Graphene/exemple.png)

**Figure 1** : Cubic water liquid between two graphene electrode

### Ionic liquid with a central separator

Using the 3D periodicity, the electrode can also be placed in the
center. Here \[EMIM\]\[TFSI\] ionic liquid (400 each) are packed with a
concentration of 5M/L. The box in **Figure 2** is 2 time larger than
longer and a CFC(110) oriented electrode is place in z=65 Å with a
buffer of 7 Å and a electrode length of 8 Å.

![Image 2](./exemple/Ionic_Liquids_Platinum/exemple.png)

**Figure 2** : Pt(110) electrode splitting box of \[EMIM\]\[TFSI\] in
half

### Electrochemically meaningful system

The system in **Figure 3** contains 3000 TIP4P water molecules and 54
ion pair of NaOH, corresponding to a 1M electrolyte. The two electrode
placed at respectively 0 and 130 Å are 8 Å long. Both electrode are 
(100) Pt electrode.

![Image 3](./exemple/Alkaline_HER_Platinum/exemple.png)

**Figure 3**: 1M NaOH in TIP4P water between (100) Pt electrode.

## Related projects 

The package is currently in active use at the *Institut de Chimie et
Procédés pour l\'Énergie, l\'Environnement et la Santé (ICPEES)* as part
of multiple research projects focused on understanding the
electrochemical double layer. These projects are carried out within the
framework of the DECODE program, which aims to improve our understanding
of the local reaction environment in electrochemical systems.

As part of its future development, Mw-Gui-Builder will support more
complex electrode configurations, including customizable surface shapes,
partial coverage models, and bimetallic electrode materials. These
enhancements will enable researchers to simulate a wider range of
realistic electrochemical interfaces with improved accuracy and
flexibility.

## Bibliography

1\. Hollingsworth, S. A. & Dror, R. O. Molecular Dynamics Simulation for
All. *Neuron* vol. 99 1129--1143 Preprint at
https://doi.org/10.1016/j.neuron.2018.08.011 (2018).

2\. Zeng, L. *et al.* Molecular dynamics simulations of electrochemical
interfaces. *Journal of Chemical Physics* vol. 159 Preprint at
https://doi.org/10.1063/5.0160729 (2023).

3\. Scalfi, L., Salanne, M. & Rotenberg, B. Molecular Simulation of
Electrode-Solution Interfaces. *Annu Rev Phys Chem* 72, 189--212 (2021).

4\. Coretti, A. *et al.* MetalWalls: Simulating electrochemical
interfaces between polarizable electrolytes and metallic electrodes.
*Journal of Chemical Physics* 157, 184801 (2022).
