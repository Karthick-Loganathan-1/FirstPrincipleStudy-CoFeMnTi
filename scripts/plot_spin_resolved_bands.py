#!/usr/bin/env python3
"""
Spin-resolved band structure plot for magnetic CoFeMnTi
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

def read_bands_data(filename):
    """Read band structure data with column information"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Skip header comments and find data
    data_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            data_lines.append(line)
    
    # Parse data - typically k-point, energy (possibly spin-resolved)
    data = []
    for line in data_lines:
        parts = line.split()
        if len(parts) >= 2:
            data.append([float(x) for x in parts])
    
    return np.array(data)

def plot_spin_resolved_bands():
    """Plot spin-resolved band structure"""
    fermi_energy = read_dos_fermi('CoFeMnTi.dos')
    
    try:
        # Try to read the corrected bands
        data = read_bands_data('CoFeMnTi_fixed.bands.gnu')
        title_suffix = "(Corrected Path)"
    except:
        # Fallback to original bands
        data = read_bands_data('CoFeMnTi.bands.gnu')
        title_suffix = "(Original Path)"
    
    k_coord = data[:, 0]
    
    # For spin-polarized calculations, we might have multiple energy columns
    # Let's assume column 1 is the energy (we'll handle spin resolution later)
    energy = data[:, 1] - fermi_energy
    
    # Detect band segments (where k resets)
    band_breaks = [0]
    for i in range(1, len(k_coord)):
        if k_coord[i] < k_coord[i-1]:
            band_breaks.append(i)
    band_breaks.append(len(k_coord))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left plot: Standard bands
    for i in range(len(band_breaks)-1):
        start_idx = band_breaks[i]
        end_idx = band_breaks[i+1]
        
        k_segment = k_coord[start_idx:end_idx]
        e_segment = energy[start_idx:end_idx]
        
        if len(k_segment) > 1:
            ax1.plot(k_segment, e_segment, 'b-', linewidth=1.2, alpha=0.8)
    
    ax1.axhline(0, color='r', linestyle='--', alpha=0.8, linewidth=2, label='Fermi Level')
    ax1.set_xlabel('k-path', fontsize=12)
    ax1.set_ylabel('Energy - E_F (eV)', fontsize=12)
    ax1.set_title(f'Band Structure {title_suffix}', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-6, 6)
    ax1.legend()
    
    # Add symmetry labels
    if len(k_coord) > 0:
        max_k = np.max(k_coord)
        symmetry_points = [0, max_k*0.33, max_k*0.66, max_k*0.85, max_k]
        labels = ['Γ', 'X', 'L', 'Γ', 'X']
        
        for point, label in zip(symmetry_points, labels):
            ax1.axvline(point, color='k', linestyle=':', alpha=0.5)
            ax1.text(point, ax1.get_ylim()[1]*0.9, label, ha='center', va='bottom', fontweight='bold')
    
    # Right plot: Zoom around Fermi level
    for i in range(len(band_breaks)-1):
        start_idx = band_breaks[i]
        end_idx = band_breaks[i+1]
        
        k_segment = k_coord[start_idx:end_idx]
        e_segment = energy[start_idx:end_idx]
        
        # Only plot bands that cross or are near Fermi level
        if len(k_segment) > 1 and np.any(np.abs(e_segment) < 3):
            ax2.plot(k_segment, e_segment, 'b-', linewidth=1.5, alpha=0.8)
    
    ax2.axhline(0, color='r', linestyle='--', alpha=0.8, linewidth=2, label='Fermi Level')
    ax2.set_xlabel('k-path', fontsize=12)
    ax2.set_ylabel('Energy - E_F (eV)', fontsize=12)
    ax2.set_title('Bands near Fermi Level', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-3, 3)
    ax2.legend()
    
    # Add symmetry labels to zoomed plot
    for point, label in zip(symmetry_points, labels):
        ax2.axvline(point, color='k', linestyle=':', alpha=0.5)
        ax2.text(point, ax2.get_ylim()[1]*0.9, label, ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('CoFeMnTi_bands_detailed.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Detailed band structure plot saved as: CoFeMnTi_bands_detailed.png")

def create_comparison_plot():
    """Create a comparison between original and corrected bands"""
    fermi_energy = read_dos_fermi('CoFeMnTi.dos')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Original bands
    try:
        data_orig = read_bands_data('CoFeMnTi.bands.gnu')
        k_orig = data_orig[:, 0]
        e_orig = data_orig[:, 1] - fermi_energy
        
        # Plot original (with discontinuities)
        ax1.plot(k_orig, e_orig, 'r-', linewidth=0.8, alpha=0.7, label='Original (with discontinuities)')
        ax1.axhline(0, color='k', linestyle='--', alpha=0.8, linewidth=1)
        ax1.set_xlabel('k-path')
        ax1.set_ylabel('Energy - E_F (eV)')
        ax1.set_title('Original Band Structure\\n(with discontinuities)')
        ax1.set_ylim(-6, 6)
        ax1.grid(True, alpha=0.3)
    except:
        ax1.text(0.5, 0.5, 'Original data not found', ha='center', va='center', transform=ax1.transAxes)
    
    # Corrected bands
    try:
        data_fixed = read_bands_data('CoFeMnTi_fixed.bands.gnu')
        k_fixed = data_fixed[:, 0]
        e_fixed = data_fixed[:, 1] - fermi_energy
        
        # Find segments for corrected data
        band_breaks = [0]
        for i in range(1, len(k_fixed)):
            if k_fixed[i] < k_fixed[i-1]:
                band_breaks.append(i)
        band_breaks.append(len(k_fixed))
        
        # Plot corrected bands properly
        for i in range(len(band_breaks)-1):
            start_idx = band_breaks[i]
            end_idx = band_breaks[i+1]
            
            k_segment = k_fixed[start_idx:end_idx]
            e_segment = e_fixed[start_idx:end_idx]
            
            if len(k_segment) > 1:
                ax2.plot(k_segment, e_segment, 'b-', linewidth=1, alpha=0.8)
        
        ax2.axhline(0, color='k', linestyle='--', alpha=0.8, linewidth=1)
        ax2.set_xlabel('k-path')
        ax2.set_ylabel('Energy - E_F (eV)')
        ax2.set_title('Corrected Band Structure\\n(smooth path)')
        ax2.set_ylim(-6, 6)
        ax2.grid(True, alpha=0.3)
        
        # Add symmetry points to corrected plot
        max_k = np.max(k_fixed)
        symmetry_points = [0, max_k*0.33, max_k*0.66, max_k*0.85, max_k]
        labels = ['Γ', 'X', 'L', 'Γ', 'X']
        
        for point, label in zip(symmetry_points, labels):
            ax2.axvline(point, color='k', linestyle=':', alpha=0.5)
            ax2.text(point, ax2.get_ylim()[1]*0.9, label, ha='center', va='bottom', fontweight='bold')
            
    except:
        ax2.text(0.5, 0.5, 'Corrected data not found', ha='center', va='center', transform=ax2.transAxes)
    
    plt.tight_layout()
    plt.savefig('CoFeMnTi_bands_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Band structure comparison plot saved as: CoFeMnTi_bands_comparison.png")

if __name__ == "__main__":
    print("Creating advanced band structure analysis for CoFeMnTi")
    print("=" * 60)
    
    plot_spin_resolved_bands()
    create_comparison_plot()
    
    print("\\n" + "=" * 60)
    print("Advanced band structure analysis completed!")
    print("\\nFiles generated:")
    print("- CoFeMnTi_bands_detailed.png (detailed view)")
    print("- CoFeMnTi_bands_comparison.png (before/after comparison)")
