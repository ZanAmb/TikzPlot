from typing import Any, Optional, Sequence, Tuple, Union, Literal
import numpy as np
from .colorbar import Colorbar

ArrayLike = Union[Sequence[float], np.ndarray]
ColorLike = Union[str, Sequence[float]]
LineStyle = Literal["-", "--", "-.", ":", "solid", "dashed", "dashdot", "none", ""]
MarkerStyle = Literal["o", "s", "^", "v", "x", "+", ".", "*", "None", ""]
FontSize = Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]


class BaseAxes:   
    def plot(self, x: ArrayLike = ..., y: ArrayLike = ..., fmt: Optional[str] = ...,*, alpha: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label:Optional[str]=...) -> None:
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

    def scatter(self, x: ArrayLike = ..., y: ArrayLike = ..., fmt: Optional[str] = ..., *,alpha: Optional[float] = ..., color: Optional[Union[Sequence[ColorLike], ColorLike]] = ..., c: Optional[ColorLike] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[Union[Sequence[float], float]] = ..., s: Optional[Union[Sequence[float], float]] = ...,  label:Optional[str]=..., cmap: Optional[Union[str, Colorbar]], vmin: Optional[float] = ..., vmax: Optional[float] = ...) -> None:
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
            Legned entry
        
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
    def semilogy(self, x: ArrayLike = ..., y: ArrayLike = ..., base: Optional[float] = 10,  fmt: Optional[str] = ...,*, alpha: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label:Optional[str]=...) -> None:
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
        c: Optional[ColorLike] = ...
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

        """
        ...

    def text(self, x: float, y: float, s: str, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., fontsize: Optional[FontSize] = ..., size: Optional[FontSize] = ..., backgroundcolor: Optional[ColorLike] = ..., horizontalalignment: Optional[str] = ..., ha: Optional[str] = ..., verticalalignment: Optional[str] = ..., va: Optional[str] = ..., rotation: Optional[Union[float, str]] = ..., label: Optional[str] = ...) -> None:
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
    def hlines(
        self,
        y: Union[float, Sequence[float]],
        xmin: Union[float, Sequence[float]],
        xmax: Union[float, Sequence[float]],
        colors: Union[str, Sequence[str]] = "k",
        linestyles: Union[str, Sequence[str]] = "solid",
    ) -> None: 
        """
        Draw horizontal lines to the selected axis.
        """
        ...
    def hist(
        self,
        x: Union[ArrayLike, Sequence[ArrayLike]],
        bins: int = ...,
        density: bool = ...,
        *,
        cumulative: bool = ...,
        orientation: Literal["horizontal","vertical"] = "vertical",
        rwidth: Optional[float] = ...,
        range: Optional[Tuple[float,float]] = ...,
        color: Optional[ColorLike] = ...,
        **kwargs: Any
    ) -> None: 
        """
        Draw histogram to the selected axis.
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
    
    def set_ylabel(self, label: str) -> None: 
        """
        Set y-axis label.
        """
        ...
    def set_ylim(self, *args: Any, bottom: Optional[float] = ..., top: Optional[float] = ...) -> None: 
        """
        Set y-axis limit(-s). Set as tuple or as kwargs (top, bottom).

        """
        ...
    def set_yscale(self, *args: Any, base: Optional[float] = ...) -> None:
        """
        Set y-axis scale (to log).
        """
        ...
    def set_yticks(self, ticks: Sequence[float], labels: Optional[Sequence[str]] = ...) -> None: 
        """
        Set y-axis ticks and their labels.
        """
        ...
    def set_yticklabels(self, labels: Sequence[str]) -> None: 
        """
        Set y-axis tick labels.
        """
        ...
    def legend(self, *args: Any, loc: Optional[Union[int,str,Tuple[float,float]]] = ...) -> None:
        """
        Show legend for the selected axis.

        Parameters
        ----------
        *args:
            - single arg: list/tuple, optional: list of labels to assign to axis elements (in given order assigned to plotted elements in the order of plotting). If label is used on any of the elements, the original label is overwritten.
            - two args: list/tuple, optional: element, label - assign labels to plots (use references of plots which are returned in plot commands). In case that a plot already has a label, both will be displayed. This is the only option to merge the legend entries for double-axis (twinx) plots.
        loc: int, str or tuple, optional
            Location of legend (as in matplotlib: 1 - upper right, 2 - upper left, ... or with tuple of relative coordinates).

        ncols: int, optional: number of columns in legend, default 1
        """
        ...
    def set(self, **kwargs) -> None:
        """
        Set parameter (lims, labels, ticks, ticklabels, title)
        """
        ...
    
class Axes(BaseAxes):
    def __init__(self, nrows: int, ncols: int, index: int, fig: Any) -> None: ...
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
    def vlines(
        self,
        x: Union[float, Sequence[float]],
        ymin: Union[float, Sequence[float]],
        ymax: Union[float, Sequence[float]],
        colors: Union[str, Sequence[str]] = "k",
        linestyles: Union[str, Sequence[str]] = "solid",
    ) -> None: 
        """
        Draw vertical lines to the selected axis.
        """
        ...
    def imshow(self, *args: Any, cmap: Optional[str] = ...) -> Tuple[Any, str, float, float]: 
        """
        Draw image to the selected axis from array. Uses matplotlib imshow() to export to PDF, then inputs the image to the axis. Return may be used to initialize Colorbar().
        """
        ...
    def set_xlabel(self, label: str) -> None: 
        """
        Set x-axis label.
        """
        ...
    def set_title(self, title: str) -> None: 
        """
        Set plot title.
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
    def set_minorticks_num(self, num: int) -> None:
        ...
        """
        Set number of minor ticks between major ticks.
        
        Parameters
        ----------
        num: int
            Number of minor ticks between major ticks.
        """
    def set_xlim(self, *args: Any, left: Optional[float] = ..., right: Optional[float] = ...) -> None: 
        """
        Set x-axis limit(-s). Set as tuple or as kwargs (left, right).

        """
        ...
    def set_xscale(self, *args: Any, base: Optional[float] = ...) -> None: 
        """
        Set x-axis scale (to log).
        """
        ...
    def set_xticks(self, ticks: Sequence[float], labels: Optional[Sequence[str]] = ...) -> None: 
        """
        Set x-axis ticks and their labels.
        """
        ...
    def set_xticklabels(self, labels: Sequence[str]) -> None: 
        """
        Set y-axis tick labels.
        """
        ...
    def twinx(self) -> "Secondary": 
        """
        Initialize secondary y-axis.
        """
        ...
    
class Secondary(BaseAxes):
    def __init__(self, primary: Axes) -> None: ...