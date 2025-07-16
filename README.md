# ElecSim

**ElecSim** is an open-source Python package and graphical interface for preparing simulation-ready input files for the [MetalWalls](https://gitlab.com/ampere2/metalwalls) molecular dynamics software. It provides a modular GUI that enables researchers to define complex electrochemical systems, including electrolyte molecules, ionic species, and electrodes, and generate all necessary structure and parameter files for simulations at constant potential.

---

## 🔍 What Does It Do?

ElecSim automates the generation of the following MetalWalls input files:

- `.inpt` — atom-ordered structure file
- `.prm` — parameter file for NVE/NVT/NPT ensembles
- `.els` — force field and charge definition per atom type
- `electrode.txt` — lattice and charge definitions for metallic electrodes

It also includes internal tools to:

- Reorder atoms to match MetalWalls requirements
- Convert `.gro` or `.xyz` files to `.inpt`
- Build and insert crystalline electrodes
- Interface with **Packmol** and **fftool** for molecular packing

---

## 🚀 Features

- Modular GUI with 4 independent tools:
  - ✅ Box generation via `fftool` and `Packmol`
  - ✅ File conversion and atom reordering for `.inpt`
  - ✅ Electrode lattice generation and insertion
  - ✅ Full `.prm` file writer for NVE, NVT, NPT
- Compatible with `.gro`, `.xyz`, `.els`, `mass.txt`, `electrode.txt`
- Automatically recognizes molecules, ions, and electrodes
- Supports charge types: `point`, `neutral`, `gaussian`
- Uses Lorentz-Berthelot rules for Lennard-Jones parameters
- Electrode crystal types supported: `hexagonal`, `CFC(100)`, `CFC(110)`, `CFC(111)`

---

## 📦 Installation

### Requirements

- Python 3.8 or higher
- `tkinter` (included by default with Python)
- `numpy`

### Installation

Clone the repository and install the required packages:

git clone https://github.com/julwolff/M-SimBu.git
cd M-SimBu
pip install -r requirements.txt


▶️ How to Use
Launch the graphical interface from the root directory:


python main.py

This will open a GUI with four independent tools:

Box Generator	Builds packed structures using fftool
Format for MW	Converts .gro or .xyz to .inpt
Electrode Generator	Adds electrodes based on lattice templates
Parameter Generator	Writes .prm files for MetalWalls

📂 Input File Formats
Detailed input file specifications can be found in the docs folder.

Basic requirements:

mass.txt: List of element names and atomic masses
.xyz: Molecule structure file (XYZ format)
.els: Atom types, charges, Lennard-Jones parameters, and force field terms
electrode.txt: Crystal definitions and charge models for electrodes

🧪 Testing (optional)

pytest core/tests/


🧑‍🔬 Example Workflow

1. Create your molecule and parameter files (.xyz, .els, mass.txt)
2. Open ElecSim via python main.py
3. Use Box Generator to place molecules in a simulation box
4. Use Format for MW to convert structure into .inpt
5. Use Electrode Generator to insert lattice-defined electrodes
6. Use Parameter Generator to define simulation settings in .prm
7. Launch your MetalWalls simulation with the prepared files

📄 License
This project is licensed under the MIT License.

