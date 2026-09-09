# Getting Started

This page explains how to install MW-Gui-Builder from the source repository and launch the graphical interface.

If you simply want to use the software, follow the steps below. The development and test workflow is described separately.

---

## 1. Clone the repository

Clone the GitHub repository:

```bash
git clone https://github.com/julwolff/MW-Gui-Builder.git
cd MW-Gui-Builder
```

---

## 2. Create a virtual environment

Using a virtual environment is recommended to keep the MW-Gui-Builder dependencies isolated from other Python projects.

```bash
python -m venv .venv
```

Activate the environment.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

You should now see `.venv` in your terminal prompt.

---

## 3. Install MW-Gui-Builder

Install the package from the repository:

```bash
pip install .
```

This installs MW-Gui-Builder and its Python dependencies, including NumPy and Packmol.

You can verify the installation with:

```bash
pip show mw-gui-builder
```

---

## 4. Check Tkinter

MW-Gui-Builder uses Tkinter for its graphical interface.

On many Python installations, Tkinter is already available. Test it with:

```bash
python -m tkinter
```

A small test window should appear.

On Debian/Ubuntu systems, Tkinter may need to be installed separately:

```bash
sudo apt install python3-tk
```

Tkinter is a system/Python component rather than a regular `pip` dependency, so its installation can depend on your operating system.

---

## 5. Launch the interface

Once the installation is complete, start MW-Gui-Builder with:

```bash
mw-gui-builder
```

The graphical interface should open.

You can run the command from the directory where you want to prepare a simulation. You do not need to run it from the source repository after installation.

---

## 6. Where to go next

MW-Gui-Builder is organized around several preparation steps rather than a single simulation workflow.

Before starting a tutorial, it is useful to understand how the program handles input files, generated files, molecular force fields, Packmol, electrodes, and MetalWalls parameters.

Read [`workflow.md`](workflow.md) for an overview of how MW-Gui-Builder works.

After that, go to the example/tutorial directory and follow the first tutorial step by step.

---

## For developers

If you are modifying MW-Gui-Builder itself, install it in editable mode instead:

```bash
pip install -e .
```

The test suite requires `pytest`:

```bash
pip install pytest
```

Run the tests with:

```bash
python -m pytest
```

The tests are **not required for normal users**. They are intended for developers and contributors who modify the source code and want to verify that existing functionality still works.
