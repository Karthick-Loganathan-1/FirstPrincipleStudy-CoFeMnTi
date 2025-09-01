# First-Principles Study of CoFeMnTi Quaternary Heusler Alloy

## Overview
This repository contains a comprehensive density functional theory (DFT) study of the CoFeMnTi quaternary Heusler alloy using Quantum ESPRESSO. The investigation covers structural optimization, electronic structure, magnetic properties, and density of states analysis.

## Abstract
We present first-principles calculations of the CoFeMnTi quaternary Heusler alloy, revealing a ferrimagnetic metallic ground state with strong spin polarization. The material adopts the L2₁ Heusler structure with a calculated lattice parameter of 5.80 Å and exhibits a total magnetic moment of 4.17 μB/cell. The electronic structure shows metallic character with significant d-orbital contributions near the Fermi level.

## Repository Structure

```
├── input_files/           # Quantum ESPRESSO input files
├── output_files/          # Calculation output files and raw data
├── analysis/              # Scientific analysis reports
├── plots/                 # Electronic structure visualizations
├── scripts/               # Python plotting scripts
├── pseudopotentials/      # PAW pseudopotential files
└── README.md             # This file
```

## Key Results

### Structural Properties
- **Crystal structure**: L2₁ Heusler (space group F-43m)
- **Optimized lattice parameter**: 5.80 Å
- **Unit cell volume**: 48.84 Å³
- **Calculated density**: 7.40 g/cm³

### Magnetic Properties
- **Magnetic ground state**: Ferrimagnetic
- **Total magnetization**: 4.17 μB/cell
- **Local magnetic moments**:
  - Fe: +1.09 μB
  - Co: +1.09 μB
  - Mn: +2.62 μB (highest)
  - Ti: -0.39 μB (antiferromagnetic)

### Electronic Structure
- **Electronic character**: Metallic
- **Fermi energy**: 17.58 eV
- **DOS at Fermi level**: 7.3 states/eV·cell
- **Spin polarization**: ~50%
- **d-orbital dominance**: Electronic properties governed by transition metal d-states

## Computational Details

### Software and Methods
- **DFT code**: Quantum ESPRESSO v7.0
- **Exchange-correlation functional**: PBE-GGA
- **Pseudopotentials**: PAW ultrasoft
- **Basis set**: Plane waves

### Parameters
- **Energy cutoffs**: 60 Ry (wavefunction), 480 Ry (charge density)
- **k-point meshes**: 12×12×12 (SCF), 20×20×20 (NSCF)
- **Convergence threshold**: 1×10⁻⁸ Ry
- **Smearing**: Marzari-Vanderbilt (0.02 Ry)

## Calculations Performed

1. **Variable-cell relaxation** - Structural optimization
2. **Self-consistent field (SCF)** - Ground state properties
3. **Non-self-consistent field (NSCF)** - Dense k-point sampling
4. **Density of states (DOS)** - Electronic density analysis
5. **Projected DOS (PDOS)** - Orbital-resolved electronic structure
6. **Band structure** - Electronic dispersion along high-symmetry path

## File Descriptions

### Input Files (`input_files/`)
- `CoFeMnTi-VC-Cf2.in` - Variable-cell relaxation input
- `CoFeMnTi-SCF.in` - Self-consistent field calculation
- `CoFeMnTi-NSCF.in` - Non-self-consistent field for DOS
- `CoFeMnTi-DOS.in` - Density of states calculation
- `CoFeMnTi-PDOS.in` - Projected density of states
- `CoFeMnTi-bands-NSCF-fixed.in` - Band structure calculation (corrected)
- `CoFeMnTi-bands-fixed.in` - Band post-processing

### Output Files (`output_files/`)
- `CoFeMnTi-VC-relax.out` - Structural optimization results
- `CoFeMnTi-SCF.out` - Ground state electronic structure
- `CoFeMnTi-NSCF.out` - Dense k-point electronic structure
- `CoFeMnTi.dos` - Total density of states data
- `CoFeMnTi.pdos_tot` - Total projected density of states
- `CoFeMnTi_fixed.bands.gnu` - Band structure data (corrected)

### Analysis (`analysis/`)
- `CoFeMnTi_Scientific_Analysis.md` - Comprehensive theoretical analysis
- `CoFeMnTi_Results_Summary.txt` - Numerical results summary

### Visualizations (`plots/`)
- `CoFeMnTi_total_dos.png` - Total density of states
- `CoFeMnTi_atomic_pdos.png` - Atomic-resolved PDOS
- `CoFeMnTi_combined_dos_pdos.png` - Combined DOS/PDOS view
- `CoFeMnTi_detailed_pdos.png` - Detailed orbital contributions
- `CoFeMnTi_d_orbital_comparison.png` - d-orbital comparison
- `CoFeMnTi_bands_corrected.png` - Corrected band structure
- `CoFeMnTi_bands_detailed.png` - Detailed band analysis
- `CoFeMnTi_bands_comparison.png` - Band structure comparison

### Scripts (`scripts/`)
- `plot_dos_pdos.py` - DOS and PDOS plotting script
- `plot_detailed_pdos.py` - Detailed PDOS analysis
- `plot_bands_improved.py` - Band structure plotting
- `plot_spin_resolved_bands.py` - Advanced band analysis

## Scientific Significance

This work provides the first comprehensive first-principles characterization of the CoFeMnTi quaternary Heusler alloy, contributing to:

1. **Theoretical understanding** of quaternary Heusler electronic structure
2. **Magnetic exchange mechanisms** in complex four-sublattice systems
3. **Structure-property relationships** in transition metal alloys
4. **Computational methodology** for complex magnetic materials

## Key Findings

1. **Ferrimagnetic ground state** with competing magnetic interactions
2. **Metallic electronic structure** with high spin polarization
3. **Structural stability** in L2₁ Heusler phase
4. **Strong d-orbital character** governing electronic properties
5. **Mn-dominated magnetism** with Ti antiferromagnetic coupling

