# MW-Gui-Builder Workflow

This document explains the general workflow of MW-Gui-Builder and the role of the different files and tools involved in preparing a MetalWalls simulation.

For installation, see [`start.md`](start.md).

For a practical example, continue to the tutorial directories in the repository.

---

## 1. General philosophy

MW-Gui-Builder is a graphical interface designed to simplify the preparation of molecular dynamics simulations for MetalWalls.

It does not replace MetalWalls itself. Instead, it helps prepare the files required before running a MetalWalls simulation.

A simplified workflow is:

```text
Molecular / electrode input
          │
          ▼
   MW-Gui-Builder
          │
          ├── Molecule preparation
          │
          ├── Force-field preparation
          │
          ├── Box generation
          │       │
          │       ├── fftool
          │       └── Packmol
          │
          ├── Electrode generation
          │
          └── MetalWalls parameters
          │
          ▼
   Simulation-ready files
          │
          ▼
      MetalWalls
```

The GUI therefore acts as a preparation layer between the user's molecular/electrode information and the final MetalWalls input files.

---

## 2. Working directory

MW-Gui-Builder is designed to work in the directory from which the GUI is launched.

A typical working directory can look like:

```text
my_simulation/
├── molecules/
├── generated/
└── simbox.xyz
```

Additional MetalWalls input files can be generated depending on the workflow.

The important distinction is between **input/reference files** and **generated files**.

---

## 3. The `molecules/` directory

The `molecules/` directory contains molecular files supplied by the user.

Typical files include:

```text
molecules/
├── tip4p.xyz
├── tip4p.els
├── na.xyz
├── na.els
└── ...
```

The exact files depend on the molecular system.

### `.xyz` files

XYZ files provide the molecular structure and atomic coordinates.

They are used as the structural definition of the molecular species.

### `.els` files

ELS files provide electrostatic information used by the MetalWalls workflow.

For a molecule that requires an ELS file, the corresponding `.xyz` and `.els` files should be kept together.

The `molecules/` directory should contain the original/reference files that you want to reuse.

---

## 4. The `generated/` directory

The `generated/` directory contains files produced automatically during the preparation workflow.

Depending on the selected tools and options, it can contain files such as:

```text
generated/
├── ff.ff
├── tip4p_ff.xyz
├── tip4p_ff_pack.xyz
├── pack.inp
└── electrode_*.els
```

These files are intermediate preparation files.

They can generally be regenerated from the original input files, so keeping the `generated/` directory separate makes it easier to clean a calculation and start again.

For example:

```bash
rm -rf generated
mkdir generated
```

Do not delete the original molecular files in `molecules/`.

---

## 5. The simulation box

The assembled molecular box is written as:

```text
simbox.xyz
```

Unlike the intermediate files in `generated/`, `simbox.xyz` represents the resulting simulation-box structure and can be considered a main output of the box-generation workflow.

It can be inspected with an XYZ-compatible molecular visualization program.

---

## 6. Molecule preparation

When molecules are selected in the GUI, MW-Gui-Builder uses the corresponding molecular information to prepare the files required for box generation.

For workflows using `fftool`, the general process is:

```text
molecules/*.xyz
       │
       ▼
    fftool
       │
       ├── force-field information
       └── Packmol preparation
```

The generated force-field and intermediate files are stored in `generated/`.

MW-Gui-Builder includes the required `fftool` executable as part of the package, so users do not need to manually copy it into the working directory.

---

## 7. Packmol and box generation

Packmol is used to arrange the requested number of molecules inside the simulation box.

The workflow is approximately:

```text
Molecular input
      │
      ▼
MW-Gui-Builder
      │
      ▼
    fftool
      │
      ▼
  Packmol input
      │
      ▼
    Packmol
      │
      ▼
Molecular packing
      │
      ▼
   simbox.xyz
```

The Packmol input file is an intermediate file and is stored in:

```text
generated/pack.inp
```

The exact dimensions and number of molecules depend on the options selected in the GUI.

---

## 8. Density and box dimensions

The box-generation workflow can be configured according to the desired system geometry.

Depending on the selected option, the user can define the system using parameters such as:

- molecular density;
- box dimensions;
- box geometry;
- number of molecules.

MW-Gui-Builder then prepares the corresponding Packmol/box-generation workflow.

The generated box should always be checked before using it in a production simulation.

---

## 9. Electrode Builder

For electrochemical systems, an electrode structure can be prepared with the Electrode Builder.

The electrode-generation workflow produces electrode files in:

```text
generated/electrode_<name>.els
```

The electrode builder is intended to simplify the preparation of electrode geometries and their associated MetalWalls electrode information.

A typical workflow is:

```text
Electrode parameters
        │
        ▼
 Electrode Builder
        │
        ▼
generated/electrode_*.els
```

The resulting electrode file can then be used by the subsequent parameter-generation workflow.

---

## 10. Parameter Generator

Once the molecular box and electrode information are available, the Parameter Generator can be used to prepare the corresponding MetalWalls parameters.

It combines information from the generated system and the selected simulation settings.

Conceptually:

```text
simbox.xyz
     +
electrode information
     +
simulation parameters
     │
     ▼
Parameter Generator
     │
     ▼
MetalWalls input
```

The exact files produced depend on the selected configuration.

---

## 11. Complete preparation workflow

For a complete electrode/electrolyte system, the overall workflow can therefore be summarized as:

```text
1. Prepare molecular input
          │
          ▼
2. Generate molecular box
          │
          ├── fftool
          └── Packmol
          │
          ▼
3. Prepare electrode
          │
          ▼
4. Generate MetalWalls parameters
          │
          ▼
5. Inspect generated files
          │
          ▼
6. Run MetalWalls
```

Each stage can be checked independently.

This is intentional: the generated files remain accessible rather than being hidden inside the GUI.

---

## 12. Reproducibility

A reproducible workflow should preserve:

- the original files in `molecules/`;
- the MW-Gui-Builder version;
- the settings selected in the GUI;
- the resulting `simbox.xyz`;
- the generated MetalWalls input files;
- the relevant generated files when they are needed to document the calculation.

The `generated/` directory can be regenerated, but preserving it can be useful when documenting or debugging a particular preparation.

---

## 13. Cleaning a working directory

Because `generated/` contains intermediate files, it can be cleaned before starting a new preparation:

```bash
rm -rf generated
mkdir generated
```

The original molecular files should remain untouched:

```text
molecules/
```

Similarly, keep any final simulation results or MetalWalls input files that you want to archive.

---

## 14. From workflow to tutorials

The workflow above describes the general logic of MW-Gui-Builder.

The tutorial examples then apply this workflow to concrete systems.

The recommended progression is:

```text
Getting started
      │
      ▼
Workflow overview
      │
      ▼
First tutorial
      │
      ▼
Electrode / electrolyte examples
      │
      ▼
More advanced MetalWalls systems
```

Start with the simplest tutorial available in the example directory before moving to more complex electrochemical systems.
