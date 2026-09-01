from __future__ import annotations

import numpy as np
from typing import Optional
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
    def tight_layout(self) -> None:
        """
        Placeholder; spacings are set in TikzConfig.
        """
        ...
    def _add_required_package(self, package: str) -> None: ...
    def _check_required_packages(self) -> None: ...
