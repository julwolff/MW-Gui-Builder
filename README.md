# Metalwalls-Gui-Builder

**MW-Gui-builder** is an open-source Python package and graphical interface for preparing simulation-ready input files for the [MetalWalls](https://gitlab.com/ampere2/metalwalls) molecular dynamics software. It provides a modular GUI that enables researchers to define complex electrochemical systems, including electrolyte molecules, ionic species, and electrodes, and generate all necessary structure and parameter files for simulations at constant potential.

---

## What Does It Do?

MWGb automates the generation of the following MetalWalls input files ('.inpt') using as an input:

- `.xyz` — atom-ordered structure file
- `.els` — force field and charge definition per atom type
- `electrode.txt` — lattice and charge definitions for metallic electrodes

It includes internal tools to:

- Reorder atoms to match MetalWalls requirements
- Convert `.xyz` files to `.inpt`
- Build and insert crystalline electrodes
- Interface with **Packmol** and **fftool** for molecular packing

---

## Features

- Modular GUI with 4 independent tools:
  -  Box generation via `fftool` and `Packmol`
  -  File conversion and atom reordering for `.inpt`
  -  Electrode lattice generation and insertion
  -  Full parameter`.inpt` file writer for NVE, NVT, NPT
- Automatically recognizes molecules, ions, and electrodes
- Supports charge types: `point`, `neutral`, `gaussian`
- Uses Lorentz-Berthelot rules for Lennard-Jones parameters
- Electrode crystal types supported: `hexagonal`, `CFC(100)`, `CFC(110)`, `CFC(111)`

---

## Installation

### Requirements

- Python 3.8 or higher
- Packmol

### Installation

Clone the repository and install the required packages:

git clone https://github.com/julwolff/MW-Gui-Builder.git
cd MW-Gui-Builder
pip install -r requirements.txt


How to Use
Launch the graphical interface from the root directory:


python main.py

This will open a GUI with four independent tools:

Box Generator	Builds packed structures using fftool
Format for MW	Converts .gro or .xyz to .inpt
Electrode Generator	Adds electrodes based on lattice templates
Parameter Generator	Writes .inpt files for MetalWalls

Input File Formats
Detailed input file specifications can be found in the docs folder.

Basic requirements:

mass.txt: List of element names and atomic masses
.xyz: Molecule structure file (XYZ format)
.els: Atom types, charges, Lennard-Jones parameters, and force field terms
electrode.txt: Crystal definitions and charge models for electrodes

Testing (optional)

pytest core/tests/


Example Workflow

1. Create your molecule and parameter files (.xyz, .els, electrode.txt)
2. Open ElecSim via python main.py
3. Use Box Generator to place molecules in a simulation box
4. Use Electrode Generator to insert lattice-defined electrodes
5. Use Format for MW to convert structure into .inpt
6. Use Parameter Generator to define simulation settings in runtime.inpt
7. Launch your MetalWalls simulation with the prepared files

License

This project is licensed under the MIT License.


