# Molecule files

This directory contains the molecular definitions used by **MW-Gui-Builder** when generating MetalWalls setups.

Each molecule is described by two files:

```text
molecule.xyz
molecule.els
```

For example:

```text
molecules/
├── emim.xyz
├── emim.els
├── ...
```

## Adding a new molecule

To add a new molecule to the library:

### 1. Create the `.xyz` file

The `.xyz` file contains the molecular geometry:

```text
N_atoms
molecule_name
element   x   y   z
element   x   y   z
...
```

For example:

```text
3
water
O   0.000   0.000   0.000
H   0.758   0.000   0.504
H  -0.758   0.000   0.504
```

The atom order is important because atom indices are used by the corresponding `.els` file.

Atom indices are **zero-based**:

```text
atom 0 → first atom
atom 1 → second atom
atom 2 → third atom
...
```

### 2. Create the `.els` file

The `.els` file contains the force-field information associated with the molecule.

It defines:

* electrostatic parameters and partial charges;
* non-bonded parameters;
* harmonic bonds;
* constraints;
* harmonic angles;
* dihedrals;
* impropers.

The atom ordering must be exactly the same as in the `.xyz` file.

For example, if the `.xyz` file contains:

```text
0  O
1  H
2  H
```

then all atom definitions and intramolecular interactions in the `.els` file must use these indices.

### 3. Check the molecular charge

Verify that the partial charges defined in the `.els` file give the intended total molecular charge.

For example:

```text
q_total = Σ q_i
```

This is particularly important for ions.

### 4. Check all atom indices

Every atom index appearing in the `.els` file must correspond to an atom in the `.xyz` file.

For a molecule containing `N` atoms, valid indices are:

```text
0 ... N-1
```

### 5. Test the molecule

After adding the two files, use the molecule in a minimal setup and verify that MW-Gui-Builder can generate the corresponding MetalWalls input without errors.

A molecule should ideally be tested before being used in a larger production setup.

---

## File naming

The two files must share the same base name:

```text
my_molecule.xyz
my_molecule.els
```

Do not use:

```text
my_molecule.xyz
another_name.els
```

unless the setup-generation code explicitly expects such a naming scheme.

---

## Recommended workflow

A typical workflow for adding a new molecule is:

```text
              Molecular structure
                      │
                      ▼
                Create .xyz
                      │
                      ▼
             Assign atom ordering
                      │
                      ▼
                Create .els
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   Check charges          Check interactions
          │                       │
          └───────────┬───────────┘
                      ▼
              Generate a setup
                      │
                      ▼
               Test with MW
```

## Important: atom ordering

The most common source of errors is an inconsistency between the `.xyz` and `.els` files.

For example:

```text
molecule.xyz

0  O
1  H
2  H
```

must correspond to the same indexing in:

```text
molecule.els

... atom 0 ...
... atom 1 ...
... atom 2 ...
```

If the atom order is changed in the XYZ file, the corresponding indices in the `.els` file must also be changed.

---

## Example: EMIM

The `emim` files provide a complete example:

```text
emim.xyz
emim.els
```

`emim.xyz` contains the 19-atom molecular geometry, while `emim.els` contains the corresponding electrostatic and intramolecular parameters.

The commented files can be used as a template when creating another molecule.

For a detailed explanation of the syntax of both files, see:

**[`molecule_file_tutorial.md`](molecule_file_tutorial.md)**

---

## Checklist

Before adding a molecule, check:

* [ ] `.xyz` file exists.
* [ ] `.els` file exists.
* [ ] Both files have the same base name.
* [ ] Number of atoms in `.xyz` is correct.
* [ ] Atom ordering is consistent between `.xyz` and `.els`.
* [ ] Atom indices are zero-based.
* [ ] Every atom has the required electrostatic parameters.
* [ ] Total molecular charge is correct.
* [ ] All bond/angle/dihedral/improper indices are valid.
* [ ] The molecule can be loaded by MW-Gui-Builder.
* [ ] A generated setup has been tested successfully.

