import tikzplot.plots as plt
import numpy as np

# Sample data
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

fig = plt.figure(figsize=(8, 8))

# 1. Normal (Rectilinear) Projection
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(x, y, color="tab:blue")
ax1.set_title("Normal Projection")
ax1.grid(True)

# 2. 3D Projection
ax2 = fig.add_subplot(2, 2, 2, projection="3d")
z = np.cos(x)
ax2.plot(x, y, z, color="tab:orange")
ax2.set_title("3D Projection")

# 3. Polar Projection
ax3 = fig.add_subplot(2, 2, 3, projection="polar")
ax3.plot(x, y, color="tab:green")
ax3.set_title("Polar Projection")

# 4. Smith Chart Projection (requires your custom package imported beforehand)
ax4 = fig.add_subplot(2, 2, 4, projection="smith")
# Dummy impedance data (S-parameters / reflection coefficient)
z_smith = 0.5 + 0.5j + 0.4 * np.exp(1j * x)
ax4.plot(z_smith.real, z_smith.imag, color="tab:red")
ax4.set_title("Smith Projection")

plt.savefig("figure.tex")