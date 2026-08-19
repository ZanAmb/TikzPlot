from typing import Any, Optional, Sequence, Tuple, Union, Literal
import numpy as np
from .colorbar import Colorbar

ArrayLike = Union[Sequence[float], np.ndarray]
ColorLike = Union[str, Sequence[float], Sequence[Sequence[float] | ArrayLike], np.ndarray, None]
LineStyle = Literal["-", "--", "-.", ":", "solid", "dashed", "dashdot", "none", ""]
MarkerStyle = Literal["o", "s", "^", "v", "x", "+", ".", "*", "None", ""]
FontSize = Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]
HatchStyle = Literal["/", "\\", "|", "-", "+", "x", ".", "*"]


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
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label: Optional[str]= ..., ecolor: Optional[ColorLike] = ..., elinewidth: Optional[float] = ..., capsize: Optional[float] = ..., elinestyle: Optional[LineStyle] = ...) -> None:
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

    def text(self, x: float, y: float, s: str, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., fontsize: Optional[FontSize] = ..., on_top: bool = ..., size: Optional[FontSize] = ..., backgroundcolor: Optional[ColorLike] = ..., horizontalalignment: Optional[str] = ..., ha: Optional[str] = ..., verticalalignment: Optional[str] = ..., va: Optional[str] = ..., rotation: Optional[Union[float, str]] = ..., label: Optional[str] = ...) -> None:
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
        hatch: str = ...,
        hatch_color: ColorLike = ...,
        hatch_linewidth: float = ...,
        hatch_distance: float = ...,
        #**kwargs: Any
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
            X coordinates or labels of the bars
        
        height: ArrayLike or float
            Heights of the bars

        width: ArrayLike or float, optional
            Widths (on x scale) of the bars (default 0.8)

        bottom: ArrayLike or float, optional
            Y coordinates of the bottom of the bars (default 0.0)

        align: {"center", "edge"}, optional
            Alignment of the bars: "center" (default) or "edge"

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Fill color of the bars

        facecolor or fc: all matplotlib color formats (without X11/xkcd), optional
            Fill color of the bars (same as color)

        edgecolor or ec: all matplotlib color formats (without X11/xkcd), optional
            Edge color of the bars

        linewidth or lw: float, optional
            Line width of the edges in pt

        tick_label: str or list of str, optional
            Tick labels for the bars

        label: str, optional
            Legend entry for the bars

        xerr, yerr: ArrayLike or float, optional
            Error bar sizes for the bars

        ecolor: all matplotlib color formats (without X11/xkcd), optional
            Color of the error bars

        capsize: float, optional
            Size of the error bar caps in pt

        hatch: str, optional
            The hatch pattern to use for filling the bars. Can be a string of characters that define the hatch pattern (e.g., '/', '\\', '|', '-', '+', 'x', '.', '*'). If not provided, no hatching is applied.

        hatch_color: ColorLike, optional
            The color of the hatch pattern. If not provided, the default color cycle is used.

        hatch_linewidth: float, optional
            The line width of the hatch pattern in points. If not provided, the default line width is used.

        hatch_distance: float, optional
            The distance between hatch lines in points. If not provided, the default distance is used.

        """

    def barh(self, y: ArrayLike | float, width: ArrayLike | float, height: ArrayLike | float = 0.8, left: ArrayLike | float = 0.0, align: Literal["center", "edge"] = "center", color: Optional[ColorLike] = None, c: Optional[ColorLike] = None, facecolor: Optional[ColorLike] = None, fc: Optional[ColorLike] = None, edgecolor: Optional[ColorLike] = None, ec: Optional[ColorLike] = None, linewidth: Optional[float] = None, lw: Optional[float] = None, tick_label: Optional[str | list[str]] = None, label: Optional[str] = None, xerr: Optional[ArrayLike] = None, yerr: Optional[ArrayLike] = None, ecolor: Optional[ColorLike] = None, capsize: Optional[float] = None, hatch: Optional[str] = None, hatch_color: Optional[ColorLike] = None, hatch_linewidth: Optional[float] = None, hatch_distance: Optional[float] = None) -> None:
        """
        Draw a horizontal bar plot to the selected axis.

        Parameters
        ----------
        y: ArrayLike or float
            Y coordinates or labels of the bars
        
        width: ArrayLike or float
            Widths (on x scale) of the bars

        height: ArrayLike or float, optional
            Heights (on y scale) of the bars (default 0.8)

        left: ArrayLike or float, optional
            X coordinates of the left side of the bars (default 0.0)

        align: {"center", "edge"}, optional
            Alignment of the bars: "center" (default) or "edge"

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Fill color of the bars

        facecolor or fc: all matplotlib color formats (without X11/xkcd), optional
            Fill color of the bars (same as color)

        edgecolor or ec: all matplotlib color formats (without X11/xkcd), optional
            Edge color of the bars

        linewidth or lw: float, optional
            Line width of the edges in pt

        tick_label: str or list of str, optional
            Tick labels for the bars

        label: str, optional
            Legend entry for the bars

        xerr, yerr: ArrayLike or float, optional
            Error bar sizes for the bars

        ecolor: all matplotlib color formats (without X11/xkcd), optional
            Color of the error bars

        capsize: float, optional
            Size of the error bar caps in pt

        hatch: str, optional
            The hatch pattern to use for filling the bars. Can be a string of characters that define the hatch pattern (e.g., '/', '\\', '|', '-', '+', 'x', '.', '*'). If not provided, no hatching is applied.

        hatch_color: ColorLike, optional
            The color of the hatch pattern. If not provided, the default color cycle is used.

        hatch_linewidth: float, optional
            The line width of the hatch pattern in points. If not provided, the default line width is used.

        hatch_distance: float, optional
            The distance between hatch lines in points. If not provided, the default distance is used.
        """

    def _common_bar(self, k: ArrayLike | float, v: ArrayLike | float, thickness: ArrayLike | float = 0.8, edge: ArrayLike | float = 0.0, group_offset: float = 0.0, align: Literal["center", "edge"] = "center", color: Optional[ColorLike] = None, c: Optional[ColorLike] = None, facecolor: Optional[ColorLike] = None, fc: Optional[ColorLike] = None, edgecolor: Optional[ColorLike] = None, ec: Optional[ColorLike] = None, linewidth: Optional[float] = None, lw: Optional[float] = None, tick_label: Optional[str | list[str]] = None, label: Optional[str] = None, xerr: Optional[ArrayLike] = None, yerr: Optional[ArrayLike] = None, ecolor: Optional[ColorLike] = None, capsize: Optional[float] = None, hatch: Optional[str] = None, hatch_color: Optional[ColorLike] = None, hatch_linewidth: Optional[float] = None, hatch_distance: Optional[float] = None) -> None: ...


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

    def axvline(self, x:float, ymin:float=0, ymax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., linestyle:Optional[str] = ..., linewidth:Optional[float] = ..., label:Optional[str] = ...) -> None:
        """
        Draw a vertical line to the selected axis at given x coordinate.
        
        Parameters
        ----------
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

    def axhline(self, y:float, xmin:float=0, xmax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., linestyle:Optional[str] = ..., linewidth:Optional[float] = ..., label:Optional[str] = ...) -> None:
        """
        Draw a horizontal line to the selected axis at given y coordinate.
        
        Parameters
        ----------
        y: float
            Y coordinate of the line(s)
        
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

    def axvspan(self, xmin:float, xmax:float, ymin:float=0, ymax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., label:Optional[str] = ..., hatch:Optional[str] = ..., hatch_color:Optional[ColorLike] = ..., hatch_linewidth:Optional[float] = ..., hatch_distance:Optional[float] = ...) -> None:
        """
        Draw a background vertical span to the selected axis between given x coordinates.

        Parameters
        ----------
        xmin, xmax: float
            X coordinates of the left and right end of the span
        
        ymin, ymax: float, optional
            Y relative coordinate of the lower and upper end of the span
        
        alpha: float, optional
            Opacity

        color or c: all matplotlib color formats (without X11/xkcd), optional
            color of line: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

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

    def axhspan(self, ymin:float, ymax:float, xmin:float=0, xmax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., label:Optional[str] = ..., hatch:Optional[str] = ..., hatch_color:Optional[ColorLike] = ..., hatch_linewidth:Optional[float] = ..., hatch_distance:Optional[float] = ...) -> None:
        """
        Draw a background horizontal span to the selected axis between given y coordinates.

        Parameters
        ----------
        ymin, ymax: float
            Y coordinates of the lower and upper end of the span
        
        xmin, xmax: float, optional
            X relative coordinate of the left and right end of the span
        
        alpha: float, optional
            Opacity

        color or c: all matplotlib color formats (without X11/xkcd), optional
            color of line: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

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
    def set_yticks(self, ticks: ArrayLike, labels: Optional[Sequence[str]] = ...) -> None: 
        """
        Set y-axis ticks and their labels.
        """
        ...
    def set_yticklabels(self, labels: Sequence[str]) -> None: 
        """
        Set y-axis tick labels.
        """
        ...
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
    def set(self, **kwargs) -> None:
        """
        Set parameter (lims, labels, ticks, ticklabels, title)
        """
        ...
    def _add_legend_entries(self) -> str: ...
    def _content_tex(self, filename: str) -> str: ...
    def _get_hard_range(self, which: Literal["xmin","xmax","ymin","ymax"]) -> Tuple[float,str]: ...
    def _get_range(self, which: Literal["xmin","xmax","ymin","ymax"]) -> Tuple[float, bool,str]: ...
    def _get_limit(self, which: Literal["xmin","xmax","ymin","ymax"]) -> Tuple[float,bool,str]: ...
    def _set_range(self, which: Literal["xmin","xmax","ymin","ymax"], value: Union[float, int]): ...
    def _num_points(self) -> list[int]: ...
    def _add_col(self, r: float, g: float, b: float) -> None: ...
    
class Axes(BaseAxes):
    def __init__(self, nrows: int, ncols: int, index: int, fig: Any, pol: bool) -> None: ...
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
    def imshow(self, *args: Any, cmap: Optional[str] = ..., **kwargs: Any) -> Tuple[Any, str, float, float]: 
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
    def set_xticks(self, ticks: ArrayLike, labels: Optional[Sequence[str]] = ...) -> None: 
        """
        Set x-axis ticks and their labels.
        """
        ...
    def set_xticklabels(self, labels: Sequence[str]) -> None: 
        """
        Set x-axis tick labels.
        """
        ...
    def twinx(self) -> "Secondary": 
        """
        Initialize secondary y-axis.
        """
        ...
    def set_facecolor(self, color: ColorLike) -> None:
        """
        Set axis background color.

        Parameters
        ----------
        color: all matplotlib color formats (without X11/xkcd)
            Background color of axis: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
        """
        ...
    def _export_imshow(self, *args: Any, **kwargs: Any) -> str: ...
    def _axis_options_string(self) -> str: ...
    def _margins(self) -> tuple[float, float, float, float]: ...
    def _get_row(self) -> int: ...
    def _get_col(self) -> int: ...
    def _get_nrows(self) -> int: ...
    def _get_ncols(self) -> int: ...
    def _get_defcol(self) -> int: ...
    def _show_colorbar(self, cbar: str, horizontal: bool = ...) -> None: ...
    def _get_index(self) -> int: ...
    def _to_tex(self, filename: str, single: bool) -> tuple[list[str], list[str]]: ...

    
class Secondary(BaseAxes):
    def __init__(self, primary: Axes) -> None: ...
    def _axis_options_string(self) -> str: ...
    def _padding(self) -> float: ...
    def _get_defcol(self) -> int: ...
    def _get_index(self) -> int: ...