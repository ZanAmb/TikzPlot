from typing import Any

from .config import TikzConfig
from .styles import Styles

_COLOR_MAP: dict[str, str] = {
    'b': 'blue',
    'g': 'teal',
    'r': 'red',
    'c': 'cyan',
    'm': 'magenta',
    'y': 'yellow',
    'k': 'black',
    'w': 'white',

    'aliceblue': 'blue!10!white',
    'antiquewhite': 'orange!15!white',
    'aqua': 'cyan',
    'aquamarine': 'cyan!50!green',
    'azure': 'cyan!10!white',
    'beige': 'yellow!20!white',
    'bisque': 'orange!20!white',
    'black': 'black',
    'blanchedalmond': 'orange!25!white',
    'blue': 'blue',
    'blueviolet': 'blue!60!violet',
    'brown': 'brown',
    'burlywood': 'brown!40!yellow',
    'cadetblue': 'cyan!60!gray',
    'chartreuse': 'green!50!yellow',
    'chocolate': 'brown!80!orange',
    'coral': 'orange!80!red',
    'cornflowerblue': 'blue!60!cyan',
    'cornsilk': 'yellow!10!white',
    'crimson': 'red!80!black',
    'cyan': 'cyan',
    'darkblue': 'blue!75!black',
    'darkcyan': 'cyan!75!black',
    'darkgoldenrod': 'brown!60!yellow',
    'darkgray': 'gray!80',
    'darkgreen': 'green!75!black',
    'darkgrey': 'gray!80',
    'darkkhaki': 'yellow!60!gray',
    'darkmagenta': 'magenta!75!black',
    'darkolivegreen': 'green!50!black',
    'darkorange': 'orange!80!red',
    'darkorchid': 'purple!70!blue',
    'darkred': 'red!75!black',
    'darksalmon': 'orange!50!red',
    'darkseagreen': 'green!40!gray',
    'darkslateblue': 'blue!50!purple',
    'darkslategray': 'cyan!25!black',
    'darkslategrey': 'cyan!25!black',
    'darkturquoise': 'cyan!80!black',
    'darkviolet': 'violet!80!black',
    'deeppink': 'magenta!80!red',
    'deepskyblue': 'cyan!80!blue',
    'dimgray': 'gray!80!black',
    'dimgrey': 'gray!80!black',
    'dodgerblue': 'blue!80!cyan',
    'firebrick': 'red!75!brown',
    'floralwhite': 'yellow!5!white',
    'forestgreen': 'green!70!black',
    'fuchsia': 'magenta',
    'gainsboro': 'gray!20!white',
    'ghostwhite': 'blue!5!white',
    'gold': 'yellow!80!orange',
    'goldenrod': 'yellow!70!brown',
    'gray': 'gray',
    'green': 'green',
    'greenyellow': 'yellow!70!green',
    'grey': 'gray',
    'honeydew': 'green!10!white',
    'hotpink': 'pink!80!magenta',
    'indianred': 'red!60!brown',
    'indigo': 'violet!80!black',
    'ivory': 'yellow!5!white',
    'khaki': 'yellow!40!white',
    'lavender': 'purple!20!white',
    'lavenderblush': 'pink!10!white',
    'lawngreen': 'green!60!yellow',
    'lemonchiffon': 'yellow!20!white',
    'lightblue': 'blue!30!white',
    'lightcoral': 'red!40!white',
    'lightcyan': 'cyan!15!white',
    'lightgoldenrodyellow': 'yellow!25!white',
    'lightgray': 'gray!30!white',
    'lightgreen': 'green!40!white',
    'lightgrey': 'gray!30!white',
    'lightpink': 'pink!60!white',
    'lightsalmon': 'orange!40!white',
    'lightseagreen': 'teal!60!green',
    'lightskyblue': 'cyan!40!white',
    'lightslategray': 'cyan!30!gray',
    'lightslategrey': 'cyan!30!gray',
    'lightsteelblue': 'blue!30!gray',
    'lightyellow': 'yellow!10!white',
    'lime': 'lime',
    'limegreen': 'lime!80!black',
    'linen': 'orange!10!white',
    'magenta': 'magenta',
    'maroon': 'red!50!black',
    'mediumaquamarine': 'cyan!60!green',
    'mediumblue': 'blue!85!black',
    'mediumorchid': 'purple!60!magenta',
    'mediumpurple': 'purple!60!white',
    'mediumseagreen': 'green!60!gray',
    'mediumslateblue': 'blue!60!violet',
    'mediumspringgreen': 'green!80!cyan',
    'mediumturquoise': 'cyan!70!green',
    'mediumvioletred': 'magenta!80!black',
    'midnightblue': 'blue!85!black',
    'mintcream': 'cyan!5!white',
    'mistyrose': 'red!10!white',
    'moccasin': 'orange!30!white',
    'navajowhite': 'orange!35!white',
    'navy': 'blue!50!black',
    'oldlace': 'yellow!10!white',
    'olive': 'yellow!50!black',
    'olivedrab': 'green!60!yellow',
    'orange': 'orange',
    'orangered': 'orange!80!red',
    'orchid': 'magenta!60!white',
    'palegoldenrod': 'yellow!30!white',
    'palegreen': 'green!30!white',
    'paleturquoise': 'cyan!30!white',
    'palevioletred': 'magenta!50!white',
    'papayawhip': 'orange!15!white',
    'peachpuff': 'orange!30!white',
    'peru': 'brown',
    'pink': 'pink',
    'plum': 'purple!40!white',
    'powderblue': 'cyan!30!white',
    'purple': 'violet',
    'rebeccapurple': 'violet!70!black',
    'red': 'red',
    'rosybrown': 'brown!50!pink',
    'royalblue': 'blue!80!cyan',
    'saddlebrown': 'brown!80!black',
    'salmon': 'orange!60!red',
    'sandybrown': 'orange!60!brown',
    'seagreen': 'green!70!black',
    'seashell': 'orange!5!white',
    'sienna': 'brown!70!red',
    'silver': 'gray!40!white',
    'skyblue': 'cyan!50!white',
    'slateblue': 'blue!50!purple',
    'slategray': 'gray!60!cyan',
    'slategrey': 'gray!60!cyan',
    'snow': 'red!5!white',
    'springgreen': 'green!80!cyan',
    'steelblue': 'blue!60!gray',
    'tan': 'brown!50',
    'teal': 'teal',
    'thistle': 'purple!30!white',
    'tomato': 'orange!70!red',
    'turquoise': 'cyan!80!green',
    'violet': 'violet',
    'wheat': 'orange!30!white',
    'white': 'white',
    'whitesmoke': 'gray!10!white',
    'yellow': 'yellow',
    'yellowgreen': 'yellow!60!green',

    'tab:blue': 'blue!80!cyan',
    'tab:orange': 'orange',
    'tab:green': 'green!80!black',
    'tab:red': 'red',
    'tab:purple': 'purple',
    'tab:brown': 'brown',
    'tab:pink': 'pink',
    'tab:gray': 'gray',
    'tab:olive': 'yellow!50!black',
    'tab:cyan': 'cyan',
}
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