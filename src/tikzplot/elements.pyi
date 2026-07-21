from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Sequence, Union

import numpy as np

ArrayLike = Sequence[float] | np.ndarray
ErrorLike = int | float | Sequence[float] | Sequence[Sequence[float]]
SettingsLike = list[str] | str | None
ColorLike = Union[str, Sequence[float], Sequence[Sequence[float] | ArrayLike], np.ndarray, None]    


class BaseGraph:
    _axes: Any
    _classic: bool
    _style: dict[str, Any]
    _label: str | None
    _settings: list[str]
    _opacity: float
    _path_name: str | None
    _has_color: bool
    _style_str: str | None

    _x: np.ndarray
    _y: np.ndarray
    _z: np.ndarray
    _xerr: np.ndarray | None
    _yerr: np.ndarray | None
    _zerr: np.ndarray | None
    _x_asym: bool
    _y_asym: bool
    _z_asym: bool
    _colors: np.ndarray | None
    _sizes: np.ndarray | None
    _special: Any
    _st_dict: dict[str, str]
    _p_dict: dict[int, str]

    def __init__(self) -> None: ...

    def _normalize_error(self, err: ErrorLike | None, n: int) -> tuple[np.ndarray | None, bool]: ...
    def _style_string(self) -> str: ...
    def _save_data(self, points: str, filename: str | Path) -> str: ...
    def _try_set_pname(self, pname: str) -> str: ...
    def _num_points(self) -> int: ...
    def _set_label(self, lab: str) -> None: ...


class Graph(BaseGraph):
    def __init__(
        self,
        axes: Any,
        coordinates: tuple[Sequence[float], Sequence[float]] | Any,
        settings: list[str] = ...,
        xerr: ErrorLike | None = ...,
        yerr: ErrorLike | None = ...,
        path_name: str | None = ...,
        **style: Any,
    ) -> None: ...

    def _header(self) -> str: ...
    def _rows(self) -> str: ...
    def _to_tex(self, filename: str | Path) -> str: ...
    def _data_range(self) -> tuple[float, float, float, float]: ...
    def _get_erange(self, which: Literal["xmin", "xmax", "ymin", "ymax"]) -> float | None: ...
    def _filter(self, which: Literal["xmin", "xmax", "ymin", "ymax"], value: float) -> None: ...
    def _check_equal(self, x: ArrayLike, y: ArrayLike) -> bool: ...
    def _reduce_points(self, limit: int) -> None: ...


class Graph3(BaseGraph):
    def __init__(
        self,
        axes: Any,
        coordinates: tuple[Sequence[float], Sequence[float], Sequence[float]] | Any,
        settings: list[str] = ...,
        xerr: ErrorLike | None = ...,
        yerr: ErrorLike | None = ...,
        zerr: ErrorLike | None = ...,
        path_name: str | None = ...,
        **style: Any,
    ) -> None: ...

    def _header(self) -> str: ...
    def _rows(self) -> str: ...
    def _to_tex(self, filename: str | Path) -> str: ...
    def _data_range(self) -> tuple[float, float, float, float, float, float]: ...
    def _get_erange(self, which: Literal["xmin", "xmax", "ymin", "ymax", "zmin", "zmax"]) -> float | None: ...
    def _filter(self, which: Literal["xmin", "xmax", "ymin", "ymax", "zmin", "zmax"], value: float) -> None: ...
    def _check_equal(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> bool: ...
    def _reduce_points(self, limit: int, logx: bool = ..., logy: bool = ..., logz: bool = ...) -> None: ...
