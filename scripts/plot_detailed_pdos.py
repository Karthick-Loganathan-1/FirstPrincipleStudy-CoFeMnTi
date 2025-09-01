#!/usr/bin/env python3
"""
Detailed PDOS plot for CoFeMnTi showing s and d orbital contributions
"""

import numpy as np
import matplotlib.pyplot as plt
import glob

def read_dos_file(filename):
    """Read DOS file and return energy, dos_up, dos_down, fermi_energy"""
    with open(filename, 'r') as f:
        header = f.readline()
        fermi_str = header.split('EFermi =')[1].split('eV')[0].strip()
        fermi_energy = float(fermi_str)
    
    data = np.loadtxt(filename, comments='#')
    energy = data[:, 0]
    dos_up = data[:, 1]
    dos_down = -data[:, 2]
    
    return energy, dos_up, dos_down, fermi_energy

def read_pdos_d(filename):
    """Read d-orbital PDOS file"""
    data = np.loadtxt(filename, comments='#')
    energy = data[:, 0]
    pdos_up = np.sum(data[:, 3::2], axis=1)  # Sum all d-orbital spin-up
    pdos_down = -np.sum(data[:, 4::2], axis=1)  # Sum all d-orbital spin-down
    return energy, pdos_up, pdos_down

def read_pdos_s(filename):
    """Read s-orbital PDOS file"""
    data = np.loadtxt(filename, comments='#')
    energy = data[:, 0]
    pdos_up = data[:, 1]  # s-orbital spin-up
    pdos_down = -data[:, 2]  # s-orbital spin-down
    return energy, pdos_up, pdos_down

def plot_detailed_pdos():
    """Plot detailed PDOS with s and d contributions for each atom"""
    _, _, _, fermi_energy = read_dos_file('CoFeMnTi.dos')
    
    atoms = ['Fe', 'Co', 'Mn', 'Ti']
    colors = ['blue', 'green', 'red', 'orange']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for i, atom in enumerate(atoms):
        # Find s and d orbital files
        s_files = glob.glob(f"CoFeMnTi.pdos_atm#{i+1}({atom})_wfc*s)")
        d_files = glob.glob(f"CoFeMnTi.pdos_atm#{i+1}({atom})_wfc*d)")
        
        ax = axes[i]
        
        # Plot d-orbitals
        if d_files:
            energy, d_up, d_down = read_pdos_d(d_files[0])
            ax.plot(energy - fermi_energy, d_up, color=colors[i], 
                   label=f'{atom} d-up', linewidth=2)
            ax.plot(energy - fermi_energy, d_down, color=colors[i], 
                   linestyle='--', label=f'{atom} d-down', linewidth=2)
            ax.fill_between(energy - fermi_energy, d_up, alpha=0.3, color=colors[i])
            ax.fill_between(energy - fermi_energy, d_down, alpha=0.3, color=colors[i])
        
        # Plot s-orbitals (lighter color)
        if s_files:
            energy_s, s_up, s_down = read_pdos_s(s_files[0])
            light_color = plt.cm.get_cmap('Pastel1')(i)
            ax.plot(energy_s - fermi_energy, s_up, color=light_color, 
                   label=f'{atom} s-up', linewidth=1, alpha=0.8)
            ax.plot(energy_s - fermi_energy, s_down, color=light_color, 
                   linestyle=':', label=f'{atom} s-down', linewidth=1, alpha=0.8)
        
        ax.axvline(0, color='k', linestyle='-', alpha=0.7, linewidth=0.8)
        ax.set_xlabel('Energy - E_F (eV)')
        ax.set_ylabel('PDOS (states/eV)')
        ax.set_title(f'{atom} Orbital Contributions')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-8, 8)
    
    plt.tight_layout()
    plt.savefig('CoFeMnTi_detailed_pdos.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Detailed PDOS plot saved as: CoFeMnTi_detailed_pdos.png")

def plot_orbital_comparison():
    """Plot comparison of d-orbital contributions from all atoms"""
    _, _, _, fermi_energy = read_dos_file('CoFeMnTi.dos')
    
    atoms = ['Fe', 'Co', 'Mn', 'Ti']
    colors = ['blue', 'green', 'red', 'orange']
    
    plt.figure(figsize=(12, 8))
    
    for i, atom in enumerate(atoms):
        d_files = glob.glob(f"CoFeMnTi.pdos_atm#{i+1}({atom})_wfc*d)")
        
        if d_files:
            energy, d_up, d_down = read_pdos_d(d_files[0])
            plt.plot(energy - fermi_energy, d_up, color=colors[i], 
                    label=f'{atom} d-up', linewidth=2)
            plt.fill_between(energy - fermi_energy, d_up, alpha=0.2, color=colors[i])
    
    plt.axvline(0, color='k', linestyle='--', alpha=0.8, linewidth=1.5, label='Fermi Level')
    plt.xlabel('Energy - E_F (eV)')
    plt.ylabel('PDOS (states/eV)')
    plt.title('d-orbital Contributions Comparison - CoFeMnTi (Spin Up)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(-8, 8)
    plt.tight_layout()
    plt.savefig('CoFeMnTi_d_orbital_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("d-orbital comparison plot saved as: CoFeMnTi_d_orbital_comparison.png")

if __name__ == "__main__":
    print("Creating detailed PDOS plots for CoFeMnTi")
    print("=" * 50)
    
    plot_detailed_pdos()
    plot_orbital_comparison()
    
    print("\n" + "=" * 50)
    print("Detailed PDOS plots completed!")
