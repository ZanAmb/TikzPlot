from .elements import Graph
from .config import TikzConfig

class BaseAxes:
    def __init__(self):
        self.elements = []
        self.axis_options = {}
        self.axis_args = set()
        self.legend_on = False

        if TikzConfig.USE_DECIMAL_COMMA:
            self.axis_args.add("/pgf/number format/use comma")

    def _plot(self, x, y, *, xerr=None, yerr=None, **style):
        self.elements.append(Graph(self, x, y, xerr=xerr, yerr=yerr, **style))

    def plot(self, *args, **kwargs):
        if len(args) == 1:
            y = args[0]
            self._plot(range(len(y)), y, **kwargs)
        elif len(args) == 2:
            x, y = args
            self._plot(x, y, **kwargs)
        else:
            x,y,fmt = args[:3]
            self._plot(x,y,fmt=fmt, **kwargs)

    def scatter(self, x, y, *args, **kwargs):
        self._plot(x, y, **kwargs, ls="")


    def semilogy(self, x, y, *args, **kwargs):
        self.axis_options["ymode"] = "log"
        self._plot(x, y, **kwargs)

    def errorbar(self, x, y, *args, **kwargs):
        self._plot(x, y, **kwargs)

    def set_ylabel(self, label):
        self.axis_options["ylabel"] = f"{{{label}}}"

    def set_ylim(self, *args, **kwargs):
        bottom = None
        top = None

        if len(args) == 1:
            bottom, top = args[0]
        elif len(args) == 2:
            bottom, top = args
        elif len(args) > 2:
            raise ValueError("set_ylim accepts at most 2 positional arguments")

        if "bottom" in kwargs:
            bottom = kwargs["bottom"]
        if "top" in kwargs:
            top = kwargs["top"]

        if bottom is not None:
            self.axis_options["ymin"] = bottom
        if top is not None:
            self.axis_options["ymax"] = top

    LEGEND_LOC_MAP = ["best", "upper right", "upper left", "lower_left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center"]
    ANCHOR_MAP = {"top": "north", "bottom": "south", "upper": "north", "lower": "south", "left": "west", "right": "east", "center": "center"}

    def legend(self, *args, **kwargs):
        if "loc" in kwargs:
            loc = kwargs["loc"]
            lx = ly = posit = None
            if isinstance(loc, tuple):
                try:
                    lx,ly=float(loc[0]), float(loc[1])
                    posit = "south west"
                except: print(f"Error parsing legend location: {loc}")
            else:
                if isinstance(loc, int):
                    loc = self.LEGEND_LOC_MAP[loc]
                posit = " ".join([self.ANCHOR_MAP[k] for k in self.ANCHOR_MAP if k in str(loc)])
                if "center" in posit:
                    if "north" in posit or "south" in posit or "west" in posit or "east" in posit:
                        posit = posit.replace("center", "")
                lx, ly = 0.5, 0.5
                if "north" in posit:
                    ly = 1 - TikzConfig.LEGEND_REL_Y
                elif "south" in posit:
                    ly = TikzConfig.LEGEND_REL_Y
                if "west" in posit:
                    lx = TikzConfig.LEGEND_REL_X
                elif "east" in posit:
                    lx = 1 - TikzConfig.LEGEND_REL_X

            legend_string = []
            if lx is not None and ly is not None:
                legend_string.append(r"at={(" + f"{lx},{ly}" + r")}")
            if len(posit):
                legend_string.append(r"anchor=" + posit)
            else: print(posit)
            self.axis_options["legend style"] = f"{{{','.join(legend_string)}}}"
        self.legend_on = True            
        
    def content_tex(self):
        return "\n".join(e.to_tex() for e in self.elements)

class Axes(BaseAxes):

    def __init__(self, nrows, ncols, index, fig):
        super().__init__()
        self.fig = fig
        self.left = False
        self.neigh = None
        def posit_string(): # returns neighbour, neighbour corner, anchor
            i = index - 1
            if i == 0:
                return None
            row = i // ncols
            col = i - row * ncols
            if col == 0:
                self.neigh = i - ncols
                self.left = True
                return self.neigh, "south", "north"
            self.neigh = i - 1
            return self.neigh, "east", "west"
        
        self.nrows = nrows
        self.ncols = ncols
        self.index = index

        self.axis_options["name"] = f"p{index-1}"
        pos = posit_string()
        if pos is not None:
            self.axis_options["at"] = f"{{(p{self.neigh}.{pos[1]})}}"
            self.axis_options["anchor"] = pos[2]

        self.secondary_y = None

        self.width = None
        self.height = None
        if fig.width:
            self.width= f"{fig.width / ncols}cm"
        if fig.height:
            self.height = f"{fig.height / nrows}cm"


    def _update_size(self):
        if self.fig.width:
            self.width= f"{self.fig.width / self.ncols}cm"
        if self.fig.height:
            self.height = f"{self.fig.height / self.nrows}cm"

    def loglog(self, x, y, *args, **kwargs):
        self.axis_options["xmode"] = "log"
        self.axis_options["ymode"] = "log"
        self._plot(x, y, **kwargs)

    def semilogx(self, x, y, *args, **kwargs):
        self.axis_options["xmode"] = "log"
        self._plot(x, y, **kwargs)

    def set_xlabel(self, label):
        self.axis_options["xlabel"] = f"{{{label}}}"


    def set_title(self, title):
        self.axis_options["title"] = f"{{{title}}}"

    def grid(self, visible=True, which="major"):

        if not visible:
            self.axis_options["grid"] = "none"
            return

        if which == "major":
            self.axis_options["grid"] = "major"

        elif which == "minor":
            self.axis_options["minor grid style"] = "{dotted}"
            self.axis_options["grid"] = "both"

        elif which == "both":
            self.axis_options["grid"] = "both"

    def set_xlim(self, *args, **kwargs):
        left = None
        right = None

        if len(args) == 1:
            left, right = args[0]
        elif len(args) == 2:
            left, right = args
        elif len(args) > 2:
            raise ValueError("set_xlim accepts at most 2 positional arguments")

        if "left" in kwargs:
            left = kwargs["left"]
        if "right" in kwargs:
            right = kwargs["right"]

        if left is not None:
            self.axis_options["xmin"] = left
        if right is not None:
            self.axis_options["xmax"] = right

    def twinx(self):
        self.secondary_y = Secondary(self)
        return self.secondary_y

    def axis_option_string(self, gs):
        if self.width:
            self.axis_options["width"] = self.width
        if self.height:
            self.axis_options["height"] = self.height
        if self.left:
            self.axis_options["yshift"] = gs[1]
        else:
            self.axis_options["xshift"] = gs[0]
        axis_opt_str = ""
        if self.axis_args:
            axis_opt_str += ",\n".join(self.axis_args)
        if self.axis_options:
            if axis_opt_str: axis_opt_str += ",\n"
            axis_opt_str += ",\n".join(f"{k}={v}" for k, v in self.axis_options.items())
        return axis_opt_str

    
    def margins(self):
        left = TikzConfig.LEFT_PADDING + TikzConfig.Y_LABEL_PADDING * ("ylabel" in self.axis_options)
        right = TikzConfig.RIGHT_PADDING
        top = TikzConfig.TOP_PADDING + TikzConfig.TITLE_PADDING * ("title" in self.axis_options)
        bottom = TikzConfig.BOTTOM_PADDING + TikzConfig.X_LABEL_PADDING * ("xlabel" in self.axis_options)

        if self.secondary_y is not None:
            right += self.secondary_y.padding()

        return left, right, top, bottom
    
class Secondary(BaseAxes):
    def __init__(self, primary):
        super().__init__()
        self.primary = primary

        self.axis_options["axis y line*"] = "right"
        self.axis_options["axis x line"] = "none"
        self.axis_options["at"] = f"{{({primary.axis_options["name"]}.south west)}}"
        self.axis_options["anchor"] = "south west"
        self.axis_options["y label style"] = r"{at={(1.1,0.5)}, rotate=180}"

    def loglog(self, x, y, *args, **kwargs):
        self.axis_options["xmode"] = "log"
        self.axis_options["ymode"] = "log"
        self._plot(x, y, **kwargs)

    def axis_option_string(self):
        if self.primary.width:
            self.axis_options["width"] = self.primary.width
        if self.primary.height:
            self.axis_options["height"] = self.primary.height
        axis_opt_str = ""
        if self.axis_args:
            axis_opt_str += ",\n".join(self.axis_args)
        if self.axis_options:
            if axis_opt_str: axis_opt_str += ",\n"
            axis_opt_str += ",\n".join(f"{k}={v}" for k, v in self.axis_options.items())
        return axis_opt_str
    
    def padding(self):
        return TikzConfig.SEC_Y_PADDING + TikzConfig.SEC_Y_LABEL_PADDING * ("ylabel" in self.axis_options)