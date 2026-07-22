from typing import Any

from .config import TikzConfig
from .styles import Styles

_COLOR_MAP: dict[str, str] = {'b':'blue', 'g':'teal', 'r':'red', 'c':'cyan', 'm':'magenta', 'y':'yellow', 'k':'black', 'w':'white', "orange":"orange", "green": "green", "cyan":"cyan", "peru": "brown", "lime": "lime", "gray": "gray", "magenta": "magetna", "purple": "violet"}

def _tex_color(input, style=Styles()) -> tuple[Any, bool | float]:
    def color_string(r,g,b):
        if TikzConfig.USE_XCOLOR:
            return (r,g,b)
        else:
            return f"rgb:red,{r};green,{g};blue,{b}"
    
    def hex_to_rgb(hex):
        if hex[0] == "#":
            hex = hex[1:]
        hex = hex.upper()
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16) / 255
            rgb.append(decimal)  
        return color_string(rgb[0],rgb[1],rgb[2])
       
    if isinstance(input, tuple):
        opacity = False
        if len(input) == 1:
            input = input[0]
        elif len(input) == 2:
            opacity= input[1]
            input = input[0]
        else:
            r,g,b = input[:3]
            if len(input) == 4:
                opacity = input[3]                    
            return color_string(r,g,b), opacity
    s = str(input)
    if s[0] == "#":
        opacity = False
        if len(s) == 4:
            hex = s[1] * 2 + s[2] * 2 + s[3] * 2
        else:
            hex = s[:8]
            if len(s) > 8:
                opacity = int(s[8:]) / 100
        return hex_to_rgb(hex), opacity
    if s.isdigit():
        i = float(s)
        return color_string(i,i,i), False
    if s.startswith("C") and s[1:].isdigit():
        index = int(s[1:]) % len(style._get_color_cycle())
        return hex_to_rgb(style._get_color_cycle()[index]), False
    if s.lower() == "none":
        return color_string(0,0,0), 0
    if s in _COLOR_MAP.keys():
        return _COLOR_MAP[s], False
    if s in _COLOR_MAP.values():
        return s, False
    print(f"Unrecognized color {input}")
    return None, False