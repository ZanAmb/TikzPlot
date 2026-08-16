import tikzplot.plots as plt
import numpy as np

np.random.seed(19680801)

n_bins = 10
x = np.random.randn(1000, 3)

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

colors = ['red', 'tan', 'lime']
ax0.hist(x, n_bins, density=True, histtype='bar', color=colors, label=colors)
ax0.legend(prop={'size': 10})
ax0.set_title('bars with legend')

ax1.hist(x, n_bins, density=True, histtype='bar', stacked=True, hatch=['+', '**', '..'], hatch_color='black', hatch_linewidth=0.7, label=["1", "2", "3"])
ax1.set_title('stacked bar')
ax1.legend()

ax2.hist(x, n_bins, histtype='step', stacked=True, fill=False, label=["1", "2", "3"])
ax2.set_title('stack step (unfilled)')
ax2.legend()

x_multi = [np.random.randn(n) for n in [10000, 5000, 2000]]
ax3.hist(x_multi, n_bins, histtype='bar')
ax3.set_title('different sample sizes')

fig.tight_layout()
plt.savefig("figure.tex")