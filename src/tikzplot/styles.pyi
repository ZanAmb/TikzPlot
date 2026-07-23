from pathlib import Path
from typing import Literal, NotRequired, TypedDict

StyleName = Literal["empty", "default", "classic", "538", "bmh", "ggplot", "seaborn", "dark_background"]

class StyleProfile(TypedDict):
    color_cycle: NotRequired[list[str]]
    line_width: NotRequired[float | None]
    grid: NotRequired[dict[str, str]]
    background: NotRequired[dict[str, str]]
    additional_settings: NotRequired[dict[str, str]]
    colorbar_settings: NotRequired[dict[str, str]]

class Styles:
    _STYLES: dict[str, StyleProfile]
    _style_setting: str
    _active_style: StyleProfile
    _user_styles_path: Path
    _user_styles: dict[str, StyleProfile]

    def __init__(self) -> None: ...
    def _load_user_styles(self) -> None: ...
    def use(self, style: StyleName | str) -> None:
        """
        Activate one of built-in styles or a user-defined style.
        """
    def get_profile(self, style: StyleName | str) -> StyleProfile:
        """
        Get the profile of a style. If the style is not found, return the currently active style.
        """
    def set_profile(self, style: str, profile: StyleProfile) -> None: 
        """
        Set and activate a user-defined style profile. Built-in styles cannot be modified.
        """
    def _get_style(self) -> str: ...
    def _get_color_cycle(self) -> list[str]: ...
    def _get_grid_cycle(self) -> dict[str, str] | None: ...
    def _get_background_cycle(self) -> str | None: ...
    def _get_line_width(self) -> float | None: ...
    def _get_additional_settings(self) -> dict[str, str] | None: ...
    def _get_colorbar_settings(self) -> dict[str, str] | None: ...