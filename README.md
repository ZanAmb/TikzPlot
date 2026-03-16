# TikzPlot
A clean version of PltToTikz, this time as Python package. Easy to use: only replace import matplotlib.pyplot with this library.

Please let me know if you find any buggs or unexpected behaviour. When the project will be ready, I might publish it on PyPI.

## Python usage
Instead of using `import matplotlib.pyplot (as plt)`, use `import tikzplot.plots (as plt)`.

## LaTeX requirements
- `\usepackage{tikz}`
- `\usepackage{pgfplots}`
- `\pgfplotsset{compat=1.18}`
- `\usepgfplotslibrary{fillbetween}` (if you use fill-between plots).

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
- `hisotrgam()`.

#### Figures
- `plt.figure()` (currently only to give you figure object or to set `figsize`),
- `plt.subplot()`, `plt.subplots()` (with `sharex/sharey` fully implemented),
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
- `ax.twinx()`.

#### Supported common **kwargs
- `color/c` (all matplotlib formats, except color schemes which are not yet implemented),
- `linestyle/ls`,
- `linewidth/ls`,
- `fmt`,
- `marker`,
- `marksize/ms`,
- `alpha`,
- `label`.

#### TikzConfig
For plot configurations (default sizes, paddings, etc.), use `from tikzplot import TikzConfig`:
- `modifyParam(PARAM=value)` (for runtime session setting),
- `setPermanent(PARAM=value)` (for user defined default value).
Currently supported parameters are listed with their default values in `src/tikzplot/config.py`.

## More features comming soon...
- automatic removal of datapoints to prevent LaTeX memory overflow,
- automatic color setting for plots with no specified color + basic color schemes,
- 3D plots,
- ... 