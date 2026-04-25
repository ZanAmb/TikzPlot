import tikzplot.plots as plt
import numpy as np
from tikzplot import TikzConfig

TikzConfig.modifyParam(SCHOOL_AXIS=True, STANDALONE=True)

x = np.linspace(1,10,20)
y = x**2

plt.plot(x, 2*y, color="blue")

plt.scatter(x, y/2, color="red")

plt.ylabel(r"$y$")
plt.grid(which="minor", linestyle=":")
plt.grid(which="major", color="teal", alpha=0.5)
plt.minorticks_num(2)
plt.xlim(0,10)

plt.errorbar(x, y, 1, color="black")

plt.savefig("figure1.tex")
