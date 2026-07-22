class Styles:
    _STYLES = ["empty", "default", "classic", "tableau", "colorblind10", "ggplot", "538", "seaborn", "bmh", "dark_background"]

    _COLOR_CYCLES: dict[str, list[str]] = {"empty": ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf'],
         'default': ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf'],
         'classic': ['#1f77b4', "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
         '538': ['#008fd5', '#fc4f30', '#e5ae38', '#6d904f', '#8b8b8b', '#810f7c'],
         'bmh': ['#348abd', '#a60628', '#7a68a6', '#467821', '#d55e00', '#cc79a7', '#56b4e9', '#009e73', '#f0e442', '#0072b2'],
         'classic': ['#0000ff', '#008000', '#ff0000', '#00bfbf', '#bf00bf', '#bfbf00', '#000000'],
         'colorblind': ['#0072b2', '#009e73', '#d55e00', '#cc79a7', '#f0e442', '#56b4e9'],
         'colorblind10': ['#006ba4', '#ff800e', '#ababab', '#595959', '#5f9ed1', '#c85200', '#898989', '#a2c8ec', '#ffbc79', '#cfcfcf'],
         'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
         'ggplot': ['#e24a33', '#348abd', '#988ed5', '#777777', '#fbc15e', '#8eba42', '#ffb5b8'],
         'seaborn': ['#4c72b0', '#55a868', '#c44e52', '#8172b2', '#ccb974', '#64b5cd'],
         'dark_background': ['#8dd3c7', '#feffb3', '#bfbbd9', '#fa8174', '#81b1d2', '#fdb462', '#b3de69', '#bc82bd', '#ccebc4', '#ffed6f']}

    _GRID_CYCLES: dict[str, dict[str, str]] = {'bmh': {"visible": "True", "which": "major", "color": "gray"},
                                               '538': {"visible": "True", "which": "major", "color": "gray"},
                                               'ggplot': {"visible": "True", "which": "major", "color": "white"},
                                               'seaborn': {"visible": "True", "which": "major", "color": "white"}}

    _BACKGROUND_CYCLES: dict[str, str] = {'bmh': "fill=gray!10", '538': "fill=gray!10", 'ggplot': "fill=gray!20", 'seaborn': "fill=gray!20", 'dark_background': "fill=black"}

    _LW_CYCLES: dict[str, float | None] = {'empty': None, 'bmh': 1.5, '538': 2.0, 'seaborn': 1.5}
    _ADDIT_SETTINGS: dict[str, dict[str, str]] = {'bmh': {"axis line style": "{draw=gray!50}"},
                                                  '538': {"axis line style": "{draw=none}"}, 
                                                  'ggplot': {"axis line style": "{draw=none}", "tick style": "{draw=gray}", "tick label style": "gray"}, 
                                                  'seaborn': {"axis line style": "{draw=none}", "tick style": "{draw=white}"},
                                                  'dark_background': {"every axis/.style": "gray!15", "tick style": "{draw=gray!15}", "tick label style": "gray!15", "axis line style": "{draw=gray!15}", "legend style": "{draw=white, fill=black}"}}

    _COLORBAR_SETTINGS: dict[str, dict[str, str]] = {'dark_background': {"text": "gray!15"}}

    _style_setting: str = "empty"
    _color_cycle: list[str] = _COLOR_CYCLES[_style_setting]

    def __init__(self):
        self._style_setting = "empty"
        self._color_cycle = self._COLOR_CYCLES[self._style_setting]

    def use(self, style: str):
        if style in self._STYLES:
            self._style_setting = style
            self._color_cycle = self._COLOR_CYCLES[self._style_setting]
        else:
            print(f"Style {style} not available.")

    def _get_style(self) -> str:
        return self._style_setting

    def _get_color_cycle(self) -> list[str]:
        return self._color_cycle

    def _get_grid_cycle(self) -> dict[str, str] | None:
        return self._GRID_CYCLES.get(self._style_setting, None)

    def _get_background_cycle(self) -> str | None:
        return self._BACKGROUND_CYCLES.get(self._style_setting, None)

    def _get_line_width(self) -> float | None:
        return self._LW_CYCLES.get(self._style_setting, 1.0)

    def _get_additional_settings(self) -> dict[str, str] | None:
        return self._ADDIT_SETTINGS.get(self._style_setting, None)

    def _get_colorbar_settings(self) -> dict[str, str] | None:
        return self._COLORBAR_SETTINGS.get(self._style_setting, None)