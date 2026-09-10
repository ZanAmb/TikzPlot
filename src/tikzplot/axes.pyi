from typing import Any, Optional, Sequence, Tuple, Union, Literal
import numpy as np
from .colorbar import Colorbar
from .elements import Graph
from .pie import Pie

ArrayLike = Union[Sequence[float|int], np.ndarray]
ColorLike = Union[str, Sequence[float], Sequence[Sequence[float] | ArrayLike], np.ndarray, None]
LineStyle = Literal["-", "--", "-.", ":", "solid", "dashed", "dashdot", "none", ""]
MarkerStyle = Literal["o", "s", "^", "v", "x", "+", ".", "*", "None", ""]
FontSize = Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]
HatchStyle = Literal["/", "\\", "|", "-", "+", "x", ".", "*"]


class BaseAxes:   
    def plot(self, x: ArrayLike = ..., y: ArrayLike = ..., fmt: Optional[str] = ...,*, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label:Optional[str]=...) -> Graph:
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

    def scatter(self, x: ArrayLike = ..., y: ArrayLike = ..., fmt: Optional[str] = ..., *,alpha: float = 1.0, color: Optional[Union[Sequence[ColorLike], ColorLike]] = ..., c: Optional[ColorLike] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[Union[ArrayLike, float]] = ..., s: Optional[Union[ArrayLike, float]] = ...,  label:Optional[str]=..., cmap: Optional[Union[str, Colorbar]] = ..., vmin: Optional[float] = ..., vmax: Optional[float] = ...) -> Graph:
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
    def semilogy(self, x: ArrayLike = ..., y: ArrayLike = ..., base: Optional[float] = 10,  fmt: Optional[str] = ...,*, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label:Optional[str]=...) -> Graph:
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
    def errorbar(self, x: ArrayLike = ..., y: ArrayLike = ..., yerr: Optional[ArrayLike | float] = ..., xerr: Optional[ArrayLike | float] = ..., fmt: Optional[str] = ..., *, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label: Optional[str]= ..., ecolor: Optional[ColorLike] = ..., elinewidth: Optional[float] = ..., capsize: Optional[float] = ..., elinestyle: Optional[LineStyle] = ...) -> Graph:
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
             label:Optional[str]=...) -> Graph: 
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
        alpha: float = 1.0,
        color: Optional[ColorLike] = ...,
        c: Optional[ColorLike] = ...,
        label: Optional[str] = ...,
        hatch: Optional[str] = ...,
        hatch_color: Optional[ColorLike] = ...,
        hatch_linewidth: Optional[float] = ...,
        hatch_distance: Optional[float] = ...,
    ) -> Graph: 
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

    def text(self, x: float, y: float, s: str, alpha: float = 1, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., fontsize: Optional[FontSize] = ..., size: Optional[FontSize] = ..., backgroundcolor: Optional[ColorLike] = ..., horizontalalignment: Literal["left", "center", "right"] = "center", ha: Literal["left", "center", "right"] = "center", verticalalignment: Literal["bottom", "center", "top"] = "center", va: Literal["bottom", "center", "top"] = "center", rotation: float = 0, label: Optional[str] = ...) -> None:
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
        bins: int | ArrayLike = 10,
        *,
        weight: ArrayLike | None = None,
        density: bool = False,
        cumulative: bool = False,
        histtype: Literal["bar", "barstacked", "step", "stepfilled"] = "bar",
        orientation: Literal["horizontal","vertical"] = "vertical",
        rwidth: float | None = None,
        range: Tuple[float,float] | None = None,
        alpha: float = 1.0,
        color: ColorLike | Sequence[ColorLike] = ...,
        facecolor: ColorLike | Sequence[ColorLike] = ...,
        fc: ColorLike | Sequence[ColorLike] = ...,
        edgecolor: ColorLike | Sequence[ColorLike] = ...,
        ec: ColorLike | Sequence[ColorLike] = ...,
        align: Literal["left", "mid", "right"] = ...,
        stacked: bool = False,
        fill: bool = True,
        hatch: str = ...,
        hatch_color: ColorLike = ...,
        hatch_linewidth: float = ...,
        hatch_distance: float = ...,
        #**kwargs: Any
    ) -> Sequence[Graph]: 
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

        alpha: float, optional
            Opacity between 0 and 1.

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

    def bar(self, x: ArrayLike | float, height: ArrayLike | float, width: ArrayLike | float = 0.8, bottom: ArrayLike | float = 0.0, *, align: Literal["center", "edge"] = "center", alpha: Optional[float | Sequence[float]] = ..., color: Optional[ColorLike] = None, c: Optional[ColorLike] = None, facecolor: Optional[ColorLike] = None, fc: Optional[ColorLike] = None, edgecolor: Optional[ColorLike] = None, ec: Optional[ColorLike] = None, linewidth: Optional[float] = None, lw: Optional[float] = None, tick_label: Optional[str] = None, label: Optional[str] = None, xerr: Optional[ArrayLike] = None, yerr: Optional[ArrayLike] = None, ecolor: Optional[ColorLike] = None, capsize: Optional[float] = None, hatch: Optional[str] = None, hatch_color: Optional[ColorLike] = None, hatch_linewidth: Optional[float] = None, hatch_distance: Optional[float] = None) -> Graph:
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

        alpha: float or sequence of float, optional
            Opacity of the bars

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

    def barh(self, y: ArrayLike | float, width: ArrayLike | float, height: ArrayLike | float = 0.8, left: ArrayLike | float = 0.0, *, align: Literal["center", "edge"] = "center", alpha: Optional[float | Sequence[float]] = ..., color: Optional[ColorLike] = None, c: Optional[ColorLike] = None, facecolor: Optional[ColorLike] = None, fc: Optional[ColorLike] = None, edgecolor: Optional[ColorLike] = None, ec: Optional[ColorLike] = None, linewidth: Optional[float] = None, lw: Optional[float] = None, tick_label: Optional[str | list[str]] = None, label: Optional[str] = None, xerr: Optional[ArrayLike] = None, yerr: Optional[ArrayLike] = None, ecolor: Optional[ColorLike] = None, capsize: Optional[float] = None, hatch: Optional[str] = None, hatch_color: Optional[ColorLike] = None, hatch_linewidth: Optional[float] = None, hatch_distance: Optional[float] = None) -> Graph:
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

        alpha: float or sequence of float, optional
            Opacity of the bars

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

    def grouped_bar(self, heights: dict[Any, ArrayLike] | ArrayLike, positions: ArrayLike | None = None, tick_labels: Sequence[str] | None = None, labels: Sequence[str] | None = None, group_spacing: float = 1.5, bar_spacing: float = 0.0, orientation: Literal["vertical", "horizontal"] = "vertical", alpha: Optional[Sequence[float] | float] = ..., colors: Optional[Sequence[ColorLike] | ColorLike] = ..., edgecolor: Optional[Sequence[ColorLike] | ColorLike] = ..., ec: Optional[Sequence[ColorLike] | ColorLike] = ..., facecolor: Optional[Sequence[ColorLike] | ColorLike] = ..., fc: Optional[Sequence[ColorLike] | ColorLike] = ..., linewidth: Optional[Sequence[float] |float] = ..., lw: Optional[Sequence[float] | float] = ..., linestyles: Optional[Sequence[LineStyle] | LineStyle] = ..., ls: Optional[Sequence[LineStyle] | LineStyle] = ..., hatch: Optional[Sequence[str] | str] = ..., hatch_color: Optional[Sequence[ColorLike] | ColorLike] = ..., hatch_linewidth: Optional[Sequence[float] | float] = ..., hatch_distance: Optional[Sequence[float] | float] = ...) -> Sequence[Graph]:
        """
        Draw a grouped bar plot to the selected axis.

        Parameters
        ----------
        heights: dict or ArrayLike
            Heights of the bars. If a dict is provided, keys are used as group labels and values as bar heights.

        positions: ArrayLike, optional
            Positions of the groups. If None, groups are placed at integer positions starting from 0.

        tick_labels: sequence of str, optional
            Labels for the ticks on the axis. If None, existing axis labels are used.

        labels: sequence of str, optional
            Labels for the individual bars within each group. If None, no bar labels are added.

        group_spacing: float, optional
            Spacing between groups of bars in widths of a single bar. Default is 1.5.

        bar_spacing: float, optional
            Spacing between individual bars within a group in widths of a single bar. Default is 0.0.

        orientation: {"vertical", "horizontal"}, optional
            Orientation of the bars. Default is "vertical".

        alpha: sequence of float or single float, optional
            Opacity of the bars. If a single value is provided, it is used for all bars. If a sequence is provided, opacities are cycled through the bars.

        colors, edgecolor, ec, facecolor, fc: sequence of ColorLike or single ColorLike, optional
            Colors for the bars and edges. If a single color is provided, it is used for all bars. If a sequence is provided, colors are cycled through the bars.

        linewidth or lw: sequence of float or single float, optional
            Line widths for the edges of the bars. If a single value is provided, it is used for all bars. If a sequence is provided, line widths are cycled through the bars.

        linestyles or ls: sequence of LineStyle or single LineStyle, optional
            Line styles for the edges of the bars. If a single value is provided, it is used for all bars. If a sequence is provided, line styles are cycled through the bars.

        hatch: sequence of str or single str, optional
            Hatch patterns for the bars. If a single pattern is provided, it is used for all bars. If a sequence is provided, hatch patterns are cycled through the bars.

        hatch_color: sequence of ColorLike or single ColorLike, optional
            Colors for the hatch patterns. If a single color is provided, it is used for all bars. If a sequence is provided, colors are cycled through the bars.

        hatch_linewidth: sequence of float or single float, optional
            Line widths for the hatch patterns. If a single value is provided, it is used for all bars. If a sequence is provided, line widths are cycled through the bars.

        hatch_distance: sequence of float or single float, optional
            Distances between hatch lines. If a single value is provided, it is used for all bars. If a sequence is provided, distances are cycled through the bars.
        """

    def _common_bar(self, k: ArrayLike | float, v: ArrayLike | float, thickness: ArrayLike | float = 0.8, edge: ArrayLike | float = 0.0, group_offset: float = 0.0, align: Literal["center", "edge"] = "center", color: Optional[ColorLike] = None, c: Optional[ColorLike] = None, facecolor: Optional[ColorLike] = None, fc: Optional[ColorLike] = None, edgecolor: Optional[ColorLike] = None, ec: Optional[ColorLike] = None, linewidth: Optional[float] = None, lw: Optional[float] = None, tick_label: Optional[str | list[str]] = None, label: Optional[str] = None, xerr: Optional[ArrayLike] = None, yerr: Optional[ArrayLike] = None, ecolor: Optional[ColorLike] = None, capsize: Optional[float] = None, hatch: Optional[str] = None, hatch_color: Optional[ColorLike] = None, hatch_linewidth: Optional[float] = None, hatch_distance: Optional[float] = None) -> Graph:
        ...

    def bar_label(self, container: Graph, labels: Sequence[str|float|int] | None = None, *, alpha: Optional[float] = None, color: Optional[ColorLike] = None, c: Optional[ColorLike] = None, fontsize: Optional[FontSize | int] = None, padding: float | None = None, fmt: str = "%g", rotation: float | Literal["vertical", "horizontal"] = 0) -> None:
        """
        Attach labels to bars in a bar container.

        Parameters
        ----------
        container: Graph
            The element of bars (return of bar/barh/element of hist) to which the labels will be attached.

        labels: sequence of str, float, or int, optional
            The labels to attach to the bars. If None, the height of each bar will be used as the label, if [], no labels will be attached.
        
        alpha: float, optional
            Opacity of the text labels

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Color of the text labels: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

        fontsize: FontSize or int, optional
            Font size of the text labels

        padding: float, optional
            Padding between the bar and the label in points. If None, a default padding is used.

        fmt: str, optional
            Format string for the labels. Default is "%g".

        rotation: float or {"vertical", "horizontal"}, optional
            Rotation of the text labels. Default is 0 (horizontal).
        """
        ...

    def stackplot(self, x: ArrayLike, *args, baseline: Literal["zero", "sym", "wiggle", "weighted_wiggle"] = "zero", labels: Optional[Sequence[str]] = ..., colors: Optional[Sequence[ColorLike] | ColorLike] = ..., alpha: Optional[float|Sequence[float]] = ..., facecolor: Optional[Sequence[ColorLike] | ColorLike] = ..., edgecolor: Optional[Sequence[ColorLike] | ColorLike] = ..., linewidth: Optional[Sequence[float] | float] = ..., linestyle: Optional[Sequence[str] | str] = ..., hatch: Optional[Sequence[str] | str] = ..., hatch_color: Optional[Sequence[ColorLike] | ColorLike] = ..., hatch_linewidth: Optional[Sequence[float] | float] = ..., hatch_distance: Optional[Sequence[float] | float] = ...) -> Sequence[Graph]:
        """
        Draw a stack plot to the selected axis.

        Parameters
        ----------
        x: ArrayLike
            X coordinates of the data points

        *args: ArrayLike
            Y coordinates of the data points for each stack (together or as separate args).

        baseline: {"zero", "sym", "wiggle", "weighted_wiggle"}, optional
            Baseline method for the stack plot. Default is "zero".

        labels: sequence of str, optional
            Labels for each stack. If not provided, no labels are added.

        colors, facecolor, edgecolor: sequence of ColorLike or single ColorLike, optional
            Colors for the stacks. If a single color is provided, it is used for all stacks. If a sequence is provided, colors are cycled through the stacks.

        alpha: float or sequence of float, optional
            Opacity of the stacks. If a single value is provided, it is used for all stacks. If a sequence is provided, opacities are cycled through the stacks.

        linewidth or lw: sequence of float or single float, optional
            Line widths for the edges of the stacks. If a single value is provided, it is used for all stacks. If a sequence is provided, line widths are cycled through the stacks.

        linestyle or ls: sequence of str or single str, optional
            Line styles for the edges of the stacks. If a single value is provided, it is used for all stacks. If a sequence is provided, line styles are cycled through the stacks.

        hatch: sequence of str or single str, optional
            Hatch patterns for the stacks. If a single pattern is provided, it is used for all stacks. If a sequence is provided, hatch patterns are cycled through the stacks.

        hatch_color: sequence of ColorLike or single ColorLike, optional
            Colors for the hatch patterns. If a single color is provided, it is used for all stacks. If a sequence is provided, colors are cycled through the stacks.

        hatch_linewidth: sequence of float or single float, optional
            Line widths for the hatch patterns. If a single value is provided, it is used for all stacks. If a sequence is provided, line widths are cycled through the stacks.

        hatch_distance: sequence of float or single float, optional
            Distances between hatch lines. If a single value is provided, it is used for all stacks. If a sequence is provided, distances are cycled through the stacks.
        """
        ...
       

    def step(self, x: ArrayLike, y: ArrayLike, *args: Any, where: Literal["pre","post","mid"] = "pre", **kwargs: Any) -> Graph:
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

    def ecdf(self, x: ArrayLike, weights: Optional[ArrayLike] = None, *, complementary: bool = False, orientation: Literal["vertical", "horizontal"] = "vertical", compress: bool = True, fmt: Optional[str] = ..., alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ..., marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label:Optional[str]=...) -> Graph:
        """
        Draw an empirical cumulative distribution function (ECDF) plot to the selected axis.

        Parameters
        ----------
        x: ArrayLike
            Data points for which the ECDF is computed.

        weights: ArrayLike, optional
            Weights for the data points. If provided, the ECDF will be computed using these weights.

        complementary: bool, optional
            If True, plot the complementary ECDF (1 - ECDF). Default is False.

        orientation: {"vertical", "horizontal"}, optional
            Orientation of the ECDF plot. Default is "vertical".

        compress: bool, optional
            If True, compress the ECDF to remove duplicate x values. Default is True.

        fmt: str, optional
            Style format string for the plot.

        alpha: float, optional
            Opacity of the plot.

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Color of the line and markers.

        linestyle or ls: str, optional
            Line style for the ECDF plot.

        linewidth or lw: float, optional
            Line width in points for the ECDF plot.

        marker: str, optional
            Marker style for the data points in the ECDF plot.

        markersize or ms: float, optional
            Size of the markers in points.

        label: str, optional
            Legend entry for the ECDF plot.
        """
        ...

    def pie(self, x: ArrayLike, *, explode: Optional[ArrayLike] = None, labels: Optional[Sequence[str]] = None, colors: Optional[Sequence[ColorLike]] = None, autopct: Optional[str] = None, pctdistance: float = 0.6, labeldistance: float = 1.1, radius: float = 1.0, startangle: float = 0.0, counterclock: bool = True, wedgeprops: Optional[dict] = None, rotate_labels: bool = False, normalize: bool = True) -> Pie:
        """
        Draw a pie chart to the selected axis.

        Parameters
        ----------
        x: ArrayLike
            The wedge sizes. If not normalized, they will be normalized to sum to 1.

        explode: ArrayLike, optional
            If not None, is a sequence of fractions that specifies the fraction of the radius with which to offset each wedge.

        labels: sequence of str, optional
            A sequence of strings providing the labels for each wedge.

        colors: sequence of ColorLike, optional
            A sequence of colors for the wedges. If not provided, the default color cycle is used.

        autopct: str, optional
            A string or function used to label the wedges with their numeric value. If None (default), no labels are drawn.

        pctdistance: float, optional
            The ratio between the center of each pie slice and the start of the text generated by autopct. Default is 0.6.

        labeldistance: float, optional
            The radial distance at which the pie labels are drawn (relative to pie radius). Default is 1.1.

        radius: float, optional
            The radius of the pie chart in cm on paper. Default is 1.0.

        startangle: float, optional
            The starting angle of the pie chart in degrees. Default is 0.0.

        counterclock: bool, optional
            If True (default), draw wedges counterclockwise. If False, draw wedges clockwise.

        wedgeprops: dict, optional
            A dictionary of properties for the wedges, for now, only width (in cm) is supported, which allows to make donut or nested charts.

        rotate_labels: bool, optional
            If True, rotate each label to be parallel to its corresponding wedge. Default is False.

        normalize: bool, optional
            If True (default), normalize x so that it sums to 1.
        """
        ...

    def pie_label(self, container: Pie, labels: Sequence[str], *, distance: float = 0.6, rotate: bool = False) -> None:
        """
        Attach labels to wedges in a pie chart.

        Parameters
        ----------
        container: Pie
            The element of wedges (return of pie) to which the labels will be attached.

        labels: sequence of str
            The labels to attach to the wedges.

        distance: float, optional
            The radial distance at which the pie labels are drawn (relative to pie radius). Default is 0.6.

        rotate: bool, optional
            If True, rotate each label to be parallel to its corresponding wedge. Default is False.
        """
        ...

    def bxp(self, bxpstats: list[dict[str, Any]], positions: list[float|int]|None=None, *, widths:float|ArrayLike=0.5, orientation: Literal["vertical", "horizontal"]="vertical", showcaps:bool=True, showbox:bool=True, showfliers:bool=True, showmeans:bool=False, boxprops:dict[str, Any]|None=None, whiskerprops:dict[str, Any]|None=None, flierprops:dict[str, Any]|None=None, medianprops:dict[str, Any]|None=None, meanprops:dict[str, Any]|None=None, capwidths:float|ArrayLike|None=None, tex_settings:dict[str, Any] = {}) -> list[Graph]:
        """
        Draw a box-and-whisker plot to the selected axis.

        Parameters
        ----------
        bxpstats: list of dict
            A list of dictionaries containing the statistics for each boxplot. Each dictionary should contain the following keys:
                - 'med': The median value.
                - 'q1': The first quartile (25th percentile).
                - 'q3': The third quartile (75th percentile).
                - 'whislo': The lower whisker position.
                - 'whishi': The upper whisker position.
                - 'fliers': A list of outlier values.
                - 'mean': The mean value (optional).
        
        positions: list of float or int, optional
            The positions of the boxes on the axis. If None, boxes are placed at integer positions starting from 1.

        widths: float or ArrayLike, optional
            The width of the boxes. If a single float is provided, all boxes will have the same width. If an array is provided, each box can have a different width.

        orientation: {"vertical", "horizontal"}, optional
            The orientation of the boxplots. Default is "vertical".

        showcaps: bool, optional
            If True (default), draw the caps on the whiskers.

        showbox: bool, optional
            If True (default), draw the boxes.

        showfliers: bool, optional
            If True (default), draw the outliers.

        showmeans: bool, optional
            If True, draw the means. Default is False.

        boxprops: dict, optional
            A dictionary of properties for the boxes. Can include 'facecolor', 'edgecolor', 'linewidth', etc.

        whiskerprops: dict, optional
            A dictionary of properties for the whiskers. Can include 'color', 'linewidth', etc.

        flierprops: dict, optional
            A dictionary of properties for the fliers (outliers). Can include 'marker', 'color', 'markersize', etc.
        
        medianprops: dict, optional
            A dictionary of properties for the median line. Can include 'color', 'linewidth', etc.

        meanprops: dict, optional
            A dictionary of properties for the mean marker. Can include 'marker', other properties like color are not yet supported.

        capwidths: float or ArrayLike, optional
            The width of the caps on the whiskers. If a single float is provided, all caps will have the same width. If an array is provided, each cap can have a different width.

        tex_settings: dict, optional
            A dictionary of direct settings for TeX rendering.
        """
        ...

    def boxplot(self, x: ArrayLike | Sequence[Sequence[float|int]], *, sym: str|None=None, orientation:Literal["vertical", "horizontal"]="vertical", whis:float=1.5, positions: ArrayLike | None=None, widths: float | ArrayLike=0.5, usermedians: ArrayLike | None=None, showmeans:bool=False, showcaps:bool=True, showbox:bool=True, showfliers:bool=True, boxprops:dict[str, Any]|None=None, tick_labels:dict[str, Any]|None=None, flierprops:dict[str, Any]|None=None, medianprops:dict[str, Any]|None=None, meanprops:dict[str, Any]|None=None, whiskerprops:dict[str, Any]|None=None, manage_ticks:bool=True, capwidths:float | ArrayLike | None=None, autorange:bool=True) -> list[Graph]:
        """
        Draw a box-and-whisker plot to the selected axis.

        Parameters
        ----------
        x: ArrayLike or sequence of sequences
            The data to be plotted. Can be a single array or a sequence of arrays for multiple boxplots.

        sym: str or None, optional
            The symbol for outliers. If None, no outliers are drawn.

        orientation: {"vertical", "horizontal"}, optional
            The orientation of the boxplots. Default is "vertical".

        whis: float, optional
            The whisker length as a proportion of the interquartile range. Default is 1.5.

        positions: ArrayLike, optional
            The positions of the boxes on the axis. If None, boxes are placed at integer positions starting from 1.

        widths: float or ArrayLike, optional
            The width of the boxes. If a single float is provided, all boxes will have the same width. If an array is provided, each box can have a different width.

        usermedians: ArrayLike, optional
            User-defined median values for the boxes. If provided, these values will be used instead of computing the medians from the data.

        showmeans: bool, optional
            If True, draw the means. Default is False.

        showcaps: bool, optional
            If True (default), draw the caps on the whiskers.

        showbox: bool, optional
            If True (default), draw the boxes.

        showfliers: bool, optional
            If True (default), draw the outliers.

        boxprops: dict, optional
            A dictionary of properties for the boxes. Can include 'facecolor', 'edgecolor', 'linewidth', etc.

        tick_labels: dict, optional
            A dictionary of properties for the tick labels. Can include 'fontsize', 'rotation', etc.

        flierprops: dict, optional
            A dictionary of properties for the fliers (outliers). Can include 'marker', 'color', 'markersize', etc.
        
        medianprops: dict, optional
            A dictionary of properties for the median line. Can include 'color', 'linewidth', etc.

        meanprops: dict, optional
            A dictionary of properties for the mean marker. Can include 'marker', other properties like color are not yet supported.

        whiskerprops: dict, optional
            A dictionary of properties for the whiskers. Can include 'color', 'linewidth', etc.

        manage_ticks: bool, optional
            If True (default), automatically manage the ticks on the axis (if tick_labels is not None, ticks will be renamed accordingly).

        capwidths: float or ArrayLike, optional
            The width of the caps on the whiskers. If a single float is provided, all caps will have the same width. If an array is provided, each cap can have a different width.

        autorange: bool, optional
            If True (default), automatically adjust the axis limits to fit the boxplots.
        """
        ...

    def violin(self, vpstats: list[dict[str, Any]], positions:ArrayLike|None=None, *, orientation:Literal["vertical", "horizontal"]="vertical", widths:float|ArrayLike=0.5, showmeans:bool=False, showextrema:bool=True, showmedians:bool=False, side:Literal["low", "high", "both"]="both", facecolor:ColorLike|Sequence[ColorLike]|None=None, linecolor:ColorLike|Sequence[ColorLike]|None=None) -> list[Graph]:
        """
        Draw a violin plot to the selected axis.

        Parameters
        ----------
        vpstats: list of dict
            A list of dictionaries containing the statistics for each violin plot. Each dictionary may contain the following keys:
                - 'coords': The coordinates of the violin shape (mandatory).
                - 'vals': The values corresponding to the coordinates (mandatory).
                - 'mean': The mean value (optional).
                - 'median': The median value (optional).
                - 'min': The minimum value (optional).
                - 'max': The maximum value (optional).
                - 'qantiles': A list of quantile values (optional).
        
        positions: list of float or int, optional
            The positions of the violins on the axis. If None, violins are placed at integer positions starting from 1.

        widths: float or list of float, optional
            The width of the violins. If a single float is provided, all violins will have the same width. If a list is provided, each violin can have a different width.

        orientation: {"vertical", "horizontal"}, optional
            The orientation of the violin plots. Default is "vertical".

        showmeans: bool, optional
            If True, draw the means. Default is False.

        showextrema: bool, optional
            If True (default), draw the extrema (min and max) of the violins.

        showmedians: bool, optional
            If True, draw the medians of the violins. Default is False.

        side: {"low", "high", "both"}, optional
            Which side of the violin to draw. Default is "both".

        facecolor: ColorLike or sequence of ColorLike, optional
            The fill color of the violins. If a single color is provided, it is used for all violins. If a sequence is provided, colors are cycled through the violins.

        linecolor: ColorLike or sequence of ColorLike, optional
            The edge color of the violins. If a single color is provided, it is used for all violins. If a sequence is provided, colors are cycled through the violins.
        """
        ...

    def violinplot(self, dataset: ArrayLike | Sequence[Sequence[float|int]], positions: ArrayLike | None =None, *, orientation:Literal["vertical", "horizontal"]="vertical", widths:float | ArrayLike=0.5, showmeans:bool=False, showextrema:bool=True, showmedians:bool=False, quantiles: Sequence[Sequence[int|float]|None]|None=None, points:int=100, bw_method:Literal["scott", "silverman"]="scott", side:Literal["low", "high", "both"]="both", facecolor:ColorLike|Sequence[ColorLike]|None=None, linecolor:ColorLike|Sequence[ColorLike]|None=None) -> Sequence[Graph]:
        """
        Draw a violin plot to the selected axis.

        Parameters
        ----------
        dataset: ArrayLike or sequence of sequences
            The data to be plotted. Can be a single array or a sequence of arrays for multiple violin plots.

        positions: ArrayLike, optional
            The positions of the violins on the axis. If None, violins are placed at integer positions starting from 1.

        widths: float or ArrayLike, optional
            The width of the violins. If a single float is provided, all violins will have the same width. If an array is provided, each violin can have a different width.

        orientation: {"vertical", "horizontal"}, optional
            The orientation of the violin plots. Default is "vertical".

        showmeans: bool, optional
            If True, draw the means. Default is False.

        showextrema: bool, optional
            If True (default), draw the extrema (min and max) of the violins.

        showmedians: bool, optional
            If True, draw the medians of the violins. Default is False.

        quantiles: sequence of sequences or None, optional
            A sequence of quantile values for each violin. If None, no quantiles are drawn. Note that the length of sequence must match the number of violins, and each inner sequence may contain the quantile values for the corresponding violin or None.

        points: int, optional
            The number of points to use for estimating the kernel density. Default is 100.

        bw_method: {"scott", "silverman"}, optional
            The method to use for bandwidth selection in kernel density estimation. Default is "scott".

        side: {"low", "high", "both"}, optional
            Which side of the violin to draw. Default is "both".

        facecolor: ColorLike or sequence of ColorLike, optional
            The fill color of the violins. If a single color is provided, it is used for all violins. If a sequence is provided, colors are cycled through the violins.

        linecolor: ColorLike or sequence of ColorLike, optional
            The edge color of the violins. If a single color is provided, it is used for all violins. If a sequence is provided, colors are cycled through the violins.
        """
        ...

    def axvline(self, x:float, ymin:float=0, ymax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., linestyle:Optional[str] = ..., linewidth:Optional[float] = ..., label:Optional[str] = ...) -> Graph:
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

    def axhline(self, y:float, xmin:float=0, xmax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., linestyle:Optional[str] = ..., linewidth:Optional[float] = ..., label:Optional[str] = ...) -> Graph:
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

    def axvspan(self, xmin:float, xmax:float, ymin:float=0, ymax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., label:Optional[str] = ..., hatch:Optional[str] = ..., hatch_color:Optional[ColorLike] = ..., hatch_linewidth:Optional[float] = ..., hatch_distance:Optional[float] = ...) -> Graph:
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

    def axhspan(self, ymin:float, ymax:float, xmin:float=0, xmax:float=1, alpha:Optional[float] = ..., color:Optional[ColorLike] = ..., label:Optional[str] = ..., hatch:Optional[str] = ..., hatch_color:Optional[ColorLike] = ..., hatch_linewidth:Optional[float] = ..., hatch_distance:Optional[float] = ...) -> Graph:
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

    def magnify(self, x_p: float, y_p: float, x_m: float, y_m: float, zoom: float, size: float, **kwargs) -> None:
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
    
    def set_ylabel(self, label: str, fontsize: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., loc: Literal["top", "center", "bottom"] = ..., rotate: Literal["vertical", "horizontal"] = ...) -> None: 
        """
        Set y-axis label.

        Parameters
        ----------
        label: str
            Label text

        fontsize: float, optional
            Font size of label

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Color of label: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

        loc: {"top", "center", "bottom"}, optional
            Location of label, default center

        rotate: {"vertical", "horizontal"}, optional
            Rotation of label, default vertical
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
    def set_yticks(self, ticks: ArrayLike, labels: Optional[Sequence[str]] = ..., fontsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...) -> None: 
        """
        Set y-axis ticks and their labels.

        Parameters
        ----------
        ticks: ArrayLike
            Tick positions

        labels: sequence of str, optional
            Tick labels, if not provided, the tick positions are used as labels

        fontsize: FontSize or int, optional
            Font size of tick labels

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Color of tick labels: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
        """
        ...
    def set_yticklabels(self, labels: Sequence[str], fontsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...) -> None: 
        """
        Set y-axis tick labels.

        Parameters
        ----------
        labels: sequence of str
            Tick labels

        fontsize: FontSize or int, optional
            Font size of tick labels

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Color of tick labels: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
        """
        ...

    def tick_params(self, axis: Literal["x", "y", "both"] = "both", color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., labelcolor: Optional[ColorLike] = ..., labelsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., direction: Optional[Literal["in", "out", "inout"]] = "in", top: Optional[bool] = True, bottom: Optional[bool] = True, left: Optional[bool] = True, right: Optional[bool] = True, labelbottom: Optional[bool] = True, labeltop: Optional[bool] = True) -> None:
        """
        Set tick parameters.

        Parameters
        ----------
        axis: {"x", "y", "both"}, optional
            Axis to apply the parameters to, default "both"

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Color of ticks and tick labels: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

        labelcolor: all matplotlib color formats (without X11/xkcd), optional
            Color of tick labels: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

        labelsize: FontSize or int, optional
            Font size of tick labels

        direction: {"in", "out", "inout"}, optional
            Direction of ticks, default "in"

        top, bottom, left, right: bool, optional
            Whether to draw ticks on the respective side of the axis, default True for all sides

        labelbottom, labeltop: bool, optional
            Available to turn off tick labels on left(y)/bottom(x) axis
        """
        ...
        
    def legend(self, *args: Any, loc: Optional[Union[int,str,Tuple[float,float]]] = ..., facecolor: Optional[ColorLike] = ..., edgecolor: Optional[ColorLike] = ..., labelcolor: Optional[ColorLike] = ..., frameon: Optional[bool] = ..., anchor: Optional[Literal["north", "south", "east", "west", "center", "north west", "north east", "south west", "south east"]] = ..., fontsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., ncols: Optional[int] = 1) -> None:
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
    def _update_axis_options(self, k: str, v: dict | str) -> None: ...
    def _not_hidable(self) -> None: ...
    
class Axes(BaseAxes):
    def __init__(self, nrows: int, ncols: int, index: int, fig: Any, pol: bool) -> None: ...
    def loglog(self, x: ArrayLike = ..., y: ArrayLike = ..., base: Optional[float] = 10,  fmt: Optional[str] = ...,*, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...) -> Graph:
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
    def semilogx(self, x: ArrayLike = ..., y: ArrayLike = ..., base: Optional[float] = 10,  fmt: Optional[str] = ...,*, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...) -> Graph:
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
    def set_xlabel(self, label: str, fontsize: Optional[float|FontSize] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., loc: Optional[Literal["left", "center", "right"]] = ...) -> None: 
        """
        Set x-axis label.

        Parameters
        ----------
        label: str
            Label text

        fontsize: FontSize or float, optional
            Font size of the label

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Text color: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

        loc: {"left", "center", "right"}, optional
            Label location, default "center"
        """
        ...
    def set_title(self, title: str, fontsize: Optional[float|FontSize] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., loc: Optional[Literal["left", "center", "right"]] = ...) -> None: 
        """
        Set plot title.

        Parameters
        ----------
        title: str
            Title text

        fontsize: FontSize or float, optional
            Font size of the title

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Text color: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible

        loc: {"left", "center", "right"}, optional
            Title location, default "center"
        """
        ...
    def grid(self, visible: bool = True, which: Literal["major","minor","both"] = "major", alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...) -> None: 
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
        ...
    def set_minorticks_num(self, num: int) -> None:
        """
        Set number of minor ticks between major ticks.
        
        Parameters
        ----------
        num: int
            Number of minor ticks between major ticks.
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
    def set_xticks(self, ticks: ArrayLike, labels: Optional[Sequence[str]] = ..., fontsize: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...) -> None: 
        """
        Set x-axis ticks and their labels.

        Parameters
        ----------
        ticks: ArrayLike
            Positions of the ticks on the x-axis.

        labels: sequence of str, optional
            Labels for the ticks. If not provided, the tick positions will be used as labels.

        fontsize: float, optional
            Font size of the tick labels.

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Color of the tick labels: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
        """
        ...
    def set_xticklabels(self, labels: Sequence[str], fontsize: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...) -> None: 
        """
        Set x-axis tick labels.

        Parameters
        ----------
        labels: sequence of str
            Labels for the ticks.

        fontsize: float, optional
            Font size of the tick labels.

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Color of the tick labels: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default cycle ("CX", X int), none for invisible
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
    def inset_axes(self, position: Literal["above", "below", "left", "right"], relsize: float = 1.0, sharex: bool = False, sharey: bool = False) -> Axes:
        """
        Create an inset axis within the current axis. This method is implemented a bit different than matplotlib's.

        Parameters
        ----------
        position: {"above", "below", "left", "right"}
            Position of the inset axis relative to the current axis.

        relsize: float, optional
            Relative size of the inset axis compared to the current axis (height if insetting above/below or width if insetting left/right). Default is 1.0

        sharex, sharey: bool, optional
            If True, the inset axis will share the x-axis or y-axis with the current axis. If the current axis was initialized using subplots with shared axes this will be respected (if in row/column/etc as set). Default is False.
        """
        ...
    
    def _export_imshow(self, *args: Any, **kwargs: Any) -> str: ...
    def _axis_options_string(self) -> str: ...
    def _parse_entry(self, k: str, v: Any) -> str: ...
    def _margins(self) -> tuple[float, float, float, float]: ...
    def _simulate_margins(self) -> tuple[float, float, float, float, float, float]: ...
    def _get_row(self) -> int: ...
    def _get_col(self) -> int: ...
    def _update_size(self, w: float|None, h: float|None) -> None: ...
    def _get_nrows(self) -> int: ...
    def _get_ncols(self) -> int: ...
    def _get_defcol(self, index: int) -> int: ...
    def _show_colorbar(self, cbar: str, horizontal: bool = ...) -> None: ...
    def _get_index(self) -> int: ...
    def _to_tex(self, filename: str, single: bool) -> tuple[list[str], list[str]]: ...
    def _new_pos(self, nrows: int, ncols: int, index: int) -> None: ...
    def _style_defaults(self) -> None: ...
    def _extend_axis(self, width: float, height: float) -> None: ...
    def _update_placeholder_size(self, width: float, height: float) -> None: ...

    
class Secondary(BaseAxes):
    def __init__(self, primary: Axes) -> None: ...
    def _axis_options_string(self) -> str: ...
    def _padding(self) -> float: ...
    def _get_defcol(self, index: int) -> int: ...
    def _get_index(self) -> int: ...