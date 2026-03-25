import numpy as np
from pathlib import Path

from .config import TikzConfig
from .state import next_export_num, main_name
from .colors import _tex_color
class Graph:
    _COLOR_MAP = {'b':'blue', 'g':'teal', 'r':'red', 'c':'cyan', 'm':'magenta', 'y':'yellow', 'k':'black', 'w':'white', "orange":"orange", "green": "green", "cyan":"cyan", "peru": "brown", "lime": "lime", "gray": "gray", "magenta": "magetna", "purple": "violet"}
    _LINE_MAP = {"--": "dashed", ":": "dotted", "-.": "dashdotted", "-":"solid"}
    _MARKER_MAP = {'o':'*', ".": "*", 's':'square*', '^':'triangle', 'v':'triangle*', 'd':'diamond', '+':'+', 'x':'x', '*':'star'}

    def __init__(self, axes, coordinates, settings=None, xerr=None, yerr=None, path_name=None, **style):
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
        self._classic = False
        if isinstance(coordinates, tuple):
            self._classic = True
            x,y=coordinates
            self._x = np.asarray(x)
            self._y = np.asarray(y)
            mask = np.isfinite(self._x) & np.isfinite(self._y)
            self._x = self._x[mask]
            self._y = self._y[mask]
            n = len(self._x)
            self._xerr, self._x_asym = __normalize_error(xerr, n)
            self._yerr, self._y_asym = __normalize_error(yerr, n)
            if self._xerr is not None:
                self._xerr = np.asarray(self._xerr)[mask]

            if self._yerr is not None:
                self._yerr = np.asarray(self._yerr)[mask]
        else:
            self._special = coordinates
        self._style = style
        self._label = None
        self._settings = settings
        if self._settings == None: self._settings = []

        self._ms_multiplier = 1
        self._opacity = 1
        self._path_name = path_name
        self._has_color = False
        self._style_str = None

    def _style_string(self):
        if self._style_str != None:
            return self._style_str
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
            self._has_color = True
            ccode, op = _tex_color(input)
            if not isinstance(op, bool):
                self._opacity = op
            if isinstance(ccode, str):
                return ccode
            r,g,b=ccode
            self._axes._add_col(r,g,b)
            return f"c{r:.3f}{g:.3f}{b:.3f}".replace(".", "")

        if "fmt" in self._style:
            fmt = self._style["fmt"]
            col = list(set(self._COLOR_MAP.keys()) & set(fmt))
            if col:
                opts.append(f"color={self._COLOR_MAP[col[0]]}")
                fmt = fmt.replace(col[0], "")
                self._has_color = True
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
        if "markerfmt" in self._style:
            col = list(set(self._COLOR_MAP.keys()) & set(fmt))
            if col:
                opts.append(f"mark options={{{self._COLOR_MAP[col[0]]}}}")
                fmt = fmt.replace(col[0], "")
                self._has_color = True
            mark = list(set(self._MARKER_MAP.keys()) & set(fmt))
            if mark:
                opts.append(f"mark={self._MARKER_MAP[mark[0]]}")
                fmt = fmt.replace(mark[0], "")
        if "label" in self._style:
            self._label = self._style["label"]

        if "alpha" in self._style:
            self._opacity = self._style["alpha"]

        #if "onlayer" in self._style:
        #    opts.append(f"on layer={self._style["onlayer"]}")

        if self._classic:
            if self._xerr is not None or self._yerr is not None:
                opts.append("error bars/.cd")
                if self._xerr is not None:
                    opts.append("x dir=both")
                    opts.append("x explicit")
                if self._yerr is not None:
                    opts.append("y dir=both")
                    opts.append("y explicit")
        if self._opacity < 1:
            opts.append(f"opacity={self._opacity}")
        if not self._has_color and self._classic:
            opts.append(f"color={{{match_color(f'C{self._axes._get_defcol()}')}}}")
        keys = {}
        for i in reversed(range(len(opts))):
            key = str(opts[i]).split("=")
            if key[0] in keys:
                del opts[i]
        if self._path_name: self._settings.append(f"name path={self._path_name}")
        if self._settings:
            opts = self._settings + opts
        self._style_str = ",\n".join(str(o) for o in opts)
        return self._style_str

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
    
    def _save_data(self, points, filename):
        path = Path(filename)
        file_number = next_export_num()
        current = path.parent
        dir = current / TikzConfig.DATAPOINTS_DIR
        dir.mkdir(parents=True, exist_ok=True)
        file_name = dir / f"{str(path.stem)}_{file_number}.dat"
        if not TikzConfig.UPDATE_STYLE_ONLY:
            with file_name.open("w", encoding="utf-8") as f:
                f.write(points)
        return str(Path(TikzConfig.DATAPOINTS_DIR) / f"{str(path.stem)}_{file_number}.dat")
    
    def _to_tex(self, filename):
        style = self._style_string()

        if self._classic:
            header = self._header()
            rows = self._rows()
            table_opts = "x=x,y=y"
            if self._xerr is not None:
                table_opts += ",x error=xerror"
            if self._yerr is not None:
                table_opts += ",y error=yerror"
            datapoints = f"{header}\n{rows}\n"
            if TikzConfig.SAVE_DATAPOINTS:
                datapoints = self._save_data(datapoints, filename)
            if not TikzConfig.SAVE_DATAPOINTS or (TikzConfig.SAVE_DATAPOINTS and not TikzConfig.UPDATE_DATA_ONLY):
                if self._label and self._axes._legend_on:
                    return f"\\addplot [{style}] table [{table_opts}] {{{datapoints}}};\\addlegendentry{{{self._label}}}"
                return f"\\addplot [forget plot,\n{style}] table [{table_opts}] {{{datapoints}}};"
            return ""
        elif TikzConfig.SAVE_DATAPOINTS or not (TikzConfig.SAVE_DATAPOINTS and not TikzConfig.UPDATE_STYLE_ONLY):
            return f"""\\addplot [forget plot,\n{style}] {self._special};"""
        else:
            return ""
    
    def _data_range(self, which):
        xmin, xmax = min(self._x), max(self._x)
        ymin, ymax = min(self._y), max(self._y)
        return xmin, xmax, ymin, ymax
    
    def _get_erange(self, which):
        if which == "xmin":
            return min(self._x)
        if which == "xmax":
            return max(self._x)
        if which == "ymin":
            return min(self._y)
        if which == "ymax":
            return max(self._y)
        
    def _filter(self, which, value):
        if which == "xmin":
            mask = self._x >= value
            idx_keep = np.where(self._x < value)[0]
            if len(idx_keep) > 0:
                idx_keep = idx_keep[-1]
        elif which == "xmax":
            mask = self._x <= value
            idx_keep = np.where(self._x > value)[0]
            if len(idx_keep) > 0:
                idx_keep = idx_keep[0]
        elif which == "ymin":
            mask = self._y >= value
            idx_keep = np.where(self._y < value)[0]
            if len(idx_keep) > 0:
                idx_keep = idx_keep[-1]
        elif which == "ymax":
            mask = self._y <= value
            idx_keep = np.where(self._y > value)[0]
            if len(idx_keep) > 0:
                idx_keep = idx_keep[0]
    
        else:
            raise ValueError("Invalid filter type")
    
        mask[idx_keep] = True
    
        self._x = self._x[mask]
        self._y = self._y[mask]
    
        if self._xerr is not None:
            self._xerr = self._xerr[mask]
    
        if self._yerr is not None:
            self._yerr = self._yerr[mask]

    def _check_equal(self, x,y):
        if self._classic:
            return np.array_equal(np.asarray(x),self._x) and np.array_equal(np.asarray(y),self._y)
        return False

    def _try_set_pname(self, pname):
        if self._path_name:
            return self._path_name
        self._path_name = pname
        return pname
    
    def _num_points(self):
        if self._classic:
            return len(self._x)
        return 0
    
    def _reduce_points(self, limit, logx=False, logy=False):
        if self._classic:
            l = len(self._x)
            if l > limit:
                if TikzConfig.REDUCE_METHOD == 0:
                    idx_keep = np.linspace(0, l-1, limit, dtype=int)
                    self._x = self._x[idx_keep]
                    self._y = self._y[idx_keep]
                    if self._xerr is not None:
                        self._xerr = self._xerr[idx_keep]
                    if self._yerr is not None:
                        self._yerr = self._yerr[idx_keep]
                elif TikzConfig.REDUCE_METHOD in [1,2]:
                    if logx:
                        vis_x = np.log(self._x)
                    else:
                        vis_x = self._x
                    if logy:
                        vis_y = np.log(self._y)
                    else:
                        vis_y = self._y
                    while len(self._x) > limit:
                        if TikzConfig.REDUCE_METHOD == 1:
                            dx1 = vis_x[1:-1] - vis_x[:-2]
                            dy1 = vis_y[1:-1] - vis_y[:-2]
                            dx2 = vis_x[2:] - vis_x[1:-1]
                            dy2 = vis_y[2:] - vis_y[1:-1]
                            crit = np.hypot(dx1, dy1) + np.hypot(dx2, dy2)
                        elif TikzConfig.REDUCE_METHOD == 2:
                            x0, x1, x2 = vis_x[:-2], vis_x[1:-1], vis_x[2:]
                            y0, y1, y2 = vis_y[:-2], vis_y[1:-1], vis_y[2:]
                            crit = np.abs((x1 - x0)*(y2 - y0) - (y1 - y0)*(x2 - x0))
                        idx_remove = np.argmin(crit)+1
                        if idx_remove == len(crit): idx_remove -= 1
                        mask = np.ones(len(self._x), dtype=bool)
                        mask[idx_remove] = False
                        self._x = self._x[mask]
                        self._y = self._y[mask]
                        vis_x = vis_x[mask]
                        vis_y = vis_y[mask]
                        if self._xerr is not None:
                            self._xerr = self._xerr[mask]
                        if self._yerr is not None:
                            self._yerr = self._yerr[mask]

    def _set_label(self, lab):
        self._style["label"] = lab