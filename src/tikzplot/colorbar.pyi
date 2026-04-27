from typing import Any, Iterable, Optional, Sequence, Tuple
import numpy.typing as npt
from .axes import Axes
from .axes3d import Axes3

ArrayLike = npt.ArrayLike


class Colorbar:
    """
    PGFPlots-compatible colorbar generator.

    This class converts a colormap definition into TikZ/PGFPlots
    colorbar configuration and provides utilities for color mapping.

    Typically constructed via:

        Colorbar(im, **kwargs)

    where `im` is a tuple describing an image:
        (axis, cmap, lower, upper)
    """

    def __init__(
        self,
        im: Optional[Tuple[Axes, str, float, float]] = ...,
        *,
        axis: Optional[Axes | Axes3] = ...,
        cmap: Optional[str] = ...,
        lower: Optional[float] = ...,
        upper: Optional[float] = ...,
        ticks: Optional[Sequence[ float]] = ...,
        tick_labels: Optional[Sequence[str | float]] = ...,
        label: Optional[str] = ...,
        width: Optional[float] = ...,
        horizontal: Optional[bool] = ...,
        rel_len: Optional[float] = ...,
        divisions: Optional[int] = ...
    ) -> None:
        """
        Parameters
        ----------
        im : imshow() return: tuple(axis, cmap, lower, upper), optional
            Tuple describing the associated image:
            - axis : parent axis object
            - cmap : name of the colormap
            - lower : minimum value of the color scale
            - upper : maximum value of the color scale

        axis: reference to axis, optional
            Axis to which the color bar is plotted.

        cmap : str, optional
            Name of the colormap to use.
            Supports reversed colormaps via suffix "_r".

        lower : float, optional
            Minimum value of the color scale.

        upper : float, optional
            Maximum value of the color scale.

        ticks : sequence of str, optional
            Positions of ticks on the colorbar.
            Must be provided as strings for direct PGFPlots usage.

        tick_labels : sequence of str, optional
            Labels corresponding to `ticks`.
            Must have the same length as `ticks`.

            Special cases:
            - empty list `[]` → disables tick labels

        label : str, optional
            Title of the colorbar.

        width : float, default = 0.3
            Thickness of the colorbar (in cm).

            - vertical colorbar → width
            - horizontal colorbar → height

        horizontal : bool, default = False
            If True, renders a horizontal colorbar.
            Otherwise, a vertical colorbar is used.

        rel_len : float, default = 1
            Relative length of the colorbar with respect to the parent axis.

            Internally mapped to:
                width or height = rel_len * parent axis dimension
        divisions: int, optional
            May be used with continuous colormaps do discretize number of colors, 0 for continuous.
        """
        ...

    def _generate_tex_colormap(self, cmap_name: str) -> str:
        """
        Generate a PGFPlots-compatible colormap definition.

        Parameters
        ----------
        cmap_name : str
            Name of the colormap.
            Supports reversed maps using suffix "_r".

        Returns
        -------
        str
            TikZ colormap definition string.
        """
        ...

    def color(self, value: float) -> Tuple[float, float, float]:
        """
        Map a scalar value to an RGB color using the current colormap.

        Parameters
        ----------
        value : float
            Value within the range [lower, upper].

        Returns
        -------
        tuple of float
            RGB color as (r, g, b), each in [0, 1].
        """
        ...
