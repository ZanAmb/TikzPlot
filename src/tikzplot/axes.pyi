from typing import Any, Optional, Sequence, Tuple, Union, Literal
import numpy as np

ArrayLike = Union[Sequence[float], np.ndarray]
ColorLike = Union[str, Sequence[float]]
LineStyle = Literal["-", "--", "-.", ":", "solid", "dashed", "dashdot", "none", ""]
MarkerStyle = Literal["o", "s", "^", "v", "x", "+", ".", "*", "None", ""]


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

    def scatter(self, x: ArrayLike = ..., y: ArrayLike = ..., fmt: Optional[str] = ..., *,alpha: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label:Optional[str]=...) -> None:
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
    def errorbar(x: ArrayLike = ..., y: ArrayLike = ..., yerr: Optional[ArrayLike | float] = ..., xerr: Optional[ArrayLike | float] = ..., fmt: Optional[str] = ..., *, alpha: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
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
        locs, heads: ArrayLike
            Datapoints for plot, (x,y) for vertical, (y,x) for horizontal

        orientation: {"vertical", "horizontal"}, default "vertical
            Orientation of stems

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
        loc: int, str or tuple, optional
            Location of legend (as in matplotlib: 1 - upper right, 2 - upper left, ... or with tuple of relative coordinates).
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
    def grid(self, visible: bool = True, which: Literal["major","minor","both"] = "major") -> None: 
        """
        Set grid.
        """
        ...
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