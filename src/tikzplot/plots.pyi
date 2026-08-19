# plots.pyi

from typing import Any, Optional, Tuple, Union, Sequence, Literal, overload, Protocol
import numpy as np

from tikzplot.styles import Styles

from .config import TikzConfig
from .colorbar import Colorbar
from .figure import Figure as Figure
from .state import main_name as main_name, next_show_num as next_show_num
from .axes import Axes

ArrayLike = Union[Sequence[float], np.ndarray]
ColorLike = Union[str, Sequence[float], Sequence[Sequence[float] | ArrayLike], np.ndarray, None]
LineStyle = Literal["-", "--", "-.", ":", "solid", "dashed", "dashdot", "none", ""]
MarkerStyle = Literal["o", "s", "^", "v", "x", "+", ".", "*", "None", ""]
FontSize = Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]

style: Styles

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
    sharex: Optional[str] = None,
    sharey: Optional[str] = None
) -> Axes:
    """
    Create a subplot and make it current.
    """
    ...

"""class AxesGrid(Protocol):
    @overload
    def __getitem__(self, index: int) -> Axes: ...
    @overload
    def __getitem__(self, index: tuple[int, int]) -> Axes: ...
    def __iter__(self): ...

@overload
def subplots(
    nrows: Literal[1] = 1,
    ncols: Literal[1] = 1,
    sharex: Optional[str] = None,
    sharey: Optional[str] = None,
    **kwargs: Any
) -> tuple[Figure, Axes]: ...

@overload
def subplots(
    nrows: int,
    ncols: int,
    sharex: Optional[str] = None,
    sharey: Optional[str] = None,
    **kwargs: Any
) -> tuple[Figure, AxesGrid]: ..."""

def subplots(
    nrows: int = 1,
    ncols: int = 1,
    sharex: Optional[str] = None,
    sharey: Optional[str] = None,
    **kwargs: Any,
) -> tuple[Figure, Any]:
    """
    Create a figure and a set of subplots.

    Returns
    -------
    fig : Figure
    ax : Axes or ndarray of Axes
        - Single Axes if nrows*ncols == 1
        - 1D array if one dimension is 1
        - 2D array otherwise

    figsize : tuple, optional
        Figure size in inches (width, height).

    sharex, sharey : Axes, optional
        Specify if row, column or all subplots should share x or y axis.
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

def xticks(ticks: ArrayLike, labels: Optional[Sequence[str]] = ...) -> None:
    """
    Set x-axis ticks and their labels.
    """
    ...

def yticks(ticks: ArrayLike, labels: Optional[Sequence[str]] = ...) -> None:
    """
    Set y-axis ticks and their labels.
    """
    ...

def grid(self, visible: bool = True, which: Literal["major","minor","both"] = "major", alpha: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...) -> None: 
    """
    Set grid.

    Parameters
    ----------
    visible: bool, default True
        Show grid

    which: {"major", "minor", "both"}, default "major"
        Grid selector

    alpha: float, optional
        Opacity
        
    color or c: all matplotlib color formats (without X11/xkcd), optional
        Grid color: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
        
    linestyle or ls: str, optional
        Grid line style
        
    linewidth or lw: float, optional
        Grid line width in pt
    """
def set_minorticks_num(num: int) -> None:
    """
    Set number of minor ticks between major ticks.

    Parameters
    ----------
    num: int
        Number of minor ticks between major ticks.
    """
def legend(self, *args: Any, loc: Optional[Union[int,str,Tuple[float,float]]] = ..., facecolor: Optional[ColorLike] = ..., edgecolor: Optional[ColorLike] = ..., labelcolor: Optional[ColorLike] = ..., frameon: Optional[bool] = ..., anchor: Optional[Literal["north", "south", "east", "west", "center", "north west", "north east", "south west", "south east"]] = ..., fontsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ...) -> None:
    """
    Show legend for the selected axis. Despite arguments requires at least one plotted element on the axis (not necesarily with label) to show up (LaTeX does not allow legend on empty axis).

    Parameters
    ----------
    *args:
        - single arg: list/tuple, optional: list of labels to assign to axis elements (in given order assigned to plotted elements in the order of plotting). If label is used on any of the elements, the original label is overwritten.
        - two args: list/tuple, optional: element, label - assign labels to plots (use references of plots which are returned in plot commands). In case that a plot already has a label, both will be displayed. This is the only option to merge the legend entries for double-axis (twinx) plots.
            
    loc: int, str or tuple, optional
        Location of legend (as in matplotlib: 1 - upper right, 2 - upper left, ... or with tuple of relative coordinates).

    ncols: int, optional: number of columns in legend, default 1

    facecolor, edgecolor, labelcolor: all matplotlib color formats (without X11/xkcd), optional
            Color of legend box, edge and text, respectively"

    fontsize: FontSize or int, optional
        Font size of legend text

    anchor: {"north", "south", "east", "west", "center", "north west", "north east", "south west", "south east"}, optional
        Anchor of legend box, default "north east" (for custom loc)
    """
    ...

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
        Legend entry

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
def errorbar(self, x: ArrayLike = ..., y: ArrayLike = ..., yerr: Optional[ArrayLike | float] = ..., xerr: Optional[ArrayLike | float] = ..., fmt: Optional[str] = ..., *, alpha: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label:Optional[str]=...) -> None:
    """
    Draw a plot with errrorbars to the selected axis.
    Parameters
    ----------
    x,y : ArrayLike or float
        Datapoints
    
    yerr, xerr: ArrayLike or float
        Datapoint error (constant, symmetric, asymmetric)
    
    fmt: str, optional
        Style
    
    alpha: float, optional
        Opacity
    
    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line and markers: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
    
    label: str, optional
        Legend entry
    
    linestyle or ls: str, optional
        Line style
    
    linewidth or lw: float, optional
        Line width in pt
    
    marker: str, optional
        Marker type
    
    markersize or ms: float, optional
        Mark size in pt

    ecolor: float, optional
        Color of errorbar

    elinewidth: float, optional
        Errorbar line width in pt

    capsize: float, optional
        Errorbar cap length in pt

    elinestyle: str, optional
        Errorbar line style
    """
    ...
def scatter(self, x: ArrayLike = ..., y: ArrayLike = ..., fmt: Optional[str] = ..., *,alpha: Optional[float] = ..., color: Optional[Union[Sequence[ColorLike], ColorLike]] = ..., c: Optional[ColorLike] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[Union[ArrayLike, float]] = ..., s: Optional[Union[ArrayLike, float]] = ...,  label:Optional[str]=..., cmap: Optional[Union[str, Colorbar]], vmin: Optional[float] = ..., vmax: Optional[float] = ...) -> None:
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
    
    color or c: array like or single: all matplotlib color formats (without X11/xkcd) or float for colormap, optional
        color of line and markers: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible. Note that if the sequence if of the same length as x, it will be interpreted as color sequence for each point, otherwise it will be interpreted as a single color for all points.
    
    label: str, optional
        Legend entry
    
    marker: str, optional
        Marker type
    
    markersize or s: ArrayLike or float, optional
        Mark size in pt (or in 1/50 pt for s), if a sequence of same length as x, it will be interpreted as size for each point, otherwise it will be interpreted as a single size for all points.
    
    cmap: str or Colorbar, optional
        Colormap for scatter points, if color is given as float or sequence of floats. Can be a colormap name or a Colorbar object.
    
    vmin, vmax: float, optional
        Colorbar limits for scatter points, if color is given sequence of floats and cmap is given as string, otherwise ignored. If cmap is given as str and no vmin or vmax is provided, they will be set to the min and max of color sequence.
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
        Legend entry

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

def stem(self, *args: Any, orientation: Literal["horizontal","vertical"] = "vertical", linefmt:Optional[str] = ..., markerfmt:Optional[str]=...,
         label:Optional[str]=...) -> None: 
    """
    Draw a stem plot to the selected axis.
    Parameters
    ----------
    locs, heads: ArrayLike
        Datapoints for plot, (x,y) for vertical, (y,x) for horizontal
    
    orientation: {"vertical", "horizontal"}, default "vertical
        Orientation of stems
    
    alpha: float, optional
        Opacity
    
    linefmt, markerfmt: str, optional
        Short style of line and marker
    
    label: str, optional
        Legend entry
    """
    ...

def fill_between(
    self,
    x: ArrayLike,
    y1: ArrayLike,
    y2: Optional[ArrayLike] = ...,
    alpha: Optional[float] = ...,
    color: Optional[ColorLike] = ...,
    c: Optional[ColorLike] = ...,
    label: Optional[str] = ...,
    hatch: Optional[str] = ...,
    hatch_color: Optional[ColorLike] = ...,
    hatch_linewidth: Optional[float] = ...,
    hatch_distance: Optional[float] = ...,
) -> None: 
    """
    Fill space between two plots (or a single plot and x-axis).

    Parameters
    ----------
    x,y1, y2 : ArrayLike or float (y2 optional)
        Datapoints, if matched with existing plot, that line will be recycled to save tikz memory.

    alpha: float, optional
        Opacity

    color or c: all matplotlib color formats (without X11/xkcd), optional
        Fill color: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
    
    label: str, optional
        Legend entry
    
    hatch: str, optional
        The hatch pattern to use for filling the bars. Can be a string of characters that define the hatch pattern (e.g., '/', '\\', '|', '-', '+', 'x', '.', '*'). If not provided, no hatching is applied.
    
    hatch_color: ColorLike, optional
        The color of the hatch pattern. If not provided, the default color cycle is used.

    hatch_linewidth: float, optional    
        The line width of the hatch pattern in points. If not provided, the default line width is used.

    hatch_distance: float, optional
        The distance between hatch lines in points. If not provided, the default distance is used.
    """
    ...
def text(self, x: float, y: float, s: str, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., fontsize: Optional[FontSize] = ..., on_top: Optional[bool] = ..., size: Optional[FontSize] = ..., backgroundcolor: Optional[ColorLike] = ..., horizontalalignment: Optional[str] = ..., ha: Optional[str] = ..., verticalalignment: Optional[str] = ..., va: Optional[str] = ..., rotation: Optional[Union[float, str]] = ..., label: Optional[str] = ...) -> None:
    """
    Add text to the selected axis.
    Parameters
    ----------
    x,y: float
        Text position in axis coordinates
    
    s: str
        Text content (LaTeX format)
    
    color or c: all matplotlib color formats (without X11/xkcd), optional
        Text color: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
    
    fontsize or size: FontSize, optional
        Font size
    
    on_top: bool, optional
        Draw text on top of other elements (True by default)
    
    backgroundcolor: all matplotlib color formats (without X11/xkcd), optional
        Background color of text box: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
    
    horizontalalignment or ha: {"center", "left", "right"}, optional
        Horizontal alignment of text
    
    verticalalignment or va: {"center", "top", "bottom"}, optional
        Vertical alignment of text
    
    rotation: float or {"vertical", "horizontal"}, optional
        Rotation angle in degrees or preset rotation
    
    label: str, optional
        Legend entry
    """
    ...

def loglog(self, x: ArrayLike = ..., y: ArrayLike = ..., base: Optional[float] = 10,  fmt: Optional[str] = ...,*, alpha: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...) -> None:
    """
    Draw a general plot to the selected axis and change the current axis into log mode.

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
        Legend entry
    
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

def hist(
    self,
    x: Union[ArrayLike, Sequence[ArrayLike]],
    bins: int | Sequence[float] = 10,
    *,
    weight: ArrayLike | None = None,
    density: bool = False,
    cumulative: bool = False,
    histtype: Literal["bar", "barstacked", "step", "stepfilled"] = "bar",
    orientation: Literal["horizontal","vertical"] = "vertical",
    rwidth: float | None = None,
    range: Tuple[float,float] | None = None,
    color: ColorLike = ...,
    facecolor: ColorLike = ...,
    fc: ColorLike = ...,
    edgecolor: ColorLike = ...,
    ec: ColorLike = ...,
    align: Literal["left", "mid", "right"] = ...,
    stacked: bool = False,
    fill: bool = True,
    hatch: str | None = None,
    hatch_color: ColorLike | None = None,
    hatch_linewidth: float | None = None,
    hatch_distance: float | None = None,
    #kwargs: Any,
) -> None:
    """
    Draw histogram to the selected axis.

    Parameters
    ----------
    x: ArrayLike or sequence of ArrayLike
        Data to be histogrammed. If a sequence of arrays is given, each array is histogrammed separately and the result is stacked (if stacked=True) or overlaid.
    
    bins: int or sequence of float, optional
        Number of bins or bin edges. If an integer is given, it defines the number of equal-width bins in the given range (10 by default). If a sequence is given, it defines the bin edges, including the rightmost edge.
    
    density: bool, optional
        If True, the histogram is normalized to form a probability density, i.e., the area under the histogram will sum to 1. Default is False.
    
    cumulative: bool, optional
        If True, the histogram is cumulative, i.e., each bin will contain the sum of all previous bins. Default is False.
    
    histtype: {"bar", "barstacked", "step", "stepfilled"}, optional
        The type of histogram to draw. "bar" (default) draws a traditional bar histogram, "barstacked" draws a stacked bar histogram, "step" draws a line plot that represents the histogram, and "stepfilled" draws a filled step plot.
    
    orientation: {"horizontal", "vertical"}, optional
        The orientation of the histogram. "vertical" (default) draws vertical bars, while "horizontal" draws horizontal bars.
    
    rwidth: float, optional
        The relative width of the bars as a fraction of the bin width. If None (default), the bars will be drawn with full width.
    
    range: tuple of float, optional
        The lower and upper range of the bins. If not provided, the range is automatically determined from the data.
    
    color, facecolor, fc, edgecolor, ec: ColorLike, optional
        The color of the bars. Can be a single color or a sequence of colors for multiple datasets. If not provided, the default color cycle is used.
    
    align: {"left", "mid", "right"}, optional
        The alignment of the bars. "mid" (default) centers the bars on the bin edges, "left" aligns the left edge of the bars with the bin edges, and "right" aligns the right edge of the bars with the bin edges.
    
    stacked: bool, optional
        If True, multiple datasets are stacked on top of each other. Default is False.
    
    fill: bool, optional
        If True (default), the bars are filled. If False, only the edges of the bars are drawn.
    
    hatch: str, optional
        The hatch pattern to use for filling the bars. Can be a string of characters that define the hatch pattern (e.g., '/', '\\', '|', '-', '+', 'x', '.', '*'). If not provided, no hatching is applied.
    
    hatch_color: ColorLike, optional
        The color of the hatch pattern. If not provided, the default color cycle is used.
    
    hatch_linewidth: float, optional
        The line width of the hatch pattern in points. If not provided, the default line width is used.
    
    hatch_distance: float, optional
        The distance between hatch lines in points. If not provided, the default distance is used.
    """
    ...

def bar(self, x: ArrayLike | float, height: ArrayLike | float, width: ArrayLike | float = 0.8, bottom: ArrayLike | float = 0.0, align: Literal["center", "edge"] = "center", color: Optional[ColorLike] = None, c: Optional[ColorLike] = None, facecolor: Optional[ColorLike] = None, fc: Optional[ColorLike] = None, edgecolor: Optional[ColorLike] = None, ec: Optional[ColorLike] = None, linewidth: Optional[float] = None, lw: Optional[float] = None, tick_label: Optional[str] = None, label: Optional[str] = None, xerr: Optional[ArrayLike] = None, yerr: Optional[ArrayLike] = None, ecolor: Optional[ColorLike] = None, capsize: Optional[float] = None, hatch: Optional[str] = None, hatch_color: Optional[ColorLike] = None, hatch_linewidth: Optional[float] = None, hatch_distance: Optional[float] = None) -> None:
    """
    Draw a bar plot to the selected axis.

    Parameters
    ----------
    x: ArrayLike or float
        x coordinates of the bars
    
    height: ArrayLike or float
        Heights of the bars
    
    width: ArrayLike or float, optional
        Widths of the bars, default 0.8
    
    bottom: ArrayLike or float, optional
        y coordinates of the bottom of the bars, default 0.0
    
    align: {"center", "edge"}, optional
        Alignment of the bars, default "center"
    
    color, facecolor, fc, edgecolor, ec: ColorLike, optional
        Color of the bars and edges
    
    linewidth or lw: float, optional
        Line width of the edges in pt
    
    tick_label: str, optional
        Tick label for the bars
    
    label: str, optional
        Legend entry for the bars
    
    xerr, yerr: ArrayLike or float, optional
        Error bar sizes in x and y directions
    
    ecolor: ColorLike, optional
        Color of the error bars
    
    capsize: float, optional
        Size of the error bar caps in pt
    
    hatch: str, optional
        Hatch pattern for the bars
    
    hatch_color: ColorLike, optional
        Color of the hatch pattern
    
    hatch_linewidth: float, optional
        Line width of the hatch pattern in pt
    
    hatch_distance: float, optional
        Distance between hatch lines in pt
    """
    ...

def barh(self, y: ArrayLike | float, width: ArrayLike | float, height: ArrayLike | float = 0.8, left: ArrayLike | float = 0.0, align: Literal["center", "edge"] = "center", color: Optional[ColorLike] = None, c: Optional[ColorLike] = None, facecolor: Optional[ColorLike] = None, fc: Optional[ColorLike] = None, edgecolor: Optional[ColorLike] = None, ec: Optional[ColorLike] = None, linewidth: Optional[float] = None, lw: Optional[float] = None, tick_label: Optional[str] = None, label: Optional[str] = None, xerr: Optional[ArrayLike] = None, yerr: Optional[ArrayLike] = None, ecolor: Optional[ColorLike] = None, capsize: Optional[float] = None, hatch: Optional[str] = None, hatch_color: Optional[ColorLike] = None, hatch_linewidth: Optional[float] = None, hatch_distance: Optional[float] = None) -> None:
    """
    Draw a horizontal bar plot to the selected axis.

    Parameters
    ----------
    y: ArrayLike or float
        y coordinates of the bars
    
    width: ArrayLike or float
        Widths of the bars
    
    height: ArrayLike or float, optional
        Heights of the bars, default 0.8
    
    left: ArrayLike or float, optional
        x coordinates of the left side of the bars, default 0.0
    
    align: {"center", "edge"}, optional
        Alignment of the bars, default "center"
    
    color, facecolor, fc, edgecolor, ec: ColorLike, optional
        Color of the bars and edges
    
    linewidth or lw: float, optional
        Line width of the edges in pt
    
    tick_label: str, optional
        Tick label for the bars
    
    label: str, optional
        Legend entry for the bars
    
    xerr, yerr: ArrayLike or float, optional
        Error bar sizes in x and y directions
    
    ecolor: ColorLike, optional
        Color of the error bars
    
    capsize: float, optional
        Size of the error bar caps in pt
    
    hatch: str, optional
        Hatch pattern for the bars
    
    hatch_color: ColorLike, optional
        Color of the hatch pattern
    
    hatch_linewidth: float, optional
        Line width of the hatch pattern in pt
    
    hatch_distance: float, optional
        Distance between hatch lines in pt
    """
    ...

def magnify(self, x_p: float, y_p: float, x_m: float, y_m: float, zoom: float, size: float, **kwargs) -> int:
    """
    Add a spyviewer to the selected axis.
    Parameters
    ----------
    x_p, y_p: float
        Spy point coordinates in axis units
    
    x_m, y_m: float
        Spy view coordinates in cm
    
    zoom: float
        Spy zoom
    
    size: float
        Spy viewer size in cm
    
    shape: {"circle"}, optional
        Spy shape, default square
    
    connect: bool, optional
        Connect spy point and view with a line, default False
    """
    ...

def hlines(
    self,
    y: Union[float, ArrayLike],
    xmin: Union[float, ArrayLike],
    xmax: Union[float, ArrayLike],
    colors: Union[str, Sequence[str]] = "k",
    linestyles: Union[str, Sequence[str]] = "solid",
) -> None: 
    """
    Draw horizontal lines to the selected axis.
    """
    ...

def vlines(
    self,
    x: Union[float, ArrayLike],
    ymin: Union[float, ArrayLike],
    ymax: Union[float, ArrayLike],
    colors: Union[str, Sequence[str]] = "k",
    linestyles: Union[str, Sequence[str]] = "solid",
) -> None: 
    """
    Draw vertical lines to the selected axis.
    """
    ...

def semilogx(self, x: ArrayLike = ..., y: ArrayLike = ..., base: Optional[float] = 10,  fmt: Optional[str] = ...,*, alpha: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...) -> None:
    """
    Draw a general plot to the selected axis and change the current x-axis into log mode.
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
        Legend entry
    
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
def imshow(self, *args: Any, cmap: Optional[str] = ...) -> Tuple[Any, str, float, float]: 
    """
    Draw image to the selected axis from array. Uses matplotlib imshow() to export to PDF, then inputs the image to the axis. Return may be used to initialize Colorbar().
    """
    ...

def step(self, x: ArrayLike, y: ArrayLike, *args: Any, where: Literal["pre","post","mid"] = "pre", **kwargs: Any) -> None:
    """
    Draw a step plot to the selected axis.
    Parameters
    ----------
    x,y : ArrayLike or float
        Datapoints
    
    where: {"pre", "post", "mid"}, default "pre"
        Define where the steps should be placed: before the value (pre), after the value (post), or centered on the value (mid).
    
    fmt: str, optional
        Style
    
    alpha: float, optional
        Opacity
    
    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line and markers: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
    
    label: str, optional
        Legend entry
    
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

def axvline(self, x:float, ymin:float=0, ymax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., linestyle:Optional[str] = ..., linewidth:Optional[float] = ..., label:Optional[str] = ...) -> None:
    """
    Draw a vertical line to the selected axis at given x coordinate.

    Parameters
    ----------
    x: float
        x coordinate of the line in axis units
    x: float
        X coordinate of the line(s)
        
    ymin, ymax: float, optional
        Y relative coordinate of the lower and upper end of the line
        
    alpha: float, optional
        Opacity

    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

    linestyle or ls: str, optional
        Line style

    linewidth or lw: float, optional
        Line width in pt

    label: str, optional
        Legend entry
    """
    ...

def axhline(self, y:float, xmin:float=0, xmax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., linestyle:Optional[str] = ..., linewidth:Optional[float] = ..., label:Optional[str] = ...) -> None:
    """
    Draw a horizontal line to the selected axis at given y coordinate.

    Parameters
    ----------
    y: float
        y coordinate of the line in axis units
        
    xmin, xmax: float, optional
        X relative coordinate of the left and right end of the line
        
    alpha: float, optional
        Opacity

    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

    linestyle or ls: str, optional
        Line style

    linewidth or lw: float, optional
        Line width in pt

    label: str, optional
        Legend entry
    """
    ...

def axvspan(self, xmin:float, xmax:float, ymin:float=0, ymax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., linestyle:Optional[str] = ..., linewidth:Optional[float] = ..., label:Optional[str] = ..., hatch:Optional[str] = ..., hatch_color:Optional[ColorLike] = ..., hatch_linewidth:Optional[float] = ..., hatch_distance:Optional[float] = ...) -> None:
    """
    Draw a vertical span to the selected axis between given x coordinates.

    Parameters
    ----------
    xmin, xmax: float
        X coordinates of the left and right end of the span in axis units
        
    ymin, ymax: float, optional
        Y relative coordinate of the lower and upper end of the span
        
    alpha: float, optional
        Opacity

    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

    linestyle or ls: str, optional
        Line style

    linewidth or lw: float, optional
        Line width in pt

    label: str, optional
        Legend entry
    
    hatch: str, optional
        The hatch pattern to use for filling the bars. Can be a string of characters that define the hatch pattern (e.g., '/', '\\', '|', '-', '+', 'x', '.', '*'). If not provided, no hatching is applied.
        
    hatch_color: ColorLike, optional
        The color of the hatch pattern. If not provided, the default color cycle is used.
    
    hatch_linewidth: float, optional    
        The line width of the hatch pattern in points. If not provided, the default line width is used.
    
    hatch_distance: float, optional
        The distance between hatch lines in points. If not provided, the default distance is used.
    """
    ...

def axhspan(self, ymin:float, ymax:float, xmin:float=0, xmax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., linestyle:Optional[str] = ..., linewidth:Optional[float] = ..., label:Optional[str] = ..., hatch:Optional[str] = ..., hatch_color:Optional[ColorLike] = ..., hatch_linewidth:Optional[float] = ..., hatch_distance:Optional[float] = ...) -> None:
    """
    Draw a horizontal span to the selected axis between given y coordinates.

    Parameters
    ----------
    ymin, ymax: float
        Y coordinates of the lower and upper end of the span in axis units
        
    xmin, xmax: float, optional
        X relative coordinate of the left and right end of the span
        
    alpha: float, optional
        Opacity

    color or c: all matplotlib color formats (without X11/xkcd), optional
        color of line: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

    linestyle or ls: str, optional
        Line style

    linewidth or lw: float, optional
        Line width in pt

    label: str, optional
        Legend entry
    
    hatch: str, optional
        The hatch pattern to use for filling the bars. Can be a string of characters that define the hatch pattern (e.g., '/', '\\', '|', '-', '+', 'x', '.', '*'). If not provided, no hatching is applied.
        
    hatch_color: ColorLike, optional
        The color of the hatch pattern. If not provided, the default color cycle is used.
    
    hatch_linewidth: float, optional    
        The line width of the hatch pattern in points. If not provided, the default line width is used.
    
    hatch_distance: float, optional
        The distance between hatch lines in points. If not provided, the default distance is used.
    """
    ...

def minorticks_num(self, num: int) -> None:
    ...
    """
    Set number of minor ticks between major ticks.
    
    Parameters
    ----------
    num: int
        Number of minor ticks between major ticks.
    """

def savefig(filename: str, standalone: None | bool = None, print_requirements: bool = False) -> None:
    """
    Save figure to .tex/.tikz file.

    If no suitable extension is provided, '.tex' is appended. If using .png extension, the code generated will compile to a .png image.

    Parameters
    ----------
    filename: str
        Name of the file to save the figure to. If no suitable extension is provided, '.tex' is appended. If using .png extension, the code generated will compile to a .png image.

    standalone: bool, optional
        If True, the generated .tex file will be a standalone document. If False, it will be a fragment that can be included in another document. If None (default), the behavior is determined by the global setting `TikzConfig.STANDALONE`.

    print_requirements: bool, optional
        If True, the required LaTeX packages will be printed to the console. Inhibited for standalone.
    """
    ...

def show(standalone: None | bool = None, print_requirements: bool = False) -> None:
    """
    Save figure to autogenerated filename and clear it.

    Parameters
    ----------
    standalone: bool, optional
        If True, the generated .tex file will be a standalone document. If False, it will be a fragment that can be included in another document. If None (default), the behavior is determined by the global setting `TikzConfig.STANDALONE`.
    
    print_requirements: bool, optional
        If True, the required LaTeX packages will be printed to the console. Inhibited for standalone."""
    ...

def clf() -> None:
    """
    Clear current figure.
    """
    ...

def gca() -> Axes:
    """
    Get current axis.
    """
    ...

def tight_layout() -> None: ...