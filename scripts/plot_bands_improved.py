#!/usr/bin/env python3
"""
Improved band structure plot for CoFeMnTi with proper discontinuity handling
"""

import numpy as np
import matplotlib.pyplot as plt

def read_dos_fermi(filename):
    """Get Fermi energy from DOS file"""
    with open(filename, 'r') as f:
        header = f.readline()
        fermi_str = header.split('EFermi =')[1].split('eV')[0].strip()
        fermi_energy = float(fermi_str)
    return fermi_energy

def plot_bands_improved():
    """Plot band structure with proper handling of k-point segments"""
    fermi_energy = read_dos_fermi('CoFeMnTi.dos')
    
    # Read the corrected .gnu file
    try:
        data = np.loadtxt('CoFeMnTi_fixed.bands.gnu')
    except:
        print("Using original bands file as fallback")
        data = np.loadtxt('CoFeMnTi.bands.gnu')
    
    k_coord = data[:, 0]
    energy = data[:, 1]
    
    # Find band indices where k-coordinate resets (indicates new band)
    band_breaks = [0]
    for i in range(1, len(k_coord)):
        if k_coord[i] < k_coord[i-1]:  # k-coordinate resets
            band_breaks.append(i)
    band_breaks.append(len(k_coord))
    
    plt.figure(figsize=(12, 8))
    
    # Plot each band separately to avoid connecting discontinuous segments
    for i in range(len(band_breaks)-1):
        start_idx = band_breaks[i]
        end_idx = band_breaks[i+1]
        
        k_segment = k_coord[start_idx:end_idx]
        e_segment = energy[start_idx:end_idx] - fermi_energy
        
        if len(k_segment) > 1:  # Only plot if segment has more than one point
            plt.plot(k_segment, e_segment, 'b-', linewidth=1.2, alpha=0.8)
    
    # Add Fermi level
    plt.axhline(0, color='r', linestyle='--', alpha=0.8, linewidth=2, label='Fermi Level')
    
    # Add high-symmetry point markers based on our k-path
    # Γ-X-W-L-Γ-X path
    if len(k_coord) > 0:
        max_k = np.max(k_coord)
        # Estimate positions based on the 4-segment path
        gamma1 = 0
        x1 = max_k * 0.33  # After first segment
        w = max_k * 0.66   # After second segment  
        l = max_k * 0.83   # After third segment
        gamma2 = max_k * 0.95  # After fourth segment
        
        symmetry_points = [gamma1, x1, w, l, gamma2]
        labels = ['Γ', 'X', 'W', 'L', 'Γ']
        
        for point, label in zip(symmetry_points, labels):
            plt.axvline(point, color='k', linestyle=':', alpha=0.6, linewidth=1)
            plt.text(point, plt.ylim()[1]*0.95, label, ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.xlabel('k-path', fontsize=14)
    plt.ylabel('Energy - E_F (eV)', fontsize=14)
    plt.title('Band Structure - CoFeMnTi Quaternary Heusler (Corrected)', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.ylim(-6, 6)
    plt.xlim(0, max_k if 'max_k' in locals() else None)
    
    plt.tight_layout()
    plt.savefig('CoFeMnTi_bands_corrected.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Corrected band structure plot saved as: CoFeMnTi_bands_corrected.png")

def analyze_band_structure():
    """Analyze the band structure data"""
    fermi_energy = read_dos_fermi('CoFeMnTi.dos')
    
    try:
        data = np.loadtxt('CoFeMnTi_fixed.bands.gnu')
    except:
        data = np.loadtxt('CoFeMnTi.bands.gnu')
    
    energy = data[:, 1] - fermi_energy
    
    # Find bands at Fermi level
    fermi_crossings = np.abs(energy) < 0.1  # Within 0.1 eV of Fermi level
    
    print("\\n=== BAND STRUCTURE ANALYSIS ===")
    print(f"Fermi Energy: {fermi_energy:.3f} eV")
    print(f"Number of k-points: {len(data)}")
    print(f"Energy range: {np.min(energy):.2f} to {np.max(energy):.2f} eV relative to EF")
    print(f"Bands crossing Fermi level: {np.sum(fermi_crossings)} points")
    
    if np.sum(fermi_crossings) > 0:
        print("System appears to be metallic (bands cross Fermi level)")
    else:
        print("System might be semiconducting/insulating")

if __name__ == "__main__":
    print("Creating improved band structure plot for CoFeMnTi")
    print("=" * 55)
    
    plot_bands_improved()
    analyze_band_structure()
    
    print("\\n" + "=" * 55)
    print("Improved band structure analysis completed!")
