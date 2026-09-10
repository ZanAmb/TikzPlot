from __future__ import annotations

import numpy as np
from typing import Optional, Any
from typing_extensions import Literal, Sequence, overload, Union

from tikzplot.styles import Styles

from .axes import Axes
from .axes3d import Axes3
from .config import TikzConfig

ShareOptions = Optional[bool] | Literal["row", "col", "all", "none"]

class Figure:
    def __init__(self, style: Styles) -> None: ...
    @overload
    def add_subplot(
        self,
        *args,
        sharex: Optional[ShareOptions] = ...,
        sharey: Optional[ShareOptions] = ...,
        projection: Literal["3d"],
        polar: Optional[bool] = ...,
    ) -> Axes3: ...
    @overload
    def add_subplot(
        self,
        *args,
        sharex: Optional[ShareOptions] = None,
        sharey: Optional[ShareOptions] = None,
        projection: Optional[Literal["polar"]] = None,
        polar: Optional[bool] = False,
    ) -> Axes:  
        ...
        """
        Add subplot axis.

        Parameters
        ----------
        args: int or (int, int, int)
            Number of rows, columns and index (in a single int or 3 separate).

        sharex, sharey: bool or "row" or "col" or "all" or "none", optional
            Share x or y axes with other subplots.

        projection: None, "polar", "3d", optional
            None results in normal 2D.
        
        polar: bool, optional
            Use polar projection for axis.
        """
        ...

    def subplots(
        self,
        nrows: int = 1,
        ncols: int = 1,
        sharex: Optional[ShareOptions] = None,
        sharey: Optional[ShareOptions] = None,
        subplot_kw: Optional[dict] = None,
        figsize: Optional[tuple[float, float]] = None,
    ) -> Any:
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

        subplot_kw : dict, optional
            Additional keyword arguments for subplot creation (currently supported: projection).

        figsize: tuple of 2 floats, optional
            Figure size in inches (width, height).
        """
        ...

    def subplot_mosaic(self, mosaic: str | list[list[str]], *, sharex: bool = False, sharey: bool = False, width_ratios: Optional[Sequence[float]] = None, height_ratios: Optional[Sequence[float]] = None, empty_sentinel: str = ".", figsize: Optional[tuple[float, float]] = None) ->  dict[str, Any]:
        """
        Create a figure and a set of subplots arranged in a mosaic layout.

        Parameters
        ----------
        mosaic : str or list of lists of str
            A string or 2D list representing the layout of the subplots. Each unique character or string represents a subplot.

        sharex, sharey : bool, optional
            Specify if row, column or all subplots should share x or y axis.

        width_ratios : list of float, optional
            Ratios for the widths of the columns. Must match the number of columns.

        height_ratios : list of float, optional
            Ratios for the heights of the rows. Must match the number of rows.

        empty_sentinel : str, optional
            Character to represent empty spaces in the mosaic layout.

        figsize : tuple of 2 floats, optional
            Figure size in inches (width, height).

        Returns
        -------
        axs : dict
            A dictionary mapping subplot names to Axes objects.
        """
        ...

    def _inset(self, ax: Axes, position: str, relsize: float = 1, sharex: bool = False, sharey: bool = False) -> Axes: ...

    def _add_subplots(self, nrows:int, ncols:int, sharex:Optional[ShareOptions], sharey:Optional[ShareOptions], subplot_kw:Optional[dict]) -> Sequence[Axes]:
        """
        Add multiple subplots to figure.
        Parameters
        ----------
        nrows, ncols: int
            Number of rows and columns of subplots.

        sharex, sharey: bool or "row" or "col" or "all" or "none", optional
            Share x or y axis between subplots.

        subplot_kw: dict, optional
            Additional keyword arguments for subplot creation.
        """
        ...
    def set_size_inches(self, *args) -> None: 
        """
        Set figure size (w,h).
        """
        ...

    def delaxes(self, ax: Axes) -> None:
        """
        Delete axis from figure.
        """
        ...

    def _compute_group_spacing(self) -> None: ...
    def _get_spacing(self, row: int, col: int) -> float: ...
    def _charcode(self, n: int) -> str: ...
    def _next_limname(self, which: str, value: float) -> str: ...
    def _get_limname(self, which: str, name: str) -> float | None: ...
    def _print_lims(self) -> list[str]: ...
    def _range_setting(self, min_val: float, max_val: float, mode: str) -> tuple[float | None, float | None]: ...
    def _shared_ranges(self) -> None: ...
    def _add_spy(self, zoom: float, size: float, **kwargs) -> int: ...
    def _reduce_points(self) -> None: ...
    def _to_tex(self, filename: str, png: Optional[bool]=False, standalone: None | bool=None, print_requirements: bool=False) -> str: ...
    def _save(self, filename: str, standalone: None | bool=None, print_requirements: bool=False) -> None: ...
    def _save_image(self, filename: str) -> None: ...
    def _get_width(self) -> float | None: ...
    def _get_height(self) -> float | None: ...

    def clear(self) -> None:
        """
        Clear figure.
        """
        ...

    def _get_free_path_name(self) -> str: ...
    def _add_col(self, r: float, g: float, b: float) -> None: ...
    def _add_global(self, setting: str) -> None: ...
    def _next_coordinate_name(self) -> str: ...
    def _add_text(self, text: object) -> None: ...
    def tight_layout(self, h_pad: float=0, w_pad: float=0, rect: tuple[float, float, float, float]=(0, 0, 1, 1)) -> None:
        """
        This method works a bit differently than matplotlib's. It requires local pdflatex to compile the empty axis and estimate the required paddings. It will also try adjusting the size of the axis in a way to make whole figure match the set size. It works only with groupplots (TikzConfig.USE_GROUPPLOTS = True). Simulation ignores most of the TikzConfig settings regarding padding, additional padding is set using kwargs here.

        Parameters
        ----------
        h_pad: float, optional
            Additional padding between rows of subplots, in cm.
        w_pad: float, optional
            Additional padding between columns of subplots, in cm.
        rect: tuple of 4 floats, optional
            Rectangle in normalized coordinates which the whole subplot will fit into. (left, bottom, right, top) in the range [0, 1].
        """
        ...
    def _add_required_package(self, package: str) -> None: ...
    def _check_required_packages(self) -> None: ...
