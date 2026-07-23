from typing import Any, NotRequired, TypedDict
import json
from pathlib import Path

class StyleProfile(TypedDict):
    color_cycle: NotRequired[list[str]]
    line_width: NotRequired[float | None] # None for LaTeX default line width, if not specified, default is 1.0
    grid: NotRequired[dict[str, str]]
    background: NotRequired[dict[str, str]]
    additional_settings: NotRequired[dict[str, str]]
    colorbar_settings: NotRequired[dict[str, str]]

class Styles:
    _STYLES: dict[str, StyleProfile] = {
        "empty": {"color_cycle": ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf'], "line_width": None},
        "default": {"color_cycle": ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']},
        "classic": {"color_cycle": ['#1f77b4', "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]},
        "538": {"color_cycle": ['#008fd5', '#fc4f30', '#e5ae38', '#6d904f', '#8b8b8b', '#810f7c'], "grid": {"visible": "True", "which": "major", "color": "gray"}, "background": {"fill": "gray!10"}, "line_width": 2.0, "additional_settings": {"axis line style": "{draw=none}"}},
        "bmh": {"color_cycle": ['#348abd', '#a60628', '#7a68a6', '#467821', '#d55e00', '#cc79a7', '#56b4e9', '#009e73', '#f0e442', '#0072b2'], "grid": {"visible": "True", "which": "major", "color": "gray"}, "background": {"fill": "gray!10"}, "line_width": 1.5, "additional_settings": {"axis line style": "{draw=gray!50}"}},
        "ggplot": {"color_cycle": ['#e24a33', '#348abd', '#988ed5', '#777777', '#fbc15e', '#8eba42', '#ffb5b8'], "grid": {"visible": "True", "which": "major", "color": "white"}, "background": {"fill": "gray!20"}, "additional_settings": {"axis line style": "{draw=none}", "tick style": "{draw=gray}", "tick label style": "gray"}},
        "seaborn": {"color_cycle": ['#4c72b0', '#55a868', '#c44e52', '#8172b2', '#ccb974', '#64b5cd'], "grid": {"visible": "True", "which": "major", "color": "white"}, "background": {"fill": "gray!20"}, "line_width": 1.5, "additional_settings": {"axis line style": "{draw=none}", "tick style": "{draw=white}"}},
        "dark_background": {"color_cycle": ['#8dd3c7', '#feffb3', '#bfbbd9', '#fa8174', '#81b1d2', '#fdb462', '#b3de69', '#bc82bd', '#ccebc4', '#ffed6f'], "background": {"fill": "black"}, "additional_settings": {"every axis/.style": "gray!15", "tick style": "{draw=gray!15}", "tick label style": "gray!15", "axis line style": "{draw=gray!15}", "legend style": "{draw=white, fill=black}"}, "colorbar_settings": {"text": "gray!15"}}
    }

    _style_setting: str = "empty"
    _active_style: StyleProfile = _STYLES[_style_setting]

    _user_styles_path: Path = Path.home() / ".tikzstyles_userconf.json"

    _user_styles: dict[str, StyleProfile] = {}

    def __init__(self):
        self._style_setting = "empty"
        self._active_style = self._STYLES[self._style_setting]
        self._load_user_styles()

    def _load_user_styles(self) -> None:
        if not self._user_styles_path.exists():
            return
        with open(self._user_styles_path) as f:
            data = json.load(f)
        self._user_styles = data

    def use(self, style: str):
        if style in self._STYLES:
            self._style_setting = style
            self._active_style = self._STYLES[self._style_setting]
        elif style in self._user_styles:
            self._style_setting = style
            self._active_style = self._user_styles[self._style_setting]
        else:
            print(f"Style {style} not available.")

    def get_profile(self, style: str) -> StyleProfile:
        return self._STYLES.get(style, self._user_styles.get(style, self._active_style))

    def set_profile(self, style: str, profile: StyleProfile) -> None:
        if style in self._STYLES:
            print(f"Style with name '{style}' already exists in default styles. Use a different name for your custom style.")
            return
        if "additional_settings" in profile:
            if "tick label style" in profile["additional_settings"]:
                profile["colorbar_settings"] = {"text": profile["additional_settings"]["tick label style"]}
        self._user_styles[style] = profile
        if not self._user_styles_path.exists():
            with open(self._user_styles_path, "w") as f:
                json.dump({}, f)
        with open(self._user_styles_path, "w") as f:
            json.dump(self._user_styles, f)
        self.use(style)

    def _get_style(self) -> str:
        return self._style_setting

    def _get_color_cycle(self) -> list[str]:
        return self._active_style.get("color_cycle", ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf'])

    def _get_grid_cycle(self) -> dict[str, str] | None:
        return self._active_style.get("grid", None)

    def _get_background_cycle(self) -> str | None:
        _bckg = self._active_style.get("background", None)
        if _bckg is not None:
            return ", ".join([f"{k}={v}" for k, v in _bckg.items()])
        return None

    def _get_line_width(self) -> float | None:
        return self._active_style.get("line_width", 1.0)

    def _get_additional_settings(self) -> dict[str, str] | None:
        return self._active_style.get("additional_settings", None)

    def _get_colorbar_settings(self) -> dict[str, str] | None:
        return self._active_style.get("colorbar_settings", None)