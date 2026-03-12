import numpy as np

class Graph:
    _COLOR_MAP = {'b':'blue', 'g':'teal', 'r':'red', 'c':'cyan', 'm':'magenta', 'y':'yellow', 'k':'black', 'w':'white', "orange":"orange", "green": "green", "cyan":"cyan", "peru": "brown", "lime": "lime", "gray": "gray", "magenta": "magetna", "purple": "violet"}
    _LINE_MAP = {"--": "dashed", ":": "dotted", "-.": "dashdotted", "-":"solid"}
    _MARKER_MAP = {'o':'*', ".": "*", 's':'square*', '^':'triangle', 'v':'triangle*', 'd':'diamond', '+':'+', 'x':'x', '*':'star'}

    def __init__(self, axes, x, y, settings=None, xerr=None, yerr=None, **style):
        def __normalize_error(err, n):
            if err is None:
                return None, False
            if isinstance(err, (int, float)):
                return np.asarray([err] * n), False
            if len(err) == n:
                if hasattr(err[0], "__len__") and len(err[0]) == 2:
                    return np.asarray(err), True

                return np.asarray(err), False
            raise ValueError("Invalid errorbar specification")
        self._axes = axes
        self._x = np.asarray(x)
        self._y = np.asarray(y)
        n = len(self._x)
        self._xerr, self._x_asym = __normalize_error(xerr, n)
        self._yerr, self._y_asym = __normalize_error(yerr, n)
        self._style = style
        self._label = None
        self._settings = settings

        self._ms_multiplier = 1
        self._opacity = 1

    def _style_string(self):
        opts = []

        def match_ls(input):
            if input in self._LINE_MAP.keys():
                return self._LINE_MAP[input]
            if input in self._LINE_MAP.values():
                return input
            print(f"Unrecognized linestyle {input}")
            return None
        
        def match_mark(input):
            if input in self._MARKER_MAP.keys():
                return self._MARKER_MAP[input]
            if input in self._MARKER_MAP.values():
                return input
            print(f"Unrecognized marker {input}")
            return None
        
        def match_color(input):

            def rgb_string(r,g,b):
                return f"rgb:red,{r};green,{g};blue,{b}"
            
            def hex_to_rgb(hex):
                if hex[0] == "#":
                    hex = hex[1:]
                hex = hex.upper()
                rgb = []
                for i in (0, 2, 4):
                    decimal = int(hex[i:i+2], 16) / 255
                    rgb.append(decimal)  
                return rgb_string(rgb[0],rgb[1],rgb[2])           

            if isinstance(input, tuple):
                if len(input) == 1:
                    input = input[0]
                elif len(input) == 2:
                    self._opacity= input[1]
                    input = input[0]
                else:
                    r,g,b = input[:3]
                    if len(input) == 4:
                        self._opacity = input[3]                    
                    return rgb_string(r,g,b)
            s = str(input)
            if s[0] == "#":
                if len(s) == 4:
                    hex = s[1] * 2 + s[2] * 2 + s[3] * 2
                else:
                    hex = s[:8]
                    if len(s) > 8:
                        self._opacity = int(s[8:]) / 100
                return hex_to_rgb(hex)
            if s.isdigit():
                i = float(s)
                return rgb_string(i,i,i)
            if s.lower() == "none":
                self._opacity = 0
                return rgb_string(0,0,0)
            if s in self._COLOR_MAP.keys():
                return self._COLOR_MAP[s]
            if s in self._COLOR_MAP.values():
                return s
            print(f"Unrecognized color {input}")
            return None

        if "fmt" in self._style:
            fmt = self._style["fmt"]
            col = list(set(self._COLOR_MAP.keys()) & set(fmt))
            if col:
                opts.append(f"color={self._COLOR_MAP[col[0]]}")
                fmt = fmt.replace(col[0], "")
            mark = list(set(self._MARKER_MAP.keys()) & set(fmt))
            if mark:
                opts.append(f"mark={self._MARKER_MAP[mark[0]]}")
                fmt = fmt.replace(mark[0], "")
            ls = None
            if fmt:
                ls = match_ls(fmt)
            if ls:
                opts.append(ls)

        if "c" in self._style:
            sel_col = match_color(self._style['c'])
            if sel_col:
                opts.append(f"color={{{sel_col}}}")
        if "color" in self._style:
            sel_col = match_color(self._style['color'])
            if sel_col:
                opts.append(f"color={{{sel_col}}}")
        if "ls" in self._style:
            ls = self._style["ls"]
            if ls == "":
                opts.append("only marks")
            else:
                sel_ls = match_ls(ls)
                if sel_ls:
                    opts.append(sel_ls)
        if "linestyle" in self._style:
            ls = self._style["linestyle"]
            if ls == "":
                opts.append("only marks")
            else:
                sel_ls = match_ls(ls)
                if sel_ls:
                    opts.append(sel_ls)
        if "lw" in self._style:
            opts.append(f"line width={self._style["lw"]}pt")
        if "linewidth" in self._style:
            opts.append(f"line width={self._style["linewidth"]}pt")
        if "marker" in self._style:
            sel_mark = match_mark(self._style['marker'])
            if sel_mark:
                opts.append(f"mark={sel_mark}")
        if "ms" in self._style:
            opts.append(f"mark size={self._style['ms']}pt")
        if "marksize" in self._style:
            opts.append(f"mark size={self._style['marksize']}pt")
        if "label" in self._style:
            self._label = self._style["label"]

        # Errorbar style
        if self._xerr is not None or self._yerr is not None:
            opts.append("error bars/.cd")
            if self._xerr is not None:
                opts.append("x dir=both")
                opts.append("x explicit")
            if self._yerr is not None:
                opts.append("y dir=both")
                opts.append("y explicit")
            
        keys = {}
        for i in reversed(range(len(opts))):
            key = str(opts[i]).split("=")
            if key[0] in keys:
                del opts[i]
        if self._settings:
            opts = self._settings + opts

        return ",\n".join(str(o) for o in opts)

    def _header(self):
        cols = ["x", "y"]
        if self._xerr is not None:
            if self._x_asym:
                cols += ["xerrminus", "xerrplus"]
            else:
                cols.append("xerror")
        if self._yerr is not None:
            if self._y_asym:
                cols += ["yerrminus", "yerrplus"]
            else:
                cols.append("yerror")
        return " ".join(cols)

    def _rows(self):    
        rows = []
        for i in range(len(self._x)):
            line = [self._x[i], self._y[i]]
            if self._xerr is not None:
                if self._x_asym:
                    line += list(self._xerr[i])
                else:
                    line.append(self._xerr[i])
            if self._yerr is not None:
                if self._y_asym:
                    line += list(self._yerr[i])
                else:
                    line.append(self._yerr[i])
            rows.append(" ".join(str(v) for v in line))
        return "\n".join(rows)

    def to_tex(self):
        style = self._style_string()
        header = self._header()
        rows = self._rows()

        # Include y error in table if present
        table_opts = "x=x,y=y"
        if self._xerr is not None:
            table_opts += ",x error=xerror"
        if self._yerr is not None:
            table_opts += ",y error=yerror"
        if self._label and self._axes._legend_on:
            return f"""\\addplot [{style}] table [{table_opts}] {{\n{header}\n{rows}\n}};\\addlegendentry{{{self._label}}}"""
        return f"""\\addplot [forget plot,\n{style}] table [{table_opts}] {{\n{header}\n{rows}\n}};"""    
    
    def data_range(self, which):
        xmin, xmax = min(self._x), max(self._x)
        ymin, ymax = min(self._y), max(self._y)
        return xmin, xmax, ymin, ymax
    
    def get_erange(self, which):
        if which == "xmin":
            return min(self._x)
        if which == "xmax":
            return max(self._x)
        if which == "ymin":
            return min(self._y)
        if which == "ymax":
            return max(self._y)
        
    def filter(self, which, value):
        if which == "xmin":
            mask = self._x >= value
            idx_keep = np.argmin(np.abs(self._x - value))
    
        elif which == "xmax":
            mask = self._x <= value
            idx_keep = np.argmin(np.abs(self._x - value))
    
        elif which == "ymin":
            mask = self._y >= value
            idx_keep = np.argmin(np.abs(self._y - value))
    
        elif which == "ymax":
            mask = self._y <= value
            idx_keep = np.argmin(np.abs(self._y - value))
    
        else:
            raise ValueError("Invalid filter type")
    
        mask[idx_keep] = True
    
        self._x = self._x[mask]
        self._y = self._y[mask]
    
        if self._xerr is not None:
            self._xerr = self._xerr[mask]
    
        if self._yerr is not None:
            self._yerr = self._yerr[mask]
    
    
    