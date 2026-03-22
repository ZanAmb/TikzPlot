from .axes import Axes as Axes
from .config import TikzConfig as TikzConfig

class Figure:
    def __init__(self) -> None: ...
    def set_size_inches(self, *args) -> None: 
        """
        Set figure size (w,h).
        """
        ...
    def clear(self) -> None: 
        """
        Clear figure.
        """
        ...
