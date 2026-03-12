import numpy as np

from .figure import Figure

_current_figure = None
_current_axes = None

def figure():
    global _current_figure, _current_axes
    _current_figure = Figure()
    _current_axes = None
    return _current_figure

def _ensure_axes():
    global _current_figure, _current_axes

    if _current_figure is None:
        from .figure import Figure
        _current_figure = Figure()

    if _current_axes is None:
        _current_axes = _current_figure._add_subplot(1, 1, 1)

def xlabel(label):
    _ensure_axes()
    _current_axes.set_xlabel(label)

def ylabel(label):
    _ensure_axes()
    _current_axes.set_ylabel(label)

def title(text):
    _ensure_axes()
    _current_axes.set_title(text)

def grid(visible=True, which="major"):
        _ensure_axes()
        if not visible:
            _current_axes.axis_options["grid"] = "none"
            return

        if which == "major":
            _current_axes.axis_options["grid"] = "major"

        elif which == "minor":
            _current_axes.axis_options["minor grid style"] = "{dotted}"
            _current_axes.axis_options["grid"] = "both"

        elif which == "both":
            _current_axes.axis_options["grid"] = "both"

def xlim(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_xlim(*args, **kwargs)

def ylim(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_ylim(*args, **kwargs)

def legend(*args, **kwargs):
    _ensure_axes()
    _current_axes.legend(*args, **kwargs)

def subplot(nrows, ncols, index, sharex=None, sharey=None):
    global _current_axes

    if _current_figure is None:
        figure()

    _current_axes = _current_figure._add_subplot(nrows, ncols, index, sharex, sharey)
    return _current_axes

def subplots(nrows=1, ncols=1, sharex=None, sharey=None,**kwargs):

    global _current_figure, _current_axes

    _current_figure = Figure()
    axes = _current_figure._add_subplots(nrows, ncols, sharex, sharey)

    if nrows * ncols == 1:
        _current_axes = axes[0]
        return _current_figure, axes[0]

    grid = []
    k = 0
    for r in range(nrows):
        row = []
        for c in range(ncols):
            row.append(axes[k])
            k += 1
        grid.append(row)

    _current_axes = axes[0]
    grid = np.asarray(grid)
    if grid.shape[0] == 1:
        grid = grid[0]
    elif grid.shape[1] == 1:
        grid = grid[:,0]
    return _current_figure, grid

def plot(*args, **kwargs):
    _ensure_axes()
    if len(args) == 0:
        pass
    elif len(args) == 1:
        y = args[0]
        _current_axes._plot(range(len(y)), y, **kwargs)
    elif len(args) == 2:
        x, y = args
        _current_axes._plot(x, y, **kwargs)
    else:
        x,y,fmt = args[:3]
        _current_axes._plot(x,y,fmt=fmt, **kwargs)

def scatter(x, y, *args, **kwargs):
    _ensure_axes()
    _current_axes.scatter(x, y, *args, **kwargs)


def loglog(x, y, *args, **kwargs):
    _ensure_axes()
    _current_axes.loglog(x, y, *args, **kwargs)

def semilogx(x, y, *args, **kwargs):
    _ensure_axes()
    _current_axes.semilogx(x, y, *args, **kwargs)

def semilogy(x, y, *args, **kwargs):
    _ensure_axes()
    _current_axes.semilogy(x, y, *args, **kwargs)

def errorbar(x, y, *args, **kwargs):
    _ensure_axes()
    _current_axes.errorbar(x, y, *args, **kwargs)

def stem(*args, **kwargs):
    _ensure_axes()
    _current_axes.stem(*args, **kwargs)

def xticks(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_xticks(*args, **kwargs)

def yticks(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_yticks(*args, **kwargs)

def savefig(filename):
    if not(filename.endswith(".tex") or filename.endswith(".tikz")):
        filename += ".tex"
    _current_figure._save(filename)

def show(): ### DODELAJ!
    _current_figure._save(f"plot.tex")

def clf():
    _current_figure._clear()
