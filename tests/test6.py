#import matplotlib.pyplot as plt
import tikzplot.plots as plt
import numpy as np

delta = 0.025
x = y = np.arange(-3.0, 3.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2

fig, ax = plt.subplots()
im = ax.imshow(Z, interpolation='bilinear', cmap="viridis", origin='lower', extent=[-3, 3, -3, 3], vmax=abs(Z).max(), vmin=-abs(Z).max())
ax.grid()
ax.plot([-2,2],[2,-2], color="white")
#plt.show()
plt.savefig("figure.tex")