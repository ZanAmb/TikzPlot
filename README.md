# TikzPlot
A clean version of PltToTikz, this time as Python package. Easy to use: only replace import matplotlib.pyplot with this library.

Please report any bugs or unexpected behaviour in Issues. Examples may be found in repository under `tests/` directory.

<p align="center">
  <img src="https://raw.githubusercontent.com/ZanAmb/TikzPlot/main/tests/demo.png" width="60%">
</p>

## Why use pgfplots instead of matplotlib?
- Tikz/pgfplots is a LaTeX package, so it is easy to integrate into your LaTeX document, and the fonts will match your document, rescaling will not affect font sizes.
- Tikz/pgfplots graph is easy to edit, especially if only minor style changes are needed, while matplotlib requires re-running the code to generate a new graph.
- Full math mode is supported, so you can use LaTeX math in your labels, legends, etc.

## Why use this package instead of other available?
- It is easy to use, with code being very similar to matplotlib and only minor changes are needed to switch from matplotlib to this package.
- It relies on frontend commands, which is less likley to change in matplotlib, so new updates do not break it.
- It generates clean and readable Tikz code, which is easy to edit and understand. Code is also efficient and does not contain unnecessary commands, which is important escpecially for large graphs.
- If you use LLMs to generate pgfplots code, you will often get code that is not compilable, since for more complex requirements, LLMs make up commands that do not exist. This package covers many use cases and generates compilable code.


# Installation
PyPI: `pip install tikzplot42`.
Alternativley, download this package and install using: `pip install [path]`, where [path] is the path to the directory, containing `pyproject.toml`.

## Python usage
Instead of using `import matplotlib.pyplot (as plt)`, use `import tikzplot.plots (as plt)`.

## LaTeX requirements
All required packages are automatically detected and can be printed at save using kwarg `print_requirements=True` (for standalone files, preambule is automatically added).
- `\usepackage{tikz}`,
- `\usepackage{pgfplots}`,
- `\pgfplotsset{compat=1.18}` (may be lower, but compilation is not guaranteed),
- `\usepgfplotslibrary{fillbetween}` (if you use fill-between plots),
- `\usepgfplotslibrary{groupplots}` (recommended for best results, enabled by default, may be avoided by setting TikzConfig USE_GROUPPLOTS=False),
- `\usepackage{xcolor}` (recommended for best colors, works without but needs change of TikzConfig USE_XCOLOR=False),
- `\usepgfplotslibrary{polar}` required for polar axis,
- `\usetikzlibrary{patterns.meta}` for hatch patterns (available for fill_between, hist and axvspan/axhspan).

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
- `fill_between()`,
- `hlines()/vlines()`,
- `hist()`,
- `bar()/barh()`,
- `bar_label()`,
- `stackplot()`,
- `step()`,
- `imshow()`,
- `text()`,
- `magnify()` (used to magnify part of a plot, but Tikz cannot handle `fill_between` if this one is used, which is a long known issue),
- `axvline()/axhline()`,
- `axvspan()/axhspan()` (background span).

#### Figures
- `plt.figure()` (currently only to give you figure object or to set `figsize`),
- `plt.subplot()`, `plt.subplots()` (with `sharex/sharey` fully implemented, projection `polar` and `3d` with basic support),
- `set_size_inches()`,
- `delaxes()`.

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
- `ax.set()`,
- `ax.tick_params()`,

There is a limited support for built-in styles (e.g. `plt.style.use("default")`), you may also define your own style using `plt.style.set_profile()`. Currently supported features are: color cycle (hex colors sequence), line width (in pt), grid (with matplotlib kwargs), background (latex style key=value), additional settings (raw latex code for optional arguments to axis: key=value).

#### Supported common **kwargs
- `color/c`,
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
- you may use `Colorbar(axis, cmap, lower, upper, ...)` for manual colorbar. Additional kwargs may also be used by `imshow()` return,
- note that only one colorbar/colormap per axis is allowed (also if you use `scatter` with colormap/colorbar).

#### TikzConfig
For plot configurations (default sizes, paddings, etc.), use `from tikzplot import TikzConfig`:
- `modifyParam(PARAM=value)` (for runtime session setting),
- `setPermanent(PARAM=value)` (for user defined default value).
Currently supported parameters are listed with their default values in `src/tikzplot/config.py`.

## More features coming soon...
- additional arguments support for implemented commands,
- improved 3D plots (currently only basic support: plot, errorbar, fill_between, scatter, plot_wireframe, plot_surface),
- ... 
