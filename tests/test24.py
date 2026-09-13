import numpy as np
import tikzplot.plots as plt

delta = 0.25
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2

CS = plt.contour(X, Y, Z, colors=["blue", "violet", "red", "yellow", "green"], labels=True, ls="--")
plt.colorbar(CS)

plt.savefig("figure.tex")