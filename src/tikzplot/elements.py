class Graph:
    COLOR_MAP = {'b':'blue', 'g':'teal', 'r':'red', 'c':'cyan', 'm':'magenta', 'y':'yellow', 'k':'black', 'w':'white', "orange":"orange", "green": "green", "cyan":"cyan", "peru": "brown", "lime": "lime", "gray": "gray", "magenta": "magetna", "purple": "violet"}
    LINE_MAP = {"--": "dashed", ":": "dotted", "-.": "dashdotted", "-":"solid"}
    MARKER_MAP = {'o':'*', ".": "*", 's':'square*', '^':'triangle', 'v':'triangle*', 'd':'diamond', '+':'+', 'x':'x', '*':'star'}

    def __init__(self, axes, x, y, xerr=None, yerr=None, **style):
        def _normalize_error(err, n):
            if err is None:
                return None, False
            if isinstance(err, (int, float)):
                return [err] * n, False
            if len(err) == n:
                if hasattr(err[0], "__len__") and len(err[0]) == 2:
                    return err, True

                return list(err), False
            raise ValueError("Invalid errorbar specification")
        self.axes = axes
        self.x = x
        self.y = y
        n = len(self.x)
        self.xerr, self.x_asym = _normalize_error(xerr, n)
        self.yerr, self.y_asym = _normalize_error(yerr, n)
        self.style = style
        self.label = None

        self.ms_multiplier = 1
        self.opacity = 1


    def _style_string(self):
        opts = []

        def match_ls(input):
            if input in self.LINE_MAP.keys():
                return self.LINE_MAP[input]
            if input in self.LINE_MAP.values():
                return input
            print(f"Unrecognized linestyle {input}")
            return None
        
        def match_mark(input):
            if input in self.MARKER_MAP.keys():
                return self.MARKER_MAP[input]
            if input in self.MARKER_MAP.values():
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
                    self.opacity= input[1]
                    input = input[0]
                else:
                    r,g,b = input[:3]
                    if len(input) == 4:
                        self.opacity = input[3]                    
                    return rgb_string(r,g,b)
            s = str(input)
            if s[0] == "#":
                if len(s) == 4:
                    hex = s[1] * 2 + s[2] * 2 + s[3] * 2
                else:
                    hex = s[:8]
                    if len(s) > 8:
                        self.opacity = int(s[8:]) / 100
                return hex_to_rgb(hex)
            if s.isdigit():
                i = float(s)
                return rgb_string(i,i,i)
            if s.lower() == "none":
                self.opacity = 0
                return rgb_string(0,0,0)
            if s in self.COLOR_MAP.keys():
                return self.COLOR_MAP[s]
            if s in self.COLOR_MAP.values():
                return s
            print(f"Unrecognized color {input}")
            return None

        if "fmt" in self.style:
            fmt = self.style["fmt"]
            col = list(set(self.COLOR_MAP.keys()) & set(fmt))
            if col:
                opts.append(f"color={self.COLOR_MAP[col[0]]}")
                fmt = fmt.replace(col[0], "")
            mark = list(set(self.MARKER_MAP.keys()) & set(fmt))
            if mark:
                opts.append(f"mark={self.MARKER_MAP[mark[0]]}")
                fmt = fmt.replace(mark[0], "")
            ls = match_ls(fmt)
            if ls:
                opts.append(ls)

        if "c" in self.style:
            sel_col = match_color(self.style['c'])
            if sel_col:
                opts.append(f"color={sel_col}")
        if "color" in self.style:
            sel_col = match_color(self.style['color'])
            if sel_col:
                opts.append(f"color={sel_col}")
        if "ls" in self.style:
            ls = self.style["ls"]
            if ls == "":
                opts.append("only marks")
            else:
                sel_ls = match_ls(ls)
                if sel_ls:
                    opts.append(sel_ls)
        if "linestyle" in self.style:
            ls = self.style["linestyle"]
            if ls == "":
                opts.append("only marks")
            else:
                sel_ls = match_ls(ls)
                if sel_ls:
                    opts.append(sel_ls)
        if "lw" in self.style:
            opts.append(self.style["lw"])
        if "linewidth" in self.style:
            opts.append(f"line width={self.style["linewidth"]}pt")
        if "marker" in self.style:
            sel_mark = match_mark(self.style['marker'])
            if sel_mark:
                opts.append(f"mark={sel_mark}")
        if "ms" in self.style:
            opts.append(f"mark size={self.style['ms']}pt")
        if "marksize" in self.style:
            opts.append(f"mark size={self.style['marksize']}pt")
        if "label" in self.style:
            self.label = self.style["label"]

        # Errorbar style
        if self.xerr is not None or self.yerr is not None:
            opts.append("error bars/.cd")
            if self.xerr is not None:
                opts.append("x dir=both")
                opts.append("x explicit")
            if self.yerr is not None:
                opts.append("y dir=both")
                opts.append("y explicit")
            
        keys = {}
        for i in reversed(range(len(opts))):
            key = opts[i].split("=")
            if key[0] in keys:
                del opts[i]

        return ",\n".join(opts)

    def _header(self):
        cols = ["x", "y"]
        if self.xerr is not None:
            if self.x_asym:
                cols += ["xerrminus", "xerrplus"]
            else:
                cols.append("xerror")
        if self.yerr is not None:
            if self.y_asym:
                cols += ["yerrminus", "yerrplus"]
            else:
                cols.append("yerror")
        return " ".join(cols)

    def _rows(self):    
        rows = []
        for i in range(len(self.x)):
            line = [self.x[i], self.y[i]]
            if self.xerr is not None:
                if self.x_asym:
                    line += list(self.xerr[i])
                else:
                    line.append(self.xerr[i])
            if self.yerr is not None:
                if self.y_asym:
                    line += list(self.yerr[i])
                else:
                    line.append(self.yerr[i])
            rows.append(" ".join(str(v) for v in line))
        return "\n".join(rows)

    def to_tex(self):
        style = self._style_string()
        header = self._header()
        rows = self._rows()

        # Include y error in table if present
        table_opts = "x=x,y=y"
        if self.xerr is not None:
            table_opts += ",x error=xerror"
        if self.yerr is not None:
            table_opts += ",y error=yerror"
        if self.label and self.axes.legend_on:
            return f"""\\addplot [{style}] table [{table_opts}] {{\n{header}\n{rows}\n}};\\addlegendentry{{{self.label}}}"""
        return f"""\\addplot [forget plot,\n{style}] table [{table_opts}] {{\n{header}\n{rows}\n}};"""    
    
    def data_range(self):
        xmin, xmax = min(self.x), max(self.x)
        ymin, ymax = min(self.y), max(self.y)
        return xmin, xmax, ymin, ymax            