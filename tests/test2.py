import tikzplot.plots as plt
import numpy as np

x = np.linspace(1,10,20)
y = x**2

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,sharex="row",sharey="row")

ax1.set_xlim(left=2)
ax1.axvline(3, 0.2, 0.5, c="r")
ax1.axhline(50,0.1,0.9, ls="--")
ax1.plot(x,x)
ax2.set_yscale("log")
ax2.step(x,y,".", ms=1,where="mid")
ax3.plot(y,y)
ax3.grid()
ax3.axvspan(3,50,0.1,0.8,c="b",alpha=0.3)
ax4.plot(y,x)
ax1.set_xlabel(r"$x$")
ax1.set_ylabel(r"$y$")
ax2.grid(which="both")

plt.savefig("figure.tex")