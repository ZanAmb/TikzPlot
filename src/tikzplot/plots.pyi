# plots.pyi

from typing import Any, Optional, Tuple, Union, Sequence, Literal
import numpy as np

from .config import TikzConfig as TikzConfig
from .figure import Figure as Figure
from .state import main_name as main_name, next_show_num as next_show_num
from .axes import Axes

ArrayLike = Union[Sequence[float], np.ndarray]
ColorLike = Union[str, Sequence[float]]
LineStyle = Literal["-", "--", "-.", ":", "solid", "dashed", "dashdot", "none", ""]
MarkerStyle = Literal["o", "s", "^", "v", "x", "+", ".", "*", "None", ""]

# --- Figure / Axes creation ---

def figure(*, figsize: Optional[Tuple[float, float]] = ...) -> Figure:
    """
    Create a new figure.

    Parameters
    ----------
    figsize : tuple of float, optional
        Figure size in inches (width, height).
    """
    ...

def subplot(
    nrows: int,
    ncols: int,
    index: int,
    sharex: Optional[Axes] = ...,
    sharey: Optional[Axes] = ...
) -> Axes:
    """
    Create a subplot and make it current.
    """
    ...

def subplots(
    nrows: int = 1,
    ncols: int = 1,
    sharex: Optional[Axes] = ...,
    sharey: Optional[Axes] = ...,
    **kwargs: Any
) -> Tuple[Figure, Union[Axes, np.ndarray]]:
    """
    Create a figure and a set of subplots.

    Returns
    -------
    fig : Figure
    ax : Axes or ndarray of Axes
        - Single Axes if nrows*ncols == 1
        - 1D array if one dimension is 1
        - 2D array otherwise
    """
    ...


# --- Axis label / limits ---

def xlabel(label: str) -> None:
    """
    Set x-axis label.
    """
    ...

def ylabel(label: str) -> None:
    """
    Set y-axis label.
    """
    ...

def title(text: str) -> None:
    """
    Set plot title.
    """
    ...

def xlim(*args: Any, left: Optional[float] = ..., right: Optional[float] = ...) -> None:
    """
    Set x-axis limit(-s). Set as tuple or as kwargs (left, right).

    """
    ...

def ylim(*args: Any, bottom: Optional[float] = ..., top: Optional[float] = ...) -> None:
    """
    Set y-axis limit(-s). Set as tuple or as kwargs (top, bottom).

    """
    ...

def xscale(*args: Any, base: Optional[float] = ...) -> None:
    """
    Set x-axis scale (to log).
    """
    ...

def yscale(*args: Any, base: Optional[float] = ...) -> None:
    """
    Set y-axis scale (to log).
    """
    ...

def xticks(ticks: Sequence[float], labels: Optional[Sequence[str]] = ...) -> None:
    """
    Set x-axis ticks and their labels.
    """
    ...

def yticks(ticks: Sequence[float], labels: Optional[Sequence[str]] = ...) -> None:
    """
    Set y-axis ticks and their labels.
    """
    ...

def grid(visible: bool = True, which: Literal["major","minor","both"] = "major") -> None:
    """
    Set grid.
    """
    ...

def legend(*args: Any, loc: Optional[Union[int,str,Tuple[float,float]]] = ...) -> None:
    """
    Show legend for the selected axis.

    Parameters
    ----------
    loc: int, str or tuple, optional
        Location of legend (as in matplotlib: 1 - upper right, 2 - upper left, ... or with tuple of relative coordinates).
    """
    ...


# --- Plotting (verbatim docstrings) ---

def plot(
    x: ArrayLike = ..., y: ArrayLike = ..., fmt: Optional[str] = ...,
    *,
    alpha: Optional[float] = ...,
    color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
    linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ...,
    linewidth: Optional[float]= ..., lw: Optional[float] = ...,
    marker: Optional[MarkerStyle] = ...,
    markersize: Optional[float] = ..., ms: Optional[float] = ...,
    label: Optional[str] = ...
) -> None:
    """
    Draw a general plot to the selected axis.

    Parameters
    ----------
    x,y : ArrayLike or float
        Datapoints

    fmt: str, optional
        Style

    alpha: float, optional
        Opacity

    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line and markers: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

    label: str, optional
        Legned entry

    linestyle or ls: str, optional
        Line style

    linewidth or lw: float, optional
        Line width in pt
    
    marker: str, optional
        Marker type

    markersize or ms: float, optional
        Mark size in pt
    """
    ...

def scatter(
    x: ArrayLike = ..., y: ArrayLike = ..., fmt: Optional[str] = ...,
    *,
    alpha: Optional[float] = ...,
    color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
    marker: Optional[MarkerStyle] = ...,
    markersize: Optional[float] = ..., ms: Optional[float] = ...,
    label: Optional[str] = ...
) -> None:
    """
    Draw a scatter plot to the selected axis.
    
    Parameters
    ----------
    x,y : ArrayLike or float
        Datapoints

    fmt: str, optional
        Style

    alpha: float, optional
        Opacity

    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line and markers: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

    label: str, optional
        Legned entry
    
    marker: str, optional
        Marker type

    markersize or ms: float, optional
        Mark size in pt
    """
    ...

def semilogy(
    x: ArrayLike = ..., y: ArrayLike = ..., base: Optional[float] = 10,
    fmt: Optional[str] = ...,
    *,
    alpha: Optional[float] = ...,
    color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
    linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ...,
    linewidth: Optional[float]= ..., lw: Optional[float] = ...,
    marker: Optional[MarkerStyle] = ...,
    markersize: Optional[float] = ..., ms: Optional[float] = ...,
    label: Optional[str] = ...
) -> None:
    """
    Draw a general plot to the selected axis and change the current y-axis into log mode.

    Parameters
    ----------
    x,y : ArrayLike or float
        Datapoints

    base: float, optional
        Log basis, default 10

    fmt: str, optional
        Style

    alpha: float, optional
        Opacity

    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line and markers: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

    label: str, optional
        Legned entry

    linestyle or ls: str, optional
        Line style

    linewidth or lw: float, optional
        Line width in pt
    
    marker: str, optional
        Marker type

    markersize or ms: float, optional
        Mark size in pt
    """
    ...

# --- Output ---

def savefig(filename: str) -> None:
    """
    Save figure to .tex/.tikz file.

    If no extension is provided, '.tex' is appended.
    """
    ...

def show() -> None:
    """
    Save figure to autogenerated filename and clear it.
    """
    ...

def clf() -> None:
    """
    Clear current figure.
    """
    ...