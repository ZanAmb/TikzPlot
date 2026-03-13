import tikzplot.plots as plt
import numpy as np

x = np.linspace(1,10,20)
y = x**2

<<<<<<< HEAD
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,sharex="row",sharey="row")

ax1.set_xlim(left=2)
ax1.plot(x,x)
ax2.set_yscale("log")
=======
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

ax1.plot(x,x)
>>>>>>> 0a7fbc5561a9fd93b0d2a38256bf13ec9f07c8d7
ax2.plot(x,y)
ax3.plot(y,y)
ax4.plot(y,x)
ax1.set_xlabel(r"$x$")
ax1.set_ylabel(r"$y$")
ax2.grid()

<<<<<<< HEAD
plt.savefig("tests/figure.tex")
=======
plt.savefig("tests/figure.tex")
>>>>>>> 0a7fbc5561a9fd93b0d2a38256bf13ec9f07c8d7
