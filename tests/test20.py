import tikzplot.plots as plt
import numpy as np

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(7, 4))

# Fixing random state for reproducibility
np.random.seed(19680801)


# generate some random test data
all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

# plot violin plot
axs[0].violinplot(all_data, linecolor="red", facecolor="blue",
                  showmeans=False,
                  showmedians=True, quantiles=[[0.1, 0.9], [0,0.2,0.3,0.5,1], [], None])
axs[0].set_title('Violin plot')

# plot box plot
axs[1].boxplot(all_data)
axs[1].set_title('Box plot')

for ax in axs:
    ax.grid(True)
    ax.set_xticks([y + 1 for y in range(len(all_data))],
                  labels=['x1', 'x2', 'x3', 'x4'])
    ax.set_xlabel('Four separate samples')
    ax.set_ylabel('Observed values')

plt.savefig("figure.tex")