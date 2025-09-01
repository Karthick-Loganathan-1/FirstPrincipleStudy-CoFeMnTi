#!/usr/bin/env python3
"""
Plot DOS and PDOS for CoFeMnTi Quaternary Heusler alloy
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Set up matplotlib for better plots
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['lines.linewidth'] = 2

def read_dos_file(filename):
    """Read DOS file and return energy, dos_up, dos_down, fermi_energy"""
    with open(filename, 'r') as f:
        header = f.readline()
        # Extract Fermi energy from header
        fermi_str = header.split('EFermi =')[1].split('eV')[0].strip()
        fermi_energy = float(fermi_str)
    
    data = np.loadtxt(filename, comments='#')
    energy = data[:, 0]
    dos_up = data[:, 1]
    dos_down = -data[:, 2]  # Negative for spin-down
    
    return energy, dos_up, dos_down, fermi_energy

def read_pdos_file(filename):
    """Read PDOS file and return energy, pdos_up, pdos_down"""
    data = np.loadtxt(filename, comments='#')
    energy = data[:, 0]
    
    # For d-orbitals, sum all d-orbital contributions
    if '_wfc#' in filename and '(d)' in filename:
        # For d-orbitals: columns are E, ldos_up, ldos_down, then 5 d-orbitals * 2 spins
        pdos_up = np.sum(data[:, 3::2], axis=1)  # Sum odd columns (d-orbital spin-up)
        pdos_down = -np.sum(data[:, 4::2], axis=1)  # Sum even columns (d-orbital spin-down), negative
    else:
        # For s,p orbitals: usually ldos_up, ldos_down in columns 1,2
        pdos_up = data[:, 1] if data.shape[1] > 1 else data[:, 1]
        pdos_down = -data[:, 2] if data.shape[1] > 2 else -data[:, 2]
    
    return energy, pdos_up, pdos_down

def plot_total_dos():
    """Plot total DOS"""
    energy, dos_up, dos_down, fermi_energy = read_dos_file('CoFeMnTi.dos')
    
    plt.figure(figsize=(10, 6))
    plt.plot(energy - fermi_energy, dos_up, 'b-', label='Spin Up', linewidth=1.5)
    plt.plot(energy - fermi_energy, dos_down, 'r-', label='Spin Down', linewidth=1.5)
    plt.axvline(0, color='k', linestyle='--', alpha=0.7, label='Fermi Level')
    plt.fill_between(energy - fermi_energy, dos_up, alpha=0.3, color='blue')
    plt.fill_between(energy - fermi_energy, dos_down, alpha=0.3, color='red')
    
    plt.xlabel('Energy - E_F (eV)')
    plt.ylabel('DOS (states/eV)')
    plt.title('Total Density of States - CoFeMnTi')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(-8, 8)
    plt.tight_layout()
    plt.savefig('CoFeMnTi_total_dos.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Total DOS plot saved as: CoFeMnTi_total_dos.png")

def plot_atomic_pdos():
    """Plot atomic-resolved PDOS for d-orbitals"""
    # Get Fermi energy from DOS file
    _, _, _, fermi_energy = read_dos_file('CoFeMnTi.dos')
    
    # Find d-orbital PDOS files for each atom
    atoms = ['Fe', 'Co', 'Mn', 'Ti']
    colors = ['blue', 'green', 'red', 'orange']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, atom in enumerate(atoms):
        # Find the d-orbital file for this atom
        d_files = glob.glob(f"CoFeMnTi.pdos_atm#{i+1}({atom})_wfc*d)")
        
        if d_files:
            filename = d_files[0]
            energy, pdos_up, pdos_down = read_pdos_file(filename)
            
            axes[i].plot(energy - fermi_energy, pdos_up, color=colors[i], 
                        label=f'{atom} d-up', linewidth=1.5)
            axes[i].plot(energy - fermi_energy, pdos_down, color=colors[i], 
                        linestyle='--', label=f'{atom} d-down', linewidth=1.5)
            axes[i].axvline(0, color='k', linestyle='-', alpha=0.7, linewidth=0.8)
            axes[i].fill_between(energy - fermi_energy, pdos_up, alpha=0.3, color=colors[i])
            axes[i].fill_between(energy - fermi_energy, pdos_down, alpha=0.3, color=colors[i])
            
            axes[i].set_xlabel('Energy - E_F (eV)')
            axes[i].set_ylabel('PDOS (states/eV)')
            axes[i].set_title(f'{atom} d-orbitals PDOS')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
            axes[i].set_xlim(-8, 8)
    
    plt.tight_layout()
    plt.savefig('CoFeMnTi_atomic_pdos.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Atomic PDOS plot saved as: CoFeMnTi_atomic_pdos.png")

def plot_combined_dos_pdos():
    """Plot combined DOS and PDOS in one figure"""
    # Get total DOS
    energy, dos_up, dos_down, fermi_energy = read_dos_file('CoFeMnTi.dos')
    
    # Get d-orbital PDOS for each atom
    atoms = ['Fe', 'Co', 'Mn', 'Ti']
    colors = ['blue', 'green', 'red', 'orange']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot total DOS
    ax1.plot(energy - fermi_energy, dos_up, 'k-', label='Total Spin Up', linewidth=2)
    ax1.plot(energy - fermi_energy, dos_down, 'k--', label='Total Spin Down', linewidth=2)
    ax1.axvline(0, color='gray', linestyle='-', alpha=0.8, linewidth=1)
    ax1.fill_between(energy - fermi_energy, dos_up, alpha=0.2, color='black')
    ax1.fill_between(energy - fermi_energy, dos_down, alpha=0.2, color='black')
    
    ax1.set_ylabel('Total DOS (states/eV)')
    ax1.set_title('CoFeMnTi - Total DOS and Atomic d-orbital PDOS')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-8, 8)
    
    # Plot atomic PDOS (d-orbitals only)
    for i, atom in enumerate(atoms):
        d_files = glob.glob(f"CoFeMnTi.pdos_atm#{i+1}({atom})_wfc*d)")
        
        if d_files:
            filename = d_files[0]
            energy_pdos, pdos_up, pdos_down = read_pdos_file(filename)
            
            # Plot only spin-up for clarity
            ax2.plot(energy_pdos - fermi_energy, pdos_up, color=colors[i], 
                    label=f'{atom} d-up', linewidth=1.5)
            ax2.fill_between(energy_pdos - fermi_energy, pdos_up, alpha=0.3, color=colors[i])
    
    ax2.axvline(0, color='gray', linestyle='-', alpha=0.8, linewidth=1)
    ax2.set_xlabel('Energy - E_F (eV)')
    ax2.set_ylabel('PDOS (states/eV)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-8, 8)
    
    plt.tight_layout()
    plt.savefig('CoFeMnTi_combined_dos_pdos.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Combined DOS/PDOS plot saved as: CoFeMnTi_combined_dos_pdos.png")

def print_magnetic_analysis():
    """Print magnetic moment analysis"""
    print("\n=== MAGNETIC ANALYSIS ===")
    print("From SCF calculation:")
    print("Fe: +1.09 μB")
    print("Co: +1.09 μB") 
    print("Mn: +2.62 μB")
    print("Ti: -0.39 μB")
    print("Total: +4.17 μB/cell")
    print("\nThis suggests a ferrimagnetic configuration with:")
    print("- High spin Mn (strongest magnetic moment)")
    print("- Moderate spin Fe and Co")
    print("- Antiferromagnetic coupling with Ti")

if __name__ == "__main__":
    print("Plotting DOS and PDOS for CoFeMnTi Quaternary Heusler Alloy")
    print("=" * 60)
    
    # Plot total DOS
    plot_total_dos()
    
    # Plot atomic PDOS
    plot_atomic_pdos()
    
    # Plot combined figure
    plot_combined_dos_pdos()
    
    # Print magnetic analysis
    print_magnetic_analysis()
    
    print("\n" + "=" * 60)
    print("All plots have been generated and saved!")
    print("Files created:")
    print("- CoFeMnTi_total_dos.png")
    print("- CoFeMnTi_atomic_pdos.png") 
    print("- CoFeMnTi_combined_dos_pdos.png")
