"""
xrd_simulator.py
Simple XRD stick pattern simulator for cubic crystals (ZnS example).
Usage: python xrd_simulator.py
Produces: a plot and saves `xrd_sim.png`
"""
import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
a = 5.41   # Lattice parameter for ZnS cubic (Å)
wavelength = 1.5406  # Cu Kα (Å)
hkl_list = [(1,1,1), (2,2,0), (3,1,1), (2,2,2), (4,0,0)]  # Planes to simulate

# Atomic scattering factors (approx, constant for simplicity)
f_Zn = 30
f_S  = 16

# Atomic positions (fractional coordinates)
Zn_positions = [(0,0,0), (0.5,0.5,0), (0.5,0,0.5), (0,0.5,0.5)]
S_positions  = [(0.25,0.25,0.25), (0.75,0.75,0.25), (0.75,0.25,0.75), (0.25,0.75,0.75)]

two_theta = []
intensities = []

for h,k,l in hkl_list:
    # --- Bragg angle ---
    d_hkl = a / np.sqrt(h**2 + k**2 + l**2)
    theta = np.arcsin(wavelength / (2*d_hkl))
    tth = 2*theta*180/np.pi
    two_theta.append(tth)
    
    # --- Structure factor ---
    F_hkl = 0
    # Contribution from Zn
    for x,y,z in Zn_positions:
        F_hkl += f_Zn * np.exp(2j*np.pi*(h*x + k*y + l*z))
    # Contribution from S
    for x,y,z in S_positions:
        F_hkl += f_S * np.exp(2j*np.pi*(h*x + k*y + l*z))
    
    I_hkl = abs(F_hkl)**2
    intensities.append(I_hkl)

# Normalize intensities
intensities = np.array(intensities)
if intensities.max() > 0:
    intensities = intensities / intensities.max() * 100

# --- Plot ---
plt.figure(figsize=(8,4))
for t,I,(h,k,l) in zip(two_theta, intensities, hkl_list):
    if I > 1:  # cutoff for weak peaks
        plt.vlines(t, 0, I, colors='blue', linewidth=2)
        plt.text(t, I+5, f"({h}{k}{l})", rotation=90, ha='center')

plt.xlabel("2θ (degrees)")
plt.ylabel("Intensity (normalized)")
plt.title("Simulated XRD Pattern of Cubic ZnS")
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("xrd_sim.png", dpi=200)
plt.show()
