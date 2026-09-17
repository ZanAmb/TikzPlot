import tikzplot.plots as plt
import numpy as np
from tikzplot import TikzConfig
TikzConfig.modifyParam(MAX_POINTS_PER_ELEMENT=5000)

X, Y = np.meshgrid(np.linspace(-3, 3, 256), np.linspace(-3, 3, 256))
Z = (1 - X/2 + X**5 + Y**3) * np.exp(-X**2 - Y**2)
V = np.diff(Z[1:, :], axis=1)
U = -np.diff(Z[:, 1:], axis=0)

fig, ax = plt.subplots()

cb = ax.streamplot(X[1:, 1:], Y[1:, 1:], U, V, density=2, broken_streamlines=True, cmap="jet")
plt.colorbar(cb)
plt.savefig("figure.tex")