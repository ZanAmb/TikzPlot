import numpy as np
import tikzplot.plots as plt
from tikzplot import TikzConfig, Colorbar
TikzConfig.modifyParam(MAX_POINTS_PER_ELEMENT=10000)
#TikzConfig.modifyParam(DEFAULT_HEIGHT=10, DEFAULT_WIDTH=5)
import math

gamma = np.vectorize(math.gamma)
N = 31
x = np.linspace(0., 10., N)
lambdas = list(reversed(range(1, 10)))

ax = plt.figure().add_subplot(projection='3d')

cmap = Colorbar(axis=ax, cmap="gist_rainbow", lower=1, upper=10, rel_len=0.5, divisions=9)

facecolors = [cmap.color(l) for l in lambdas]

for i, l in enumerate(lambdas):
    ax.fill_between(x, l, l**x * np.exp(-l) / gamma(x + 1),
                    x, l, 0,
                    color=facecolors[i], alpha=.5)

ax.set(xlim=(0, 10), ylim=(1, 9), zlim=(0, 0.35),
       xlabel='$x$', ylabel=r'$\lambda$', zlabel='probability')

plt.savefig("figure.tex")