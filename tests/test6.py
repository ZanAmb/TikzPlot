#import matplotlib.pyplot as plt
import tikzplot.plots as plt
import numpy as np
from tikzplot import Colorbar
from tikzplot import TikzConfig

delta = 0.025
x = y = np.arange(-3.0, 3.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2

fig, ax = plt.subplots()
im = ax.imshow(Z, interpolation='bilinear', cmap="Pastel1", origin='lower', extent=[1, 3, 1, 3], vmax=abs(Z).max(), vmin=-abs(Z).max())
ax.grid()
cbar = Colorbar(im, label="$x$", rel_len=0.9, horizontal=True, tick_labels=[])
#plt.show()

plt.savefig("figure.tex")