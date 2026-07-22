import numpy as np

from tikzplot.styles import Styles

from .figure import Figure
from .state import main_name, next_show_num
from .config import TikzConfig

from .axes3d import Axes3

_current_figure = None
_current_axes = None

style = Styles()

def figure(**kwargs):        
    global _current_figure, _current_axes
    _current_figure = Figure(style)
    _current_axes = None
    if "figsize" in kwargs:
        _current_figure.set_size_inches(kwargs["figsize"])
    return _current_figure

def _ensure_axes():
    global _current_figure, _current_axes

    if _current_figure is None:
        _current_figure = Figure(style)

    if _current_axes is None:
        _current_axes = subplot(1, 1, 1)


def xlabel(label):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_xlabel(label)

def ylabel(label):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_ylabel(label)

def title(text):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_title(text)

def grid(*args, **kwargs):
        _ensure_axes()
        assert _current_axes
        _current_axes.grid(*args, **kwargs)

def minorticks_num(num):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("minorticks_num is not supported for 3D axes.")
    _current_axes.set_minorticks_num(num)

def xlim(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_xlim(*args, **kwargs)

def ylim(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_ylim(*args, **kwargs)

def legend(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.legend(*args, **kwargs)

def subplot(nrows, ncols, index, sharex=None, sharey=None, projection=None, polar=False):
    global _current_axes

    if _current_figure is None:
        figure()
    assert _current_figure
    _current_axes = _current_figure.add_subplot(nrows, ncols, index, sharex, sharey, projection, polar)
    return _current_axes

def subplots(nrows=1, ncols=1, sharex=None, sharey=None, subplot_kw=None, **kwargs):

    global _current_figure, _current_axes

    _current_figure = Figure(style)
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
    assert _current_axes
    _current_axes.plot(*args, **kwargs)

def scatter(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.scatter(*args, **kwargs)

def loglog(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("loglog is not supported for 3D axes.")
    _current_axes.loglog(*args, **kwargs)

def semilogx(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("semilogx is not supported for 3D axes.")
    _current_axes.semilogx(*args, **kwargs)

def semilogy(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("semilogy is not supported for 3D axes.")
    _current_axes.semilogy(*args, **kwargs)

def errorbar(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("errorbar is not supported for 3D axes.")
    _current_axes.errorbar(*args, **kwargs)

def stem(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("stem is not supported for 3D axes.")
    _current_axes.stem(*args, **kwargs)

def fill_between(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.fill_between(*args, **kwargs)

def text(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.text(*args, **kwargs)

def hlines(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("hlines is not supported for 3D axes.")
    _current_axes.hlines(*args, **kwargs)

def vlines(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("vlines is not supported for 3D axes.")
    _current_axes.vlines(*args, **kwargs)

def imshow(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("imshow is not supported for 3D axes.")
    return _current_axes.imshow(*args, **kwargs)

def hist(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("hist is not supported for 3D axes.")
    return _current_axes.hist(*args, **kwargs)

def step(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("step is not supported for 3D axes.")
    return _current_axes.step(*args, **kwargs)

def axvline(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("axvline is not supported for 3D axes.")
    return _current_axes.axvline(*args, **kwargs)

def axhline(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("axhline is not supported for 3D axes.")
    return _current_axes.axhline(*args, **kwargs)

def axvspan(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("axvspan is not supported for 3D axes.")
    return _current_axes.axvspan(*args, **kwargs)

def axhspan(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("axhspan is not supported for 3D axes.")
    return _current_axes.axhspan(*args, **kwargs)

def magnify(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("magnify is not supported for 3D axes.")
    return _current_axes.magnify(*args, **kwargs)

def xticks(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_xticks(*args, **kwargs)

def yticks(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_yticks(*args, **kwargs)

def xscale(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_xscale(*args, **kwargs)

def yscale( *args, **kwargs):
    _ensure_axes()
    assert _current_axes
    _current_axes.set_yscale(*args, **kwargs)

def savefig(filename):
    if not(filename.endswith(".tex") or filename.endswith(".tikz")):
        filename += ".tex"
    assert _current_figure
    _current_figure._save(filename)

def show():
    assert _current_figure
    _current_figure._save(f"{str(main_name()[1]).removesuffix('.py')}_{TikzConfig.SHOW_SAVENAME}{next_show_num()}.tex")
    clf()

def clf():
    assert _current_figure
    _current_figure.clear()

def gca():
    _ensure_axes()
    return _current_axes

def tight_layout():
    pass