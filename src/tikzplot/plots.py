import numpy as _np

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
    _current_axes = _current_figure.add_subplot(nrows, ncols, index, sharex=sharex, sharey=sharey, projection=projection, polar=polar)
    return _current_axes

def subplots(nrows=1, ncols=1, sharex=None, sharey=None, subplot_kw=None, **kwargs):

    global _current_figure, _current_axes
    if _current_figure is None:
        _current_figure = Figure(style)
    axs = _current_figure.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey, subplot_kw=subplot_kw, **kwargs)
    if isinstance(axs, _np.ndarray):
        if isinstance(axs[0], _np.ndarray):
            _current_axes = axs[0, 0]
        else:
            _current_axes = axs[0]
    else:
        _current_axes = axs
    return _current_figure, axs

def subplot_mosaic(mosaic, *, sharex=False, sharey=False, width_ratios=None, height_ratios=None, empty_sentinel=".", **kwargs):
    global _current_figure
    if _current_figure is None:
        _current_figure = Figure(style)
    axs = _current_figure.subplot_mosaic(mosaic, sharex=sharex, sharey=sharey, width_ratios=width_ratios, height_ratios=height_ratios, empty_sentinel=empty_sentinel, **kwargs)

    return _current_figure, axs
    
    

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

def bar(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("bar is not supported for 3D axes.")
    return _current_axes.bar(*args, **kwargs)

def barh(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("barh is not supported for 3D axes.")
    return _current_axes.barh(*args, **kwargs)

def grouped_bar(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("grouped_bar is not supported for 3D axes.")
    return _current_axes.grouped_bar(*args, **kwargs)

def stackplot(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("stackplot is not supported for 3D axes.")
    return _current_axes.stackplot(*args, **kwargs)

def bar_labels(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("bar_labels is not supported for 3D axes.")
    return _current_axes.bar_label(*args, **kwargs)

def step(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("step is not supported for 3D axes.")
    return _current_axes.step(*args, **kwargs)

def ecdf(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("ecdf is not supported for 3D axes.")
    return _current_axes.ecdf(*args, **kwargs)

def magnitude_spectrum(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("magnitude_spectrum is not supported for 3D axes.")
    return _current_axes.magnitude_spectrum(*args, **kwargs)

def angle_spectrum(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("angle_spectrum is not supported for 3D axes.")
    return _current_axes.angle_spectrum(*args, **kwargs)

def phase_spectrum(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("phase_spectrum is not supported for 3D axes.")
    return _current_axes.phase_spectrum(*args, **kwargs)

def specgram(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("specgram is not supported for 3D axes.")
    return _current_axes.specgram(*args, **kwargs)

def psd(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("psd is not supported for 3D axes.")
    return _current_axes.psd(*args, **kwargs)

def pie(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("pie is not supported for 3D axes.")
    return _current_axes.pie(*args, **kwargs)

def pie_label(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("pie_label is not supported for 3D axes.")
    return _current_axes.pie_label(*args, **kwargs)

def bxp(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("bxp is not supported for 3D axes.")
    return _current_axes.bxp(*args, **kwargs)

def boxplot(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("boxplot is not supported for 3D axes.")
    return _current_axes.boxplot(*args, **kwargs)

def violin(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("violin is not supported for 3D axes.")
    return _current_axes.violin(*args, **kwargs)

def violinplot(*args, **kwargs):
    _ensure_axes()
    assert _current_axes
    if isinstance(_current_axes, Axes3):
        raise ValueError("violinplot is not supported for 3D axes.")
    return _current_axes.violinplot(*args, **kwargs)

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

def savefig(filename, standalone=None, print_requirements=False):
    _im = False
    if filename.endswith(".png"):
        if not TikzConfig.STANDALONE:
            print("Must be in standalone mode to create code for image. TikzConfig.STANDALONE is now set to True.")
            TikzConfig.modifyParam(STANDALONE=True)
        _im = True
        print("If .png is not generated on compile while running in vs-code, edit latex.workshop.latex.tools in settings.json: under args, add: -shell-escape.")
        filename = filename.removesuffix(".png") + ".tex"
    if not(filename.endswith(".tex") or filename.endswith(".tikz")):
        filename += ".tex"
    assert _current_figure
    if _im:
        _current_figure._save_image(filename)
    else:
        _current_figure._save(filename, standalone=standalone, print_requirements=print_requirements)

def show(standalone=None, print_requirements=False):
    assert _current_figure
    _current_figure._save(f"{str(main_name()[1]).removesuffix('.py')}_{TikzConfig.SHOW_SAVENAME}{next_show_num()}.tex", standalone=standalone, print_requirements=print_requirements)
    clf()

def clf():
    assert _current_figure
    _current_figure.clear()

def gca():
    _ensure_axes()
    return _current_axes

def tight_layout(*args, **kwargs):
    assert _current_figure
    _current_figure.tight_layout(*args, **kwargs)

def sca(ax):
    global _current_axes
    _current_axes = ax

def colorbar(*args, **kwargs):
    global _current_figure
    if _current_figure is None:
        _current_figure = Figure(style)
    return _current_figure.colorbar(*args, **kwargs)