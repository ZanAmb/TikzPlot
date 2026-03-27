import numpy as np
import tikzplot.plots as plt

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make the data
x = np.arange(-5, 5, 0.5)
y = np.arange(-5, 5, 0.5)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

ax.plot_wireframe(X, Y, Z, color='C0')

ax.set(xlim=(-5, 5), ylim=(-5, 5), zlim=(-1, 0.5))

plt.savefig("figure.tex")