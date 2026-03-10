from .axes import Axes
from .config import TikzConfig

class Figure:

    def __init__(self):
        self.axes = []
        self.width = None
        self.height = None
        if TikzConfig.DEFAULT_WIDTH:
            self.width = TikzConfig.DEFAULT_WIDTH
        if TikzConfig.DEFAULT_HEIGHT:
            self.height = TikzConfig.DEFAULT_HEIGHT

        self.sharex = None
        self.sharey = None

        self.nrows = 0
        self.ncols = 0

    def add_subplot(self, nrows, ncols, index, sharex, sharey):
        ax = Axes(nrows, ncols, index, self)
        self.nrows = nrows
        self.ncols = ncols
        self.axes.append(ax)
        if sharex:
            self.sharex = sharex
        if sharey:
            self.sharey = sharey
        return ax    
    
    def add_subplots(self, nrows, ncols, sharex, sharey):
        grid = []
        if sharex:
            self.sharex = sharex
        if sharey:
            self.sharey = sharey
        for i in range(1, nrows * ncols + 1):
            ax = self.add_subplot(nrows, ncols, i, sharex, sharey)
            grid.append(ax)
        return grid
    
    def set_size_inches(self, *args):
        try:
            w,h = args
            self.width = w * 2.5
            self.height = h * 2.5
            for ax in self.axes:
                ax._update_size()
        except:
            pass
    
    def _compute_group_spacing(self):

        max_left = 0
        max_right = 0
        max_top = 0
        max_bottom = 0

        for ax in self.axes:

            l, r, t, b = ax.margins()

            max_left = max(max_left, l)
            max_right = max(max_right, r)
            max_top = max(max_top, t)
            max_bottom = max(max_bottom, b)

        horizontal = max_left + max_right
        vertical = max_top + max_bottom

        return f"{horizontal:.2f}cm", f"{-vertical:.2f}cm"
    
    def shared_ranges(self):
        shared_x = []
        shared_y = []
        if self.sharex and self.sharex != "none":
            if self.sharex == "all":
                shared_x = [self.axes]
            if self.sharex == "row":
                shared_x = [[] for _ in range(self.nrows)]
                for ax in self.axes:
                    shared_x[ax.row].append(ax)
            elif self.sharex == "col":
                shared_x = [[] for _ in range(self.ncols)]
                for ax in self.axes:
                    shared_x[ax.col].append(ax)
        if self.sharey and self.sharey != "none":
            if self.sharey == "all":
                shared_y = [self.axes]
            if self.sharey == "row":
                shared_y = [[] for _ in range(self.nrows)]
                for ax in self.axes:
                    shared_y[ax.row].append(ax)
            elif self.sharey == "col":
                shared_y = [[] for _ in range(self.ncols)]
                for ax in self.axes:
                    shared_y[ax.col].append(ax)
        def set_ax_ranges(which, group):
        
            hard_min_vals = []
            hard_max_vals = []
            mode = "lin"
        
            # ---- check hard limits ----
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
        
            # ---- if any hard limits exist, use them ----
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
        
            # ---- otherwise compute ranges from data ----
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
        
                else:  # log
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

    def to_tex(self):
        if not self.axes:
            return ""
        gs = self._compute_group_spacing()
        self.shared_ranges()
        lines = ["\\begin{tikzpicture}"]
        nrows = self.axes[0].nrows
        ncols = self.axes[0].ncols
        for ax in self.axes:
            lines.append("\\begin{axis}")
            lines.append(f"[{ax.axis_option_string(gs)}]")
            lines.append(ax.content_tex())
            lines.append("\\end{axis}")
            if ax.secondary_y is not None:
                ax_sec_y = ax.secondary_y
                lines.append("\\begin{axis}")
                lines.append(f"[{ax_sec_y.axis_option_string()}]")
                lines.append(ax_sec_y.content_tex())
                lines.append("\\end{axis}")
        lines.append("\\end{tikzpicture}")
        return "\n".join(lines)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.to_tex())