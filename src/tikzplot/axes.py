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

    def _plot(self, x, y, settings=None, xerr=None, yerr=None, **style):
        self.elements.append(Graph(self, x, y, settings, xerr=xerr, yerr=yerr, **style))

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

    def semilogy(self, x, y, *args, base=10, **kwargs):
        self.axis_options["ymode"] = "log"
        self.axis_options["log basis y"] = base
        self._plot(x, y, **kwargs)

    def errorbar(self, x, y, *args, **kwargs):
        if len(args) == 1:
            self._plot(x, y, **kwargs, yerr=args[0])
        elif len(args) == 2:
            self._plot(x, y, **kwargs, yerr=args[0], fmt=args[1])
        else:
            self._plot(x, y, **kwargs)

    def stem(self, *args, **kwargs):
        vert = True
        if len(args) == 1:
            y = args[0]
            x = range(len(y))
        elif len(args) == 2:
            x,y=args
        elif len(args) == 3:
            x,y,fmt=args
            kwargs["fmt"]=fmt
        if "orientation" in kwargs:
            o = kwargs.pop("orientation")
            if o == "horizontal":
                vert = False
        if vert:
            self._plot(x,y,settings=["ycomb"], **kwargs)
        else:
            self._plot(x,y,settings=["xcomb"], **kwargs)
    def set_ylabel(self, label):
        self.axis_options["ylabel"] = f"{{{label}}}"

    def set_ylim(self, *args, **kwargs):
        bottom = None
        top = None
        for k in kwargs:
            if k not in ["bottom", "top"]:
                print(f"Invalid argument {kwargs.pop(k)} in ylim")

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

    def set_yscale(self, *args):
        if "log" in args:
            self.axis_options["ymode"] = "log"

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
    
    """def get_ranges(self):
        xm = xM = ym = yM = None
        if "xmin" in self.axis_options:
            xm = (self.axis_options["xmin"], True)
        else:
            xm = (min([e.get_range("xmin") for e in self.elements]), False)
        if "xmax" in self.axis_options:
            xM = (self.axis_options["xmax"], True)
        else:
            xM = (max([e.get_range("xmax") for e in self.elements]), False)
        if "ymin" in self.axis_options:
            ym = (self.axis_options["ymin"], True)
        else:
            ym = (min([e.get_range("ymin") for e in self.elements]), False)
        if "ymax" in self.axis_options:
            yM = (self.axis_options["ymax"], True)
        else:
            yM = (max([e.get_range("ymax") for e in self.elements]), False)
        return xm, xM, ym, yM"""
    
    def get_hard_range(self,which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self.axis_options:
            mode = self.axis_options[arg]
        if which in self.axis_options:
            for e in self.elements:
                e.filter(which, self.axis_options[which])
            return (self.axis_options[which], mode)
        return None, mode
    
    def get_range(self, which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self.axis_options:
            mode = self.axis_options[arg]
        if which in self.axis_options:
            for e in self.elements:
                e.filter(which, self.axis_options[which])
            return (self.axis_options[which], True, mode)
        if "min" in which:
            return (min([e.get_erange(which) for e in self.elements]), False, mode)
        return (max([e.get_erange(which) for e in self.elements]), False, mode)
    
    def set_range(self, which, value):
        self.axis_options[which] = value
        for e in self.elements:
            e.filter(which, value)

class Axes(BaseAxes):

    def __init__(self, nrows, ncols, index, fig):
        super().__init__()
        self.fig = fig
        self.left = False
        self.neigh = None
        
        self.nrows = nrows
        self.ncols = ncols
        self.index = index - 1
        self.row = self.index // self.ncols
        self.col = self.index - self.row * self.ncols

        def posit_string(): # returns neighbour, neighbour corner, anchor
            i = self.index
            if i == 0:
                return None
            if self.col == 0:
                self.neigh = i - self.ncols
                self.left = True
                return self.neigh, "south", "north"
            self.neigh = i - 1
            return self.neigh, "east", "west"

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

    def loglog(self, x, y, *args, base=10, **kwargs):
        self.axis_options["xmode"] = "log"
        self.axis_options["ymode"] = "log"
        self.axis_options["log basis x"] = base
        self.axis_options["log basis y"] = base
        self._plot(x, y, **kwargs)

    def semilogx(self, x, y, *args, base=10, **kwargs):
        self.axis_options["xmode"] = "log"
        self.axis_options["log basis x"] = base
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
        for k in kwargs:
            if k not in ["left", "right"]:
                print(f"Invalid argument {kwargs.pop(k)} in ylim")

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

    def set_xscale(self, *args):
        if "log" in args:
            self.axis_options["xmode"] = "log"

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