# config.pyi

from typing import Any, Dict
from pathlib import Path

from typing import TypedDict, Unpack

class _ConfigParams(TypedDict, total=False):
    USE_DECIMAL_COMMA: bool

    LEGEND_REL_X: float
    LEGEND_REL_Y: float

    LEFT_PADDING: float
    RIGHT_PADDING: float
    TOP_PADDING: float
    BOTTOM_PADDING: float
    Y_LABEL_PADDING: float
    SEC_Y_PADDING: float
    SEC_Y_LABEL_PADDING: float
    TITLE_PADDING: float
    X_LABEL_PADDING: float

    DEFAULT_WIDTH: float
    DEFAULT_HEIGHT: float

    SHARED_AXIS_REL_MARGIN: float

    SAVE_DATAPOINTS: bool
    DATAPOINTS_DIR: str
    UPDATE_DATA_ONLY: bool
    UPDATE_STYLE_ONLY: bool

    SHOW_SAVENAME: str
    IMSHOW_SAVENAME: str

    REDUCE_NUM_POINTS: bool
    REDUCE_METHOD: int
    MAX_POINTS_PER_FIGURE: int
    MAX_POINTS_PER_ELEMENT: int

    STANDALONE: bool
    USE_XCOLOR: bool

    CBAR_X_OFFSET: float
    CBAR_Y_OFFSET: float


class TikzConfig:

    def modifyParam(self, **kwargs: Unpack[_ConfigParams]) -> None:
        """
        Modify configuration parameters temporarily.

        Parameters
        ----------
        kwargs:
            Key-value pairs of configuration parameters to update.

        Raises
        ------
        ValueError
            If an unknown parameter is provided.
        """
        ...

    def setPermanent(self, **kwargs: Unpack[_ConfigParams]) -> None:
        """
        Modify configuration parameters permanently.

        Updates the in-memory configuration and writes changes
        to the user configuration file (~/.tikz_userconf.json).

        Parameters
        ----------
        kwargs:
            Key-value pairs of configuration parameters to update.
        """
        ...
