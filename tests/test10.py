# Example from official matplotlib documentation

import tikzplot.plots as plt
import numpy as np
#from tikzplot import Colorbar
#from tikzplot import TikzConfig

#TikzConfig.modifyParam(USE_GROUPPLOTS=False)

# Fixing random state for reproducibility
#np.random.seed(19680801)

# Compute areas and colors
N = 150
r = 2 * np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)
area = 200 * r**2
colors = theta

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(projection='polar')
#cbar = Colorbar(cmap='hsv', lower=0, upper=max(theta))
c = ax.scatter(theta, r, c="blue", s=100, alpha=0.75)
plt.savefig("figure.tex")