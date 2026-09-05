import tikzplot.plots as plt
import numpy as np
from tikzplot import Colorbar

# based on Matplotlib examples

fig, ax = plt.subplots(2,2)

np.random.seed(1)
x = 4 + np.random.normal(0, 1.5, 200)
ax[0,0].ecdf(x)

x = np.random.randn(5000)
y = 1.2 * x + np.random.randn(5000) / 3

_,_,_, im = ax[0,1].hist2d(x, y, bins=(np.arange(-3, 3, 0.1), np.arange(-3, 3, 0.1)), cmin=1)
Colorbar(im)

ax[0,1].set(xlim=(-2, 2), ylim=(-3, 3))

x = [1, 2, 3, 4]
cbar = Colorbar(cmap="Blues")
colors = cbar.colors(np.linspace(0.2, 0.7, len(x)))

ax[1,0].pie(x, colors=colors, radius=0.8, autopct="%1.0f%%", startangle=90, pctdistance=0.6, labeldistance=1.1, rotate_labels=True, labels=["a", "b", "c", "d"])

stats = [
    dict(med=0, q1=-1, q3=1, whislo=-2, whishi=2, mean=0.5, fliers=[-4, -3, 3, 4], label='A'),
    dict(med=0, q1=-2, q3=2, whislo=-3, whishi=3, fliers=[], label='B'),
    dict(med=0, q1=-3, q3=3, whislo=-4, whishi=4, fliers=[], label='C'),
]

#ax[1,1].bxp(stats, positions=[1, 2, 4], widths=0.7, showfliers=True,showmeans=True, boxprops={'facecolor': 'bisque'})

np.random.seed(19680801)
data = np.random.randn(20, 3)

ax[1,1].boxplot(data, tick_labels=['A', 'B', 'C'], boxprops={'facecolor': 'bisque'})


plt.savefig("figure.tex")