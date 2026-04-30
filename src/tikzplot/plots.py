import numpy as np

from .figure import Figure
from .state import main_name, next_show_num
from .config import TikzConfig

_current_figure = None
_current_axes = None

def figure(**kwargs):        
    global _current_figure, _current_axes
    _current_figure = Figure()
    _current_axes = None
    if "figsize" in kwargs:
        _current_figure.set_size_inches(kwargs["figsize"])
    return _current_figure

def _ensure_axes():
    global _current_figure, _current_axes

    if _current_figure is None:
        from .figure import Figure
        _current_figure = Figure()

    if _current_axes is None:
        _current_axes = _current_figure.add_subplot(1, 1, 1)

def xlabel(label):
    _ensure_axes()
    _current_axes.set_xlabel(label)

def ylabel(label):
    _ensure_axes()
    _current_axes.set_ylabel(label)

def title(text):
    _ensure_axes()
    _current_axes.set_title(text)

def grid(*args, **kwargs):
        _ensure_axes()
        _current_axes.grid(*args, **kwargs)

def minorticks_num(num):
    _ensure_axes()
    _current_axes.set_minorticks_num(num)

def xlim(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_xlim(*args, **kwargs)

def ylim(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_ylim(*args, **kwargs)

def legend(*args, **kwargs):
    _ensure_axes()
    _current_axes.legend(*args, **kwargs)

def subplot(nrows, ncols, index, sharex=None, sharey=None, projection=None, polar=False):
    global _current_axes

    if _current_figure is None:
        figure()

    _current_axes = _current_figure.add_subplot(nrows, ncols, index, sharex, sharey, projection, polar)
    return _current_axes

def subplots(nrows=1, ncols=1, sharex=None, sharey=None, subplot_kw=None, **kwargs):

    global _current_figure, _current_axes

    _current_figure = Figure()
    axes = _current_figure._add_subplots(nrows, ncols, sharex, sharey, subplot_kw)

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

    if "figsize" in kwargs:
        _current_figure.set_size_inches(kwargs["figsize"])
    return _current_figure, grid

def plot(*args, **kwargs):
    _ensure_axes()
    _current_axes.plot(*args, **kwargs)

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

def fill_between(*args, **kwargs):
    _ensure_axes()
    _current_axes.fill_between(*args, **kwargs)

def text(*args, **kwargs):
    _ensure_axes()
    _current_axes.text(*args, **kwargs)

def hlines(*args, **kwargs):
    _ensure_axes()
    _current_axes.hlines(*args, **kwargs)

def vlines(*args, **kwargs):
    _ensure_axes()
    _current_axes.vlines(*args, **kwargs)

def imshow(*args, **kwargs):
    _ensure_axes()
    return _current_axes.imshow(*args, **kwargs)

def xticks(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_xticks(*args, **kwargs)

def yticks(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_yticks(*args, **kwargs)

def xscale(*args, **kwargs):
    _ensure_axes()
    _current_axes.set_xscale(*args, **kwargs)

def yscale( *args, **kwargs):
    _ensure_axes()
    _current_axes.set_yscale(*args, **kwargs)

def savefig(filename):
    if not(filename.endswith(".tex") or filename.endswith(".tikz")):
        filename += ".tex"
    _current_figure._save(filename)

def show():
    _current_figure._save(f"{str(main_name()[1]).removesuffix('.py')}_{TikzConfig.SHOW_SAVENAME}{next_show_num()}.tex")
    clf()

def clf():
    _current_figure.clear()

def gca():
    _ensure_axes()
    return _current_axes

def tight_layout():
    pass