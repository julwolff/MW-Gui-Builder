# -*- coding: utf-8 -*-
"""
GUI Tool to convert .xyz files to MetalWalls .inp format

Refactored on Mon Jun 30 2025 by ChatGPT
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.xyz2inp import (
    mw_file_writting,
    extract_lines_as_a_list,
    formate_lines,
    convert_list_from_int_to_string
)

class GuiConverter:
    """Interface graphique pour convertir un fichier .xyz en fichier .inp compatible MetalWalls."""

    ANG_TO_BOHR_CONV = 1.890
    MARGIN = 1.0

    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("XYZ to MetalWalls Converter")

        self._init_variables()
        self._build_widgets()

    def _init_variables(self):
        self.input_path_var = tk.StringVar()
        self.output_name_var = tk.StringVar()

    def _build_widgets(self):
        frm = ttk.Frame(self.master, padding=10)
        frm.grid(sticky="nsew")

        ttk.Label(frm, text="Input .xyz file:").grid(row=0, column=0, sticky="w")
        entry_input = ttk.Entry(frm, textvariable=self.input_path_var, width=50)
        entry_input.grid(row=0, column=1, sticky="ew")
        ttk.Button(frm, text="Browse", command=self._browse_input_file).grid(row=0, column=2, padx=5)

        ttk.Label(frm, text="Output .inp file name:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.output_name_var, width=50).grid(row=1, column=1, columnspan=2, sticky="ew")

        self.progress = ttk.Label(frm, text="")
        self.progress.grid(row=2, column=0, columnspan=3, pady=5)

        ttk.Button(frm, text="Convert", command=self.launch).grid(row=3, column=0, columnspan=3, pady=10)

        frm.columnconfigure(1, weight=1)

    def _browse_input_file(self):
        path = filedialog.askopenfilename(filetypes=[("XYZ files", "*.xyz")])
        if path:
            self.input_path_var.set(path)

    def launch(self):
        """Convertit le fichier .xyz en .inp pour MetalWalls avec calcul de la boîte et mise en forme."""
        input_path = self.input_path_var.get().strip()
        output_name = self.output_name_var.get().strip()

        if not input_path or not output_name:
            messagebox.showerror("Erreur", "Veuillez remplir les deux champs.")
            return

        if not os.path.exists(input_path):
            messagebox.showerror("Erreur", f"Le fichier '{input_path}' n'existe pas.")
            return

        self.progress.config(text="🕒 Conversion en cours...")
        self.master.update_idletasks()

        try:
            # Lire les coordonnées
            with open(input_path, "r") as f:
                lines = f.readlines()

            atom_number = int(lines[0].split()[0])
            try:
                electrode_atom_number = int(lines[1].split()[8])
            except (IndexError, ValueError):
                electrode_atom_number = 0
                messagebox.showwarning("Attention", "Nombre d'atomes de l'électrode non trouvé. Mis à 0.")

            x, y, z = [], [], []
            for i, line in enumerate(lines[2:], start=3):
                tokens = line.split()
                if len(tokens) < 4:
                    raise ValueError(f"Ligne {i} invalide : {line.strip()}")
                x.append(float(tokens[1]))
                y.append(float(tokens[2]))
                z.append(float(tokens[3]))

            # Boîte de simulation
            x_box = (max(x) + self.MARGIN) * self.ANG_TO_BOHR_CONV
            y_box = (max(y) + self.MARGIN) * self.ANG_TO_BOHR_CONV
            z_box = (max(z) + self.MARGIN) * self.ANG_TO_BOHR_CONV

            header = convert_list_from_int_to_string([atom_number, electrode_atom_number, x_box, y_box, z_box])
            atom_lines = extract_lines_as_a_list(input_path)
            formatted_atoms = formate_lines(atom_lines)

            mw_file_writting(input_path, output_name, header, formatted_atoms)

            self.progress.config(text="✅ Conversion terminée")
            messagebox.showinfo("Succès", f"Fichier converti avec succès en '{output_name}'")

        except Exception as e:
            self.progress.config(text="❌ Erreur")
            messagebox.showerror("Erreur de conversion", f"Une erreur est survenue :\n{e}")
            return

if __name__ == "__main__":
    root = tk.Tk()
    GuiConverter(root)
    root.mainloop()
