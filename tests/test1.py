import tikzplot.plots as plt
import numpy as np

x = np.linspace(1,10,20)
y = x**2

plt.plot(x, 2*y, color="blue")

plt.scatter(x, y/2, color="red")

plt.ylabel(r"$y$")
plt.grid()
plt.xlim(0,10)

plt.errorbar(x, y, yerr=1, color="black")

plt.savefig("tests/figure.tex")
