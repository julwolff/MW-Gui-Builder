# MW-Gui-Builder

**MW-Gui-Builder** is an open-source Python package and graphical interface for preparing simulation-ready input files for [MetalWalls](https://gitlab.com/ampere2/MetalWalls), a molecular dynamics software package for constant-potential simulations.

MW-Gui-Builder is designed to simplify the preparation of electrochemical molecular dynamics systems by providing graphical tools for molecular packing, electrode construction, structure conversion, and MetalWalls parameter generation.

## Features

MW-Gui-Builder provides four independent tools:

* **Box Generator**

  * Builds molecular simulation boxes using `fftool` and Packmol.
  * Handles mixtures of molecules and ions.
  * Generates the molecular force-field and packing files required for the simulation.

* **Format for MW**

  * Converts molecular structures into MetalWalls `.inpt` format.
  * Reorders atoms when required by MetalWalls.
  * Handles the conversion of molecular and electrode coordinates.

* **Electrode Generator**

  * Generates crystalline electrode coordinates.
  * Supports several crystal geometries.
  * Inserts electrodes into an existing simulation box.
  * Generates the corresponding MetalWalls `.els` file.

* **Parameter Generator**

  * Generates the MetalWalls simulation input file.
  * Defines simulation parameters such as temperature, ensemble, electrodes, electrostatic settings, and simulation time.

The package is intended to automate repetitive preparation steps while keeping the resulting files accessible to the user.

## Typical workflow

A typical preparation workflow is:

1. Prepare the molecular `.xyz` and `.els` files.
2. Place the molecular files in the `molecules/` directory.
3. Use the **Box Generator** to build the electrolyte box.
4. Use the **Electrode Generator** to generate and insert the electrode.
5. Use **Format for MW** to prepare the structure for MetalWalls.
6. Use the **Parameter Generator** to generate the MetalWalls input file.
7. Run the resulting simulation with MetalWalls.

The detailed workflow and generated files are described in [`workflow.md`](workflow.md).

A step-by-step guide for installing and launching MW-Gui-Builder is available in [`start.md`](start.md).

Example systems and tutorials are available in the [`exemple/`](exemple/) directory.

## Input files

MW-Gui-Builder works with several types of input files.

### Molecular `.xyz` files

Molecules are described using the standard XYZ format:

```text
number_of_atoms
comment
atom    x    y    z
...
```

Example:

```text
3
Water molecule
O    0.000000    0.000000    0.000000
H    0.957200    0.000000    0.000000
H   -0.239987    0.927297    0.000000
```

Molecular examples are provided in the [`molecules/`](molecules/) directory.

### Molecular `.els` files

`.els` files contain the force-field and charge parameters associated with the atom types used by MetalWalls.

A molecular system generally requires both:

```text
molecule.xyz
molecule.els
```

The existing files in `molecules/` can be used as references when preparing new molecules.

### Electrode database

The electrode database is stored in:

```text
src/mw_gui_builder/data/electrode.txt
```

It contains the lattice and electrostatic parameters used by the Electrode Generator.

The currently implemented crystal geometries are:

* `hexagonal`
* `CFC(100)`
* `CFC(110)`
* `CFC(111)`

Additional electrode materials can be added when appropriate parameters are available.

## Directory structure

After cloning the repository, the main directories are organized as follows:

```text
MW-Gui-Builder/
├── exemple/
│   ├── Alkaline_HER_Platinum/
│   ├── Ionic_Liquids_Platinum/
│   └── Water_Graphene/
│
├── molecules/
│   ├── *.xyz
│   └── *.els
│
├── src/
│   └── mw_gui_builder/
│       ├── gui/
│       ├── core/
│       ├── bin/
│       └── data/
│
├── tests/
│
├── README.md
├── start.md
├── workflow.md
├── contributing.md
├── pyproject.toml
└── LICENSE
```

During a simulation preparation, generated intermediate files are placed in the `generated/` directory.

A typical working directory may therefore contain:

```text
working_directory/
├── molecules/
├── generated/
│   ├── ff.ff
│   ├── pack.inp
│   ├── *_ff.xyz
│   └── electrode_*.els
└── simbox.xyz
```

The `molecules/` directory contains user-provided molecular data, while `generated/` contains intermediate files produced by MW-Gui-Builder.

## Installation

### Requirements

MW-Gui-Builder requires:

* Python 3.10 or newer
* Tkinter
* Packmol

`numpy` is installed automatically as a Python dependency.

On Linux, Tkinter may need to be installed separately through the operating system package manager.

For example, on Debian/Ubuntu:

```bash
sudo apt install python3-tk
```

### Install from the repository

Clone the repository:

```bash
git clone https://github.com/julwolff/MW-Gui-Builder.git
cd MW-Gui-Builder
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install MW-Gui-Builder:

```bash
pip install .
```

The package installs its Python dependencies, Packmol, and the bundled `fftool` executable.

## Launching MW-Gui-Builder

After installation, launch the graphical interface with:

```bash
mw-gui-builder
```

The GUI provides access to the four main tools:

```text
Box Generator
Format for MW
Electrode Generator
Parameter Generator
```

For a complete installation and first-use guide, see [`start.md`](start.md).

## Examples and tutorials

The [`exemple/`](exemple/) directory contains example simulation systems and tutorials.

Current examples include:

* **Alkaline HER on Platinum**
* **Ionic liquids on Platinum**
* **Water on Graphene**

Each example can be used as a starting point for preparing a corresponding MetalWalls simulation.

See the relevant `tutorial.md` file inside each example directory for step-by-step instructions.

## Testing

The test suite can be run from the repository root with:

```bash
python -m pytest
```

The tests are primarily intended for development and verification of the package.

To install the development dependency:

```bash
pip install pytest
```

The test suite can then be executed with:

```bash
python -m pytest
```

## Development installation

For development, install the package in editable mode:

```bash
pip install -e .
```

This allows modifications to the source code to be used immediately without reinstalling the package.

Install the testing dependency if needed:

```bash
pip install pytest
```

Then run:

```bash
python -m pytest
```

## Documentation

The repository provides several complementary documents:

* [`start.md`](start.md) — installation and first launch.
* [`workflow.md`](workflow.md) — detailed description of how MW-Gui-Builder prepares a simulation.
* [`exemple/`](exemple/) — practical examples and tutorials.
* [`contributing.md`](contributing.md) — information for contributors.

## Relationship with MetalWalls

MW-Gui-Builder is a preparation and file-generation tool for MetalWalls. It does not replace the MetalWalls molecular dynamics engine.

The package prepares the structures and input files required to perform simulations with MetalWalls, while the actual molecular dynamics simulation is performed by MetalWalls.

For more information about MetalWalls, see the [MetalWalls repository](https://gitlab.com/ampere2/MetalWalls).

## Contributing

Contributions, bug reports, feature requests, and suggestions are welcome.

Please use the GitHub repository to:

* report bugs,
* request new features,
* suggest additional molecular models,
* suggest additional electrode materials,
* improve documentation,
* contribute code or tests.

Before submitting a contribution, please see [`contributing.md`](contributing.md).

## Citation

If you use MW-Gui-Builder in your research, please cite the associated software publication:

> Wolff, J. *et al.* MW-Gui-Builder: a graphical interface for preparing MetalWalls molecular dynamics simulations.

The corresponding citation information is provided in [`paper.bib`](paper.bib).

## License

MW-Gui-Builder is distributed under the **GNU General Public License v3.0 (GPL-3.0)**.

See [`LICENSE`](LICENSE) for the complete license text.
