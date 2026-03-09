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

    def add_subplot(self, nrows, ncols, index):
        ax = Axes(nrows, ncols, index, self)
        self.axes.append(ax)
        return ax
    
    def add_subplots(self, nrows, ncols):
        grid = []
        for i in range(1, nrows * ncols + 1):
            ax = self.add_subplot(nrows, ncols, i)
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

    def to_tex(self):
        if not self.axes:
            return ""
        gs = self._compute_group_spacing()
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