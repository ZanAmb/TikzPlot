import numpy as np
import tikzplot.plots as plt
#import matplotlib.pyplot as plt

xs = np.linspace(0,5,20)
plt.plot(xs, xs, "b--", lw=2, label="line")
plt.fill_between(xs, np.sin(xs), xs, hatch=".", hatch_color="white", label="fill")
plt.legend()
plt.savefig("figure.tex")