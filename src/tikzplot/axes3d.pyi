from __future__ import annotations

from typing import Any, Optional, Union, Sequence, Tuple, Literal

import numpy as np
from tikzplot.config import TikzConfig

from .colorbar import Colorbar
from .elements import Graph3

ArrayLike = np.ndarray | list[float] | tuple[float, ...]
ColorLike = Union[str, Sequence[float], Sequence[Sequence[float] | ArrayLike], np.ndarray, None]
FontSize = Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]
LineStyle = Literal["-", "--", "-.", ":", "solid", "dashed", "dashdot", "none", ""]
MarkerStyle = Literal["o", "s", "^", "v", "x", "+", ".", "*", "None", ""]

class Axes3:
    def __init__(self, nrows: int, ncols: int, index: int, fig: Any) -> None: ...
    def plot(self, xs: Union[ArrayLike, float, int], ys: Union[ArrayLike, float, int], zs: Union[ArrayLike, float, int], zdir: Literal["x", "y", "z"] = "z", fmt: Optional[str] = ...,*, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,
             linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float]= ..., lw: Optional[float] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ...,  label:Optional[str]=...) -> Graph3:
        """
        Draw a general plot to the selected axis.

        Parameters
        ----------
        x,y,z : ArrayLike or float
            Datapoints

        zdir: {"x", "y", "z"}, optional
            Direction to use as z-axis. Default is "z"

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
    def scatter(self, xs: Union[ArrayLike, float, int], ys: Union[ArrayLike, float, int], zs: Union[ArrayLike, float, int] = ..., zdir: Literal["x", "y", "z"] = "z", fmt: Optional[str] = ..., *,alpha: float = 1.0, color: Optional[Union[Sequence[ColorLike], ColorLike]] = ..., c: Optional[ColorLike] = ...,
             marker: Optional[MarkerStyle] = ..., markersize: Optional[Union[ArrayLike, float]] = ..., s: Optional[Union[ArrayLike, float]] = ...,  label:Optional[str]=..., cmap: Optional[Union[str, Colorbar]] = ..., vmin: Optional[float] = ..., vmax: Optional[float] = ...) -> Graph3:
        """
        Draw a scatter plot to the selected axis.
        
        Parameters
        ----------
        x,y,z : ArrayLike or float
            Datapoints

        zdir: {"x", "y", "z"}, optional
            Direction to use as z-axis. Default is "z"

        fmt: str, optional
            Style

        alpha: float, optional
            Opacity

        color or c: array like or single: all matplotlib color formats (without X11/xkcd) or float for 
        colormap, optional
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
    def plot_surface(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float] = ..., lw: Optional[float] = ..., label: Optional[str] = ...) -> Graph3: 
        """
        Draw a surface plot to the selected axis.

        Parameters
        ----------
        X, Y, Z : array-like
            The data to plot.
        alpha : float, optional
            The transparency of the surface.
        color, c : color-like, optional
            The color of the surface.
        linestyle, ls : str, optional
            The style of the lines.
        linewidth, lw : float, optional
            The width of the lines.
        label : str, optional
            The label for the legend.
        """
        ...
    def plot_wireframe(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float] = ..., lw: Optional[float] = ..., label: Optional[str] = ...) -> Graph3: 
        """
        Draw a wireframe plot to the selected axis.

        Parameters
        ----------
        X, Y, Z : array-like
            The data to plot.
        alpha : float, optional
            The transparency of the surface.
        color, c : color-like, optional
            The color of the surface.
        linestyle, ls : str, optional
            The style of the lines.
        linewidth, lw : float, optional
            The width of the lines.
        label : str, optional
            The label for the legend.
        """
        ...
    def errorbar(self, x: Union[ArrayLike, float, int], y: Union[ArrayLike, float, int], z: Union[ArrayLike, float, int], zerr: Optional[Union[ArrayLike, float, int] | float] = ..., yerr: Optional[Union[ArrayLike, float, int] | float] = ..., xerr: Optional[Union[ArrayLike, float, int] | float] = ..., alpha: float = 1.0, fmt: Optional[str] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., linestyle: Optional[LineStyle] = ..., ls: Optional[LineStyle] = ..., linewidth: Optional[float] = ..., lw: Optional[float] = ..., marker: Optional[MarkerStyle] = ..., markersize: Optional[float] = ..., ms: Optional[float] = ..., label: Optional[str] = ...) -> Graph3:
        """
        Draw a plot with errorbars to the selected axis.

        Parameters
        ----------
        x,y,z : ArrayLike or float
            Datapoints

        zerr, yerr, xerr : ArrayLike or float, optional
            Error values for the corresponding axes. Can be a single value or an array of the same length (with single or double values) as x, y, z.

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
    def fill_between(self, x1: Union[ArrayLike, float, int], y1: Union[ArrayLike, float, int], z1: Union[ArrayLike, float, int], x2: Union[ArrayLike, float, int], y2: Union[ArrayLike, float, int], z2: Union[ArrayLike, float, int], *, alpha: float = 1.0, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...,label: Optional[str] = ..., hatch: Optional[str] = ..., hatch_color: Optional[ColorLike] = ..., hatch_linewidth: Optional[float] = ..., hatch_distance: Optional[float] = ...,
        ) -> Graph3: 
            """
            Fill space between two plots.
    
            Parameters
            ----------
            x1,y1,z1,x2,y2,z2 : ArrayLike or float
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
    def bar3d(self, x: Union[ArrayLike, float, int], y: Union[ArrayLike, float, int], z: Union[ArrayLike, float, int], dx: Union[ArrayLike, float, int], dy: Union[ArrayLike, float, int], dz: Union[ArrayLike, float, int], color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., shade: bool = True, lightsources: Optional[Tuple[int | float, int | float]] = (315, 45), edgecolor: Optional[ColorLike] = ..., ec: Optional[ColorLike] = ..., label: Optional[str] = ...) -> Graph3:
        """
        Draw a 3D bar plot.

        Parameters
        ----------
        x, y, z : array-like or single values
            The coordinates of the anchor point of the bars.
        dx, dy, dz : array-like or single values
            The dimensions of the bars.
        color, c : color-like, optional
            The color of the bars. If not specified, a default color will be used.
        shade : bool, default True
            Whether to shade the bars to give a 3D effect.
        lightsources : tuple of two floats, optional
            The azimuth and elevation angles of the light source for shading. Default is (315, 45).
        edgecolor, ec : color-like, optional
            The color of the edges of the bars. If not specified, no edges will be drawn.
        label : str, optional
            The label for the bars in the legend.
        """
        ...
    def text(self, x: float, y: float, z: float, s: str, alpha: float = 1, color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., fontsize: Optional[FontSize] = ..., size: Optional[FontSize] = ..., backgroundcolor: Optional[ColorLike] = ..., horizontalalignment: Literal["left", "center", "right"] = "center", ha: Literal["left", "center", "right"] = "center", verticalalignment: Literal["bottom", "center", "top"] = "center", va: Literal["bottom", "center", "top"] = "center", rotation: float = 0, label: Optional[str] = ...) -> None:
        """
        Add text to the selected axis.

        Parameters
        ----------
        x,y,z: float
            Text position in axis coordinates

        s: str
            Text content (LaTeX format)

        color or c: all matplotlib color formats (without X11/xkcd), optional
            Text color: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str), name (str), default  cycle ("CX", X int), none for invisible

        fontsize or size: FontSize, optional
            Font size

        on_top: bool, optional
            Draw text on top of other elements (True by default)

        backgroundcolor: all matplotlib color formats (without X11/xkcd), optional
            Background color of text box: RGB/RGBA (tuple), HEX (str), grayscale (float), single-char (str),    name (str), default cycle ("CX", X int), none for invisible

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
    def set_xlabel(self, label: str, fontsize: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., loc: Literal["top", "center", "bottom"] = ..., rotate: Literal["vertical", "horizontal"] = ...) -> None:
        """
        Set x-axis label.

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
    def set_zlabel(self, label: str, fontsize: Optional[float] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., loc: Literal["top", "center", "bottom"] = ..., rotate: Literal["vertical", "horizontal"] = ...) -> None: 
        """
        Set z-axis label.

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
    def set_xlim(self, *args: Any, left: Optional[float] = ..., right: Optional[float] = ...) -> None: 
        """
        Set x-axis limit(-s). Set as tuple or as kwargs (left, right).

        """
        ...
    def set_ylim(self, *args: Any, bottom: Optional[float] = ..., top: Optional[float] = ...) -> None: 
        """
        Set y-axis limit(-s). Set as tuple or as kwargs (top, bottom).

        """
        ...
    def set_zlim(self, *args: Any, bottom: Optional[float] = ..., top: Optional[float] = ...) -> None: 
        """
        Set z-axis limit(-s). Set as tuple or as kwargs (top, bottom).

        """
        ...
    def set_xscale(self, *args: Any, base: Optional[float] = ...) -> None:
        """
        Set x-axis scale (to log).
        """
        ...
    def set_yscale(self, *args: Any, base: Optional[float] = ...) -> None:
        """
        Set y-axis scale (to log).
        """
        ...
    def set_zscale(self, *args: Any, base: Optional[float] = ...) -> None:
        """
        Set z-axis scale (to log).
        """
        ...
    def set_xticks(self, ticks: ArrayLike, labels: Optional[Sequence[str]] = ..., fontsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...) -> None: 
        """
        Set x-axis ticks and their labels.

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
    def set_zticks(self, ticks: ArrayLike, labels: Optional[Sequence[str]] = ..., fontsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...) -> None: 
        """
        Set z-axis ticks and their labels.

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
    def set_xticklabels(self, labels: Sequence[str], fontsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...) -> None: 
        """
        Set x-axis tick labels.

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
    def set_zticklabels(self, labels: Sequence[str], fontsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ...) -> None: 
        """
        Set z-axis tick labels.

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
    def view_init(self, elev: Optional[float] = TikzConfig.DEFAULT_3D_ELEV, azim: Optional[float] = TikzConfig.DEFAULT_3D_AZIM, roll: Optional[float] = TikzConfig.DEFAULT_3D_ROLL) -> None: 
        """
        Set the elevation and azimuthal angles of the 3D plot view. Roll is not yet supported.

        Parameters
        ----------
        elev, azim, roll: float, optional
            Angle in degrees, roll not yet supported. Default values are taken from TikzConfig.DEFAULT_3D_ELEV, TikzConfig.DEFAULT_3D_AZIM, TikzConfig.DEFAULT_3D_ROLL.
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
    def set(self, **kwargs) -> None:
        """
        Set parameter (lims, labels, ticks, ticklabels, title)
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
    def tick_params(self, axis: Literal["x", "y", "z", "both"] = "both", color: Optional[ColorLike] = ..., c: Optional[ColorLike] = ..., labelcolor: Optional[ColorLike] = ..., labelsize: Optional[Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"] | int] = ..., direction: Optional[Literal["in", "out", "inout"]] = "in", top: Optional[bool] = True, bottom: Optional[bool] = True, left: Optional[bool] = True, right: Optional[bool] = True) -> None:
        """
        Set tick parameters.

        Parameters
        ----------
        axis: {"x", "y", "z", "both"}, optional
            Axis to apply the parameters to, default "both". "both" acts as ALL.

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
        """
        ...

    def _add_legend_entries(self) -> str: ...
    def _content_tex(self, filename: str) -> str: ...
    def _get_hard_range(self, which: Literal["xmin","xmax","ymin","ymax"]) -> Tuple[float,str]: ...
    def _get_range(self, which: Literal["xmin","xmax","ymin","ymax"]) -> Tuple[float, bool,str]: ...
    def _set_range(self, which: Literal["xmin","xmax","ymin","ymax"], value: Union[float, int]): ...
    def _num_points(self) -> list[int]: ...
    def _add_col(self, r: float, g: float, b: float) -> None: ...
    def _update_size(self, w: float|None, h: float|None) -> None: ...
    def _update_axis_options(self, k: str, v: dict | str) -> None: ...
    def _axis_options_string(self) -> str: ...
    def _parse_entry(self, k: str, v: Any) -> str: ...
    def _margins(self) -> tuple[float, float, float, float]: ...
    def _simulate_margins(self) -> tuple[float, float, float, float, float, float]: ...
    def _get_row(self) -> int: ...
    def _get_col(self) -> int: ...
    def _get_nrows(self) -> int: ...
    def _get_ncols(self) -> int: ...
    def _get_defcol(self, index: int) -> int: ...
    def _show_colorbar(self, cbar: str, horizontal: bool = ...) -> None: ...
    def _get_index(self) -> int: ...
    def _to_tex(self, filename: str, single: bool) -> tuple[list[str], list[str]]: ...
