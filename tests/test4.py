import numpy as np
import tikzplot.plots as plt
#import matplotlib.pyplot as plt

xs = np.linspace(0,5,20)
plt.plot(xs, xs, "b--", lw=2)
plt.fill_between(xs, np.sin(xs), xs)
plt.savefig("figure.tex")