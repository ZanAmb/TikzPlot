# TikzPlot
A clean version of PltToTikz, this time as Python package. Easy to use: only replace import matplotlib.pyplot with this library.

Please let me know if you find any bugs or unexpected behaviour. Examples may be found in repository under `tests/` directory.

<p align="center">
  <img src="https://raw.githubusercontent.com/ZanAmb/TikzPlot/main/tests/demo.png" width="60%">
</p>

# Installation
NEW: PyPI: `pip install tikzplot42`.
Alternativley, download this package and install using: `pip install [path]`, where [path] is the path to the directory, containing `pyproject.toml`.

## Python usage
Instead of using `import matplotlib.pyplot (as plt)`, use `import tikzplot.plots (as plt)`.

## LaTeX requirements
- `\usepackage{tikz}`,
- `\usepackage{pgfplots}`,
- `\pgfplotsset{compat=1.18}` (may be lower, but compilation is not guaranteed),
- `\usepgfplotslibrary{fillbetween}` (if you use fill-between plots),
- `\usepgfplotslibrary{groupplots}` (recommended for best results, enabled by default, may be avoided by setting TikzConfig USE_GROUPPLOTS=False),
- `\usepackage{xcolor}` (recommended for best colors, works without but needs change of TikzConfig USE_XCOLOR=False),
- `\usepgfplotslibrary{polar}` required for polar axis.

Export using `plt.savefig("example_graph.tex")` (recommended) or `plt.show()`.
Then use the generated file as `\input{example_graph.tex}`.

## Currently implemented:
Some basic plot commands are already implemented with commonly used arguments:
#### Plotting
- `plot()`,
- `scatter()`,
- `loglog()`,
- `semilogx()/semilogy()`,
- `errorbar()`,
- `stem()`,
- `fill-between()`,
- `hlines()/vlines()`,
- `historgam()`,
- `step()`,
- `imshow()`,
- `text()`.

#### Figures
- `plt.figure()` (currently only to give you figure object or to set `figsize`),
- `plt.subplot()`, `plt.subplots()` (with `sharex/sharey` fully implemented, projection `polar` and `3d` with basic support),
- `set_size_inches()`.

#### Styles
If axes and plot have different name for command with same effect, both are implemented (e.g. `plt.xlim()` and `ax.set_xlim()`).
- `grid()`,
- `xlabel()/ylabel()`,
- `xlim(), ylim()`,
- `xscale("log")/yscale("log")`,
- `xticks()/yticks()`,
- `ax.set_xticklabels()/ax.set_yticklabels()`,
- `legend()` (basic position control),
- `ax.twinx()`,
- `ax.set()`.

#### Supported common **kwargs
- `color/c` (all matplotlib formats, except color schemes which are not yet implemented),
- `linestyle/ls`,
- `linewidth/ls`,
- `fmt`,
- `marker`,
- `marksize/ms`,
- `alpha`,
- `label`.

#### Colorbars
Colorbars and colormaps are implemented a bit differently than in matplotlib (simplified):
- if you use `imshow()`, you may use its return in `Colorbar()` (which you have to import as `from tikzplot import Colorbar`),
- you may use `Colorbar(axis, cmap, lower, upper, ...)` for manual colorbar. Additional kwargs may also be used by `imshow()` return.

#### TikzConfig
For plot configurations (default sizes, paddings, etc.), use `from tikzplot import TikzConfig`:
- `modifyParam(PARAM=value)` (for runtime session setting),
- `setPermanent(PARAM=value)` (for user defined default value).
Currently supported parameters are listed with their default values in `src/tikzplot/config.py`.

## More features coming soon...
- basic color schemes,
- improved 3D plots (currently only basic support: plot, errorbar, fill_between, scatter, plot_wireframe, plot_surface),
- ... 
