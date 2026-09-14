import numpy as np
import tikzplot.plots as plt

delta = 0.1
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2
fig, axs = plt.subplots(1, 2, figsize=(8, 4))
GS = axs[0].imshow(Z, cmap="gray_r", origin="lower", extent=[-3, 3, -2, 2])
fig.colorbar(GS, ax=axs[0], label="$H$")

CS = axs[0].contour(X, Y, Z, colors=["blue", "violet", "red", "yellow", "green"], labels=True, ls="--")
fig.colorbar(CS, ax=axs[0], location="bottom", label="$Z$")
axs[0].set_xlim(-3, 3)
axs[0].set_ylim(-2, 2)

#CF = axs[1].contourf(X, Y, Z, levels=10, cmap="viridis")
#axs[1].grid()
CF = axs[1].matshow(np.diag(range(16)), labels=True, cmap="plasma", label_size=10, label_color="C0", origin="lower")
fig.colorbar(CF, ax=axs[1], label="$Z$", orientation="horizontal")
plt.tight_layout()
plt.savefig("figure.tex")