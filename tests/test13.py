import tikzplot.plots as plt
import numpy as np

b = True

if b:
    np.random.seed(19680801)

    n_bins = 10
    x = np.random.randn(1000, 3)

    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

    colors = ['red', 'tan', 'lime']
    ax0.hist(x, n_bins, density=True, histtype='bar', color=colors, label=colors, align="mid")
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

else:
    np.random.seed(19680801)

    mu_x = 200
    sigma_x = 25
    x = np.random.normal(mu_x, sigma_x, size=100)

    mu_w = 200
    sigma_w = 10
    w = np.random.normal(mu_w, sigma_w, size=100)

    fig, axs = plt.subplots(nrows=2, ncols=2)

    axs[0, 0].hist(x, 20, density=True, histtype='stepfilled', facecolor='g',
                   alpha=0.75)
    axs[0, 0].set_title('stepfilled')

    axs[0, 1].hist(x, 20, density=True, histtype='step', facecolor='g',
                   alpha=0.75)
    axs[0, 1].set_title('step')

    axs[1, 0].hist(x, density=True, histtype='barstacked', rwidth=0.8)
    axs[1, 0].hist(w, density=True, histtype='barstacked', rwidth=0.8)
    axs[1, 0].set_title('barstacked')

    # Create a histogram by providing the bin edges (unequally spaced).
    bins = [100, 150, 180, 195, 205, 220, 250, 300]
    axs[1, 1].hist(x, bins, density=True, histtype='bar', rwidth=0.8, align='right')
    axs[1, 1].set_title('bar, unequal bins')

fig.tight_layout()
plt.savefig("figure.tex")