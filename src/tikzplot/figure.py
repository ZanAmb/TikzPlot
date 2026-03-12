import numpy as np

from .axes import Axes
from .config import TikzConfig

class Figure:

    def __init__(self):
        self._axes = []
        self._width = None
        self._height = None
        if TikzConfig.DEFAULT_WIDTH:
            self._width = TikzConfig.DEFAULT_WIDTH
        if TikzConfig.DEFAULT_HEIGHT:
            self._height = TikzConfig.DEFAULT_HEIGHT

        self._sharex = None
        self._sharey = None

        self._nrows = 0
        self._ncols = 0

        self._spacings = None

    def _add_subplot(self, nrows, ncols, index, sharex, sharey):
        ax = Axes(nrows, ncols, index, self)
        self._nrows = nrows
        self._ncols = ncols
        self._axes.append(ax)
        if sharex:
            self._sharex = sharex
        if sharey:
            self._sharey = sharey
        return ax    
    
    def _add_subplots(self, nrows, ncols, sharex, sharey):
        grid = []
        if sharex:
            self._sharex = sharex
        if sharey:
            self._sharey = sharey
        for i in range(1, nrows * ncols + 1):
            ax = self._add_subplot(nrows, ncols, i, sharex, sharey)
            grid.append(ax)
        return grid
    
    def set_size_inches(self, *args):
        try:
            w,h = args
            self._width = w * 2.5
            self._height = h * 2.5
            for ax in self._axes:
                ax._update_size()
        except:
            pass
    
    def _compute_group_spacing(self):
        grid = np.zeros((self._nrows, self._ncols, 4))

        for ax in self._axes:
            grid[ax._get_row(), ax._get_col()] = np.array(ax._margins())
        l = grid[:, :, 0]
        r = grid[:, :, 1]
        t = grid[:, :, 2]
        b = grid[:, :, 3]
        row_spacing = np.max(b[:-1, :], axis=1) + np.max(t[1:, :], axis=1)
        col_spacing = np.max(r[:, :-1], axis=0) + np.max(l[:, 1:], axis=0)
        self._spacings = row_spacing, col_spacing

    def _get_spacing(self, row, col):
        if not self._spacings:
            self._compute_group_spacing()
        if col == 0:
            if row == 0:
                return 0
            return self._spacings[0][row-1]
        return self._spacings[1][col-1]

    
    def _shared_ranges(self):
        shared_x = []
        shared_y = []
        if self._sharex and self._sharex != "none":
            if self._sharex == "all":
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
            if self._sharey == "all":
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
                hmin, m = ax.get_hard_range(which + "min")
                if m == "log":
                    mode = "log"
                if hmin is not None:
                    hard_min_vals.append(hmin)
        
                hmax, m = ax.get_hard_range(which + "max")
                if m == "log":
                    mode = "log"
                if hmax is not None:
                    hard_max_vals.append(hmax)
        
            if hard_min_vals or hard_max_vals:
                min_val = min(hard_min_vals) if hard_min_vals else None
                max_val = max(hard_max_vals) if hard_max_vals else None
        
                if min_val is not None:
                    for ax in group:
                        ax.set_range(which + "min", min_val)
        
                if max_val is not None:
                    for ax in group:
                        ax.set_range(which + "max", max_val)
        
                return
        
            mins = [ax.get_range(which + "min") for ax in group]
            maxes = [ax.get_range(which + "max") for ax in group]
        
            min_val = min(r[0] for r in mins)
            max_val = max(r[0] for r in maxes)
        
            for r in mins:
                if r[2] == "log":
                    mode = "log"
        
            if min_val < max_val:
                if mode == "lin":
                    d = max_val - min_val
                    min_val -= d * TikzConfig.SHARED_AXIS_REL_MARGIN
                    max_val += d * TikzConfig.SHARED_AXIS_REL_MARGIN
        
                else:
                    d = (max_val / min_val) ** TikzConfig.SHARED_AXIS_REL_MARGIN
                    min_val /= d
                    max_val *= d
        
            for ax in group:
                ax.set_range(which + "min", min_val)
                ax.set_range(which + "max", max_val)
        
        
        for group in shared_x:
            set_ax_ranges("x", group)
        
        for group in shared_y:
            set_ax_ranges("y", group)

    def _to_tex(self):
        if not self._axes:
            return ""
        self._shared_ranges()
        lines = ["\\begin{tikzpicture}"]
        nrows = self._axes[0]._get_nrows()
        ncols = self._axes[0]._get_ncols()
        for ax in self._axes:
            lines.append("\\begin{axis}")
            lines.append(f"[{ax._axis_option_string()}]")
            lines.append(ax.content_tex())
            lines.append("\\end{axis}")
            if ax._secondary_y is not None:
                ax_sec_y = ax._secondary_y
                lines.append("\\begin{axis}")
                lines.append(f"[{ax_sec_y._axis_option_string()}]")
                lines.append(ax_sec_y.content_tex())
                lines.append("\\end{axis}")
        lines.append("\\end{tikzpicture}")
        return "\n".join(lines)

    def _save(self, filename):
        with open(filename, "w") as f:
            f.write(self._to_tex())

    def _get_width(self):
        return self._width
    
    def _get_height(self):
        return self._height
    
    def _clear(self):
        del self