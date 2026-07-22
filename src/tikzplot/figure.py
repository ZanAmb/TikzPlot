import numpy as np

from .axes import Axes
from .axes3d import Axes3
from .config import TikzConfig

class Figure:

    def __init__(self, style):
        self._axes = []
        self._width = None
        self._height = None
        self._style = style
        if TikzConfig.DEFAULT_WIDTH:
            self._width = TikzConfig.DEFAULT_WIDTH
        if TikzConfig.DEFAULT_HEIGHT:
            self._height = TikzConfig.DEFAULT_HEIGHT

        self._sharex = None
        self._sharey = None

        self._nrows = 0
        self._ncols = 0

        self._spacings = None
        
        self._last_path_num = 0

        self._col_dict = {}

        self._globals = set()
        self._spies = []

        self._num_coordinates = 0

        self.texts = []

        self._lims = {"xmin": {}, "xmax": {}, "ymin": {}, "ymax": {}}

    def add_subplot(self, nrows=1, ncols=1, index=1, sharex=None, sharey=None, projection=None, polar=False):
        if projection=="3d":
            ax = Axes3(nrows, ncols, index, self)
        else:
            pol: bool = projection=="polar" or polar
            ax = Axes(nrows, ncols, index, self, pol)
        self._nrows = nrows
        self._ncols = ncols
        self._axes.append(ax)
        if sharex:
            self._sharex = sharex
        if sharey:
            self._sharey = sharey
        return ax    
    
    def _add_subplots(self, nrows, ncols, sharex=None, sharey=None, subplot_kw=None):
        grid = []
        if sharex:
            self._sharex = sharex
        if sharey:
            self._sharey = sharey
        for i in range(1, nrows * ncols + 1):
            if subplot_kw:
                if "projection" in subplot_kw:
                    ax = self.add_subplot(nrows, ncols, i, sharex, sharey, projection=subplot_kw["projection"])
                else:
                    ax = self.add_subplot(nrows, ncols, i, sharex, sharey)
            else:
                ax = self.add_subplot(nrows, ncols, i, sharex, sharey)
            grid.append(ax)
        return grid
    
    def set_size_inches(self, *args):
        if isinstance(args[0], tuple):
            args = args[0]
        try:
            w,h = args
            self._width = w * 2.5
            self._height = h * 2.5
            for ax in self._axes:
                ax._update_size()
        except:
            pass

    def delaxes(self, ax):
        if ax in self._axes:
            self._axes.remove(ax)
            del ax
    
    def _compute_group_spacing(self):
        grid = np.zeros((self._nrows, self._ncols, 4))

        for ax in self._axes:
            grid[ax._get_row(), ax._get_col()] = np.array(ax._margins())
        l = grid[:, :, 0]
        r = grid[:, :, 1]
        t = grid[:, :, 2]
        b = grid[:, :, 3]
        if self._nrows > 1:
             row_spacing = np.max(b[:-1, :], axis=1) + np.max(t[1:, :], axis=1)
        else:
            row_spacing = [0]
        if self._ncols > 1:
            col_spacing = np.max(r[:, :-1], axis=0) + np.max(l[:, 1:], axis=0)
        else:
            col_spacing =  [0]
        self._spacings = row_spacing, col_spacing

    def _get_spacing(self, row, col):
        if not self._spacings:
            self._compute_group_spacing()
        assert self._spacings is not None
        if col == 0:
            if row == 0:
                return 0
            return self._spacings[0][row-1]
        return self._spacings[1][col-1]
    
    def _charcode(self, n):
        result = []
        while n > 0:
            n -= 1
            n, r = divmod(n, 26)
            result.append(chr(ord('a') + r))
        return ''.join(reversed(result))
    
    def _next_limname(self, which, value):
        d2 = {v: k for k, v in self._lims[which].items()}
        if value in d2.keys():
            return d2[value]
        dct = self._lims[which]
        n = len(dct)+1
        nm = "\\" + which + self._charcode(n)
        self._lims[which][nm] = value
        return nm
    
    def _get_limname(self, which, name):
        return self._lims[which].get(name)
    
    def _range_setting(self, min_val, max_val, mode):
        if min_val < max_val:
            if mode == "lin":
                d = max_val - min_val
                min_val -= d * TikzConfig.SHARED_AXIS_REL_MARGIN
                max_val += d * TikzConfig.SHARED_AXIS_REL_MARGIN
        
            else:
                d = (max_val / min_val) ** TikzConfig.SHARED_AXIS_REL_MARGIN
                min_val /= d
                max_val *= d

            return min_val, max_val
        return None, None
    
    def _shared_ranges(self):
        shared_x = []
        shared_y = []
        if self._sharex and self._sharex != "none":
            if self._sharex == "all" or self._sharex == True:
                shared_x = [self._axes]
            if self._sharex == "row":
                shared_x = [[] for _ in range(self._nrows)]
                for ax in self._axes:
                    shared_x[ax._get_row()].append(ax)
            elif self._sharex == "col":
                shared_x = [[] for _ in range(self._ncols)]
                for ax in self._axes:
                    shared_x[ax._get_col()].append(ax)
        if self._sharey and self._sharey != "none":
            if self._sharey == "all" or self._sharey == True:
                shared_y = [self._axes]
            if self._sharey == "row":
                shared_y = [[] for _ in range(self._nrows)]
                for ax in self._axes:
                    shared_y[ax._get_row()].append(ax)
            elif self._sharey == "col":
                shared_y = [[] for _ in range(self._ncols)]
                for ax in self._axes:
                    shared_y[ax._get_col()].append(ax)

        def set_ax_ranges(which, group):        
            hard_min_vals = []
            hard_max_vals = []
            mode = "lin"
        
            for ax in group:
                hmin, m = ax._get_hard_range(which + "min")
                if m == "log":
                    mode = "log"
                if hmin is not None:
                    hard_min_vals.append(hmin)
        
                hmax, m = ax._get_hard_range(which + "max")
                if m == "log":
                    mode = "log"
                if hmax is not None:
                    hard_max_vals.append(hmax)
        
            if hard_min_vals or hard_max_vals:
                min_val = min(hard_min_vals) if hard_min_vals else None
                max_val = max(hard_max_vals) if hard_max_vals else None
        
                if min_val is not None:
                    for ax in group:
                        ax._set_range(which + "min", min_val)
        
                if max_val is not None:
                    for ax in group:
                        ax._set_range(which + "max", max_val)
                
            mins = [ax._get_range(which + "min") for ax in group]
            maxes = [ax._get_range(which + "max") for ax in group]
        
            min_val = min(r[0] for r in mins)
            max_val = max(r[0] for r in maxes)
            mode = "log" if "log" in [r[2] for r in mins] else "lin"
            min_val, max_val = self._range_setting(min_val, max_val, mode)
            for ax in group:
                if hard_min_vals == []:
                    ax._set_range(which + "min", min_val)
                if hard_max_vals == []:
                    ax._set_range(which + "max", max_val)        
        
        for group in shared_x:
            set_ax_ranges("x", group)
        
        for group in shared_y:
            set_ax_ranges("y", group)

    def _add_spy(self, zoom, size, **kwargs):
        sp_str = f"\\spy [size={size}cm, magnification={zoom}"
        bck = ""
        n = len(self._spies)
        if "shape" in kwargs and kwargs["shape"] == "circle":
            sp_str += ", circle"
            bck = f"\\fill[white] (spyviewr{n}) circle ({size/2}cm);\n"
        else:
            bck = f"\\fill[white] ($(spyviewr{n}) + (-{size/2}cm,-{size/2}cm)$) rectangle ($(spyviewr{n}) + ({size/2}cm,{size/2}cm)$);\n"
        if "connect" in kwargs and kwargs["connect"]:
            sp_str += ", connect spies"
        sp_str += f"] on (spypoint{n}) in node at (spyviewr{n});"
        self._spies.append(bck + sp_str)
        return n
    
    def _reduce_points(self):
        counts = [0]
        for ax in self._axes:
            counts += ax._num_points()
        counts = [min(c, TikzConfig.MAX_POINTS_PER_ELEMENT) for c in counts]
        limit = max(counts)
        if sum(counts) > TikzConfig.MAX_POINTS_PER_FIGURE:
            lo, hi = 0, max(counts)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                total = sum(min(c, mid) for c in counts)
                if total <= TikzConfig.MAX_POINTS_PER_FIGURE:
                    lo = mid
                else:
                    hi = mid - 1
            limit = lo

        for ax in self._axes:
            ax._reduce_points(limit)

    def _to_tex(self, filename):
        single = self._nrows * self._ncols == 1
        if not self._axes:
            return ""
        self._shared_ranges()
        if TikzConfig.REDUCE_NUM_POINTS:
            self._reduce_points()
        preambule = ""
        if TikzConfig.STANDALONE:
            preambule += "\\documentclass[tikz,border=2pt]{standalone}\n"
            preambule += "\\usepackage{tikz}\n"
            preambule += "\\usepackage{pgfplots}\n"
            if TikzConfig.USE_GROUPPLOTS and not single:
                preambule += "\\usepgfplotslibrary{groupplots}\n"
            preambule += "\\usepgfplotslibrary{fillbetween}\n"
            preambule += "\\usepgfplotslibrary{polar}\n"
            preambule += f"\\pgfplotsset{{compat={TikzConfig.TIKZ_COMPAT}}}\n"
            if TikzConfig.USE_XCOLOR:
                preambule += "\\usepackage{xcolor}\n"
            if self._spies:
                 preambule += "\\usetikzlibrary{spy}\n"
            preambule += "\\begin{document}\n"
            
        lines0 = [g for g in self._globals]
        lines = []
        lines2 = []
        if self._spies:
            lines0.append("\\begin{tikzpicture}[spy using outlines={}]")
        else:
            lines0.append("\\begin{tikzpicture}")
        nrows = self._axes[0]._get_nrows()
        ncols = self._axes[0]._get_ncols()
        if TikzConfig.USE_GROUPPLOTS and not single:
            self._compute_group_spacing()
            assert self._spacings is not None
            if len(self._spacings[0]) > 0 and len(self._spacings[1]) > 0:
                lines.append(f"\\begin{{groupplot}}[group style={{group size={ncols} by {nrows}, horizontal sep={max(self._spacings[1])}cm, vertical sep={max(self._spacings[0])}cm}}]")
            else:
                lines.append(f"\\begin{{groupplot}}[group style={{group size={ncols} by {nrows}}}]")
        for ax in self._axes:
            prim, sec = ax._to_tex(filename, single)
            lines += prim
            if sec:
                lines2 += sec
        if TikzConfig.USE_GROUPPLOTS and not single:
            lines.append("\\end{groupplot}")
        lines += lines2
        for spy in self._spies:
            lines.append(spy)
        for text in self.texts:
            lines.append(text._to_tex_fin())
        lines.append("\\end{tikzpicture}")
        for c in self._col_dict:
            r,g,b=self._col_dict[c]
            lines0.insert(1,f"\\definecolor{{{c}}}{{rgb}}{{{r:.3f}, {g:.3f}, {b:.3f}}}")
        fin = ""
        if TikzConfig.STANDALONE:
            fin += "\\end{document}"
        for k in self._lims.keys():
            for j in self._lims[k]:
                lines0.append(f"\\def{j}{{{self._lims[k][j]}}}")
        lines = lines0 + lines
        output = preambule + "\n" + "\n".join(lines) + "\n" + fin
        return output

    def _save(self, filename):
        content = self._to_tex(filename)
        if not TikzConfig.SAVE_DATAPOINTS or (TikzConfig.SAVE_DATAPOINTS and not TikzConfig.UPDATE_DATA_ONLY):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

    def _get_width(self):
        return self._width
    
    def _get_height(self):
        return self._height
    
    def clear(self):
        self.__init__(style=self._style)

    def _get_free_path_name(self):
        self._last_path_num += 1
        return f"path{self._last_path_num}"
    
    def _add_col(self, r,g,b):
        code = f"c{r:.3f}{g:.3f}{b:.3f}".replace(".", "")
        self._col_dict[code] = (r,g,b)

    def _add_global(self, setting):
        self._globals.add(setting)

    def _next_coordinate_name(self):
        self._num_coordinates += 1
        return f"(coordinate{self._num_coordinates})"
    
    def _add_text(self, text):
        self.texts.append(text)
