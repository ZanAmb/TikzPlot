from .axes import Axes as Axes
from .config import TikzConfig as TikzConfig

from typing import Optional

class Figure:
    def __init__(self) -> None: ...
    def add_subplot(self, nrows:Optional[int], ncols:Optional[int], index:Optional[int], sharex:Optional[str], sharey:Optional[str], projection:Optional[str], polar:Optional[bool]) -> Axes:
        """
        Add subplot axis.
        Parameters
        ----------
        projection: None, "polar", "3d", optional
        polar: bool, optional
            Use polar projection for axis (no additional features implemented yet).
        """
        ...
    def set_size_inches(self, *args) -> None: 
        """
        Set figure size (w,h).
        """
        ...

    def delaxes(self, ax:Axes) -> None:
        """
        Delete axis from figure.
        """
        ...
    def clear(self) -> None: 
        """
        Clear figure.
        """
        ...
