import tikzplot.plots as plt
<<<<<<< HEAD
#import matplotlib.pyplot as plt
=======
>>>>>>> 0a7fbc5561a9fd93b0d2a38256bf13ec9f07c8d7
import numpy as np

x = np.linspace(1,10,20)
y = x**2

plt.plot(x, 2*y, color="blue")

plt.scatter(x, y/2, color="red")

plt.ylabel(r"$y$")
plt.grid()
plt.xlim(0,10)

<<<<<<< HEAD
plt.errorbar(x, y, 1, color="black")

plt.savefig("tests/figure.tex")
=======
plt.errorbar(x, y, yerr=1, color="black")

plt.savefig("tests/figure.tex")
>>>>>>> 0a7fbc5561a9fd93b0d2a38256bf13ec9f07c8d7
