import tikzplot.plots as plt
import numpy as np

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

l = ax0.plot([-2,0,2], [0.2,0.3,0.35])
x = np.random.randn(1000, 3)
colors = ['red', 'tan', 'lime']
ax0.hist(x, 10, density=True, histtype='bar', color=colors, label=colors)
ax0.plot([-2,0,2], [0.45,0.2,0.25], label="line 2")
ax0.legend([l], ["line 1"])

ax1.plot([-2,0,2], [0.2,0.3,0.35], label="line 1")
ax1.legend()

species = [-1,0,1]
weight_counts = {
    "Below": np.array([70, 31, 58]),
    "Above": np.array([82, 37, 66]),
}
width = 0.5

bottom = np.zeros(3)
ax2.plot([-2,0,2], [50, 100, 80], label="line 1")
for boolean, weight_count in weight_counts.items():
    ax2.bar(species, weight_count, width, label=boolean, bottom=bottom, align='center')
    bottom += weight_count
ax2.plot([-2,0,2], [80, 100, 90], label="line 2")
ax2.legend()

categories = ['A', 'B', 'C', 'D']
means = [23, 35, 18, 28]
errors = [2.5, 4.0, 1.8, 3.2]

bars = ax3.barh(categories, means, xerr=errors, capsize=5, color='#3498db', edgecolor='#2C3E50', linewidth=1.2, alpha=0.85, height=0.4, ecolor='#2C3E50')

plt.savefig("figure.tex")