import numpy as np
import tikzplot.plots as plt
#import matplotlib.pyplot as plt

# From official matplotlib documentation
rng = np.random.default_rng(19680801)

N_points = 100000
n_bins = 20

# Generate two normal distributions
dist1 = rng.standard_normal(N_points)
dist2 = 0.4 * rng.standard_normal(N_points) + 5

fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

# We can set the number of bins with the *bins* keyword argument.
axs[0].hist(dist1, bins=n_bins, color="b")
axs[1].hist(dist2, bins=n_bins, color="r", rwidth=0.5, cumulative=True)

plt.show()

#plt.show()
plt.savefig("figure.tex")