# Tutorial: Ionic Liquid [EMIM][TFSI] split by Pt electrode

## 1. Generate the Water Box

1. Launch the application:  
   ```bash
   python main.py
   ```

2. Click on **"Box Generation"**.

3. Fill in the molecule information:  
   - **Molecule name:** `tip4p.xyz`  
   - **Molecule number:** `3000`  
   Then click **"Add"**.

   - **Molecule name:** `na.xyz`  
   - **Molecule number:** `54`  
   Then click **"Add"**.

   - **Molecule name:** `oh.xyz`  
   - **Molecule number:** `54`  
   Then click **"Add"**.


4. Click on **"Density"** and select **"z 5:1"**.

5. Enter the density:  
   - **Density:** `57.5`

6. Click on **"Launch"** and validate each step.
/!\  The generation is quite long. Be patient.
---

## 2. Generate the First Electrode

1. Close the Box Generation window and click on **"Electrode Generation"**.

2. In the **Input** field, write:
   ```
   simbox.xyz
   ```

3. Write the desired electrode name (e.g., **Pt1** in the example).

4. Select **"Pt(100)"** in the electrode menu.

5. Set the electrode parameters:
   - **Electrode position:** `132`
   - **z dimension:** `8`
   - **Buffer:** `2`

6. Click **"Launch"**.  
   This generates a file named:
   ```
   simbox_electrode.xyz
   ```

---

## 3. Generate the Second Electrode

1. In the **Input** field, write:
   ```
   simbox_electrode.xyz
   ```

2. Change the electrode name (e.g., **Pt0** in the example).
Keep other parameters the same

3. Set the electrode parameters:
   - **Electrode position:** `0`
   - **z dimension:** `8`
   - **Buffer:** `2`

4. Click **"Launch"**.  
   This generates the final structure file:
   ```
   simbox_electrode_electrode.xyz
   ```

---

## 4. Generate the Parameter File

1. Close the Electrode Generator and open **"Parameter Generator"**.

2. Fill in:
   - **Input file:** `simbox_electrode_electrode.xyz`
   - **Temperature:** *(your desired value)*
   - **Simulation steps:** *(your desired value)*

3. Make sure the **NVT** box is selected (if not already).

4. Click **"Generate parameters"**.

---

## 5. Export to MetalWalls Format

1. Close the Parameter Generator and open **"Format for MetalWalls"**.

2. Select the file:
   ```
   simbox_electrode_electrode.xyz
   ```

3. MetalWalls uses **data.inpt** as the default file name.  
   It is recommended to keep this name.

4. Click **"Launch"**.

---

## 6. Run simulation

You now go the 
   ```bash
   runtime.inpt
   ```

 and

   ```bash
   data.inpt
   ```

file needed to launch a simulation with Metalwalls package.
To launch it, go in the file containing .inpt file and run 

   ```bash
   path/mw
   ```
