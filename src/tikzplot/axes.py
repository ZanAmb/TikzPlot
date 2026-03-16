import numpy as np

from .elements import Graph
from .config import TikzConfig

class BaseAxes:
    def __init__(self):
        self._elements = []
        self._axis_options = {}
        self._axis_args = set()
        self._legend_on = False
        self._yticks = True
        self._fig = None

        if TikzConfig.USE_DECIMAL_COMMA:
            self._axis_args.add("/pgf/number format/use comma")

    def _plot(self, x, y, settings=None, xerr=None, yerr=None, **style):
        self._elements.append(Graph(self, (x, y), settings, xerr=xerr, yerr=yerr, **style))

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
        self._axis_options["ymode"] = "log"
        self._axis_options["log basis y"] = base
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

    def fill_between(self, x, y1, y2=None, **kwargs):
        def _check_instance(xs, ys, pname):
            for el in self._elements:
                if el._check_equal(xs,ys):
                    return el._try_set_pname(pname)
                else:
                    return None
        name1 = self._fig._get_free_path_name()
        name2 = self._fig._get_free_path_name()
        if isinstance(y1, (int, float)):
            y1 = np.asarray([y1] * len(x))
        inst = _check_instance(x,y1,name1)
        if inst is None:
            self._plot(x,y1,path_name=name1, opacity=0)
        else:
            name1 = inst

        if y2 is not None:
            if isinstance(y1, (int, float)):
                y2 = np.asarray([y2] * len(x))
            inst = _check_instance(x,y2,name2)
            if inst is None:
                self._plot(x,y2,path_name=name2, opacity=0)
            else:
                name2 = inst
        else:
            xs = [min(x), max(x)]
            ys = [0,0]
            inst = _check_instance(xs,ys,name2)
            if inst is None:
                self._plot(xs,ys,path_name=name2, opacity=0)
            else:
                name2 = inst
        self._elements.append(Graph(self, f"fill between [of={name1} and {name2}]",settings=None, xerr=None, yerr=None, **kwargs))
        
    def hlines(self, y, xmin, xmax, colors="k", linestyles="solid", **kwargs):
        def _pad_or_truncate(some_list, target_len):
            return some_list[:target_len] + [some_list[-1]]*(target_len - len(some_list))
        def _to_list(x):
            if x is None:
                return []
            if isinstance(x, (int, float, str)):
                return [x]
            return list(x)
        ys = _to_list(y)
        xmins = _pad_or_truncate(_to_list(xmin), len(ys))
        xmaxs = _pad_or_truncate(_to_list(xmax), len(ys))
        colorss = _pad_or_truncate(_to_list(colors), len(ys))
        lss = _pad_or_truncate(_to_list(linestyles), len(ys))
        for i in range(len(ys)):
            if i == 0 and "label" in kwargs:
                self._plot([xmins[i], xmaxs[i]], [ys[i]]*2, None, None, None, c=colorss[i], ls=lss[i], label=kwargs["label"])
            else:
                self._plot([xmins[i], xmaxs[i]], [ys[i]]*2, None, None, None, c=colorss[i], ls=lss[i])

    def hist(self, x, bins=10, density=False,**kwargs):
        try:
            iter(x)
            iter(x[0])
            datasets = x
        except:
            datasets = [x]
        all_data = np.concatenate(datasets)
        edges = np.histogram_bin_edges(all_data, bins=bins)
        for data in datasets:
            counts, _ = np.histogram(data, edges, density=density)
            centers = (edges[:-1] + edges[1:]) / 2
        widths = edges[1:] - edges[:-1]
        settings = []
        if "orientation" in kwargs and kwargs["orientation"] == "horizontal":
            settings.append("xbar")
        else:
            settings.append("ybar")
        settings.append("fill")
        if "rwidth" in kwargs:
            settings.append(f"bar width={widths.mean()*kwargs["rwidth"]}")
        else:
            settings[0] += " interval"
        if "range" in kwargs:
            if settings[0] == "xbar":
                self.set_ylim(kwargs["range"])
            else:
                self.set_xlim(kwargs["range"])
        if "cumulative" in kwargs and kwargs["cumulative"]:
            counts = np.cumsum(counts)

        self._plot(centers, counts, settings=settings, **kwargs)

    def set_ylabel(self, label):
        self._axis_options["ylabel"] = f"{{{label}}}"

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
            self._axis_options["ymin"] = bottom
        if top is not None:
            self._axis_options["ymax"] = top

    def set_yscale(self, *args):
        if "log" in args:
            self._axis_options["ymode"] = "log"

    def set_yticks(self, ticks, labels=None):
        if ticks:
            s_ticks = map(str, ticks)
            self._axis_options["ytick"]=f"{{{','.join(s_ticks)}}}"
            if labels and len(labels)==len(ticks):
                self._axis_options["yticklabels"]=f"{{{','.join(labels)}}}"
            elif labels is not None and len(labels) == 0:
                self._axis_options["yticklabels"]=r"{}"
        else:
            self._axis_options["yticks"]=r"{}"
            self._yticks = False

    def set_yticklabels(self, labels):
        if labels:
            self._axis_options["yticklabels"]=f"{{{','.join(labels)}}}"
        else:
            self._axis_options["yticklabels"]=r"{}"

    _LEGEND_LOC_MAP = ["best", "upper right", "upper left", "lower_left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center"]
    _ANCHOR_MAP = {"top": "north", "bottom": "south", "upper": "north", "lower": "south", "left": "west", "right": "east", "center": "center"}

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
                    loc = self._LEGEND_LOC_MAP[loc]
                posit = " ".join([self._ANCHOR_MAP[k] for k in self._ANCHOR_MAP if k in str(loc)])
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
            self._axis_options["legend style"] = f"{{{','.join(legend_string)}}}"
        self._legend_on = True            
        
    def content_tex(self):
        return "\n".join(e.to_tex() for e in self._elements)
    
    """def get_ranges(self):
        xm = xM = ym = yM = None
        if "xmin" in self._axis_options:
            xm = (self._axis_options["xmin"], True)
        else:
            xm = (min([e.get_range("xmin") for e in self._elements]), False)
        if "xmax" in self._axis_options:
            xM = (self._axis_options["xmax"], True)
        else:
            xM = (max([e.get_range("xmax") for e in self._elements]), False)
        if "ymin" in self._axis_options:
            ym = (self._axis_options["ymin"], True)
        else:
            ym = (min([e.get_range("ymin") for e in self._elements]), False)
        if "ymax" in self._axis_options:
            yM = (self._axis_options["ymax"], True)
        else:
            yM = (max([e.get_range("ymax") for e in self._elements]), False)
        return xm, xM, ym, yM"""
    
    def get_hard_range(self,which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self._axis_options:
            mode = self._axis_options[arg]
        if which in self._axis_options:
            for e in self._elements:
                e.filter(which, self._axis_options[which])
            return (self._axis_options[which], mode)
        return None, mode
    
    def get_range(self, which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self._axis_options:
            mode = self._axis_options[arg]
        if which in self._axis_options:
            for e in self._elements:
                e.filter(which, self._axis_options[which])
            return (self._axis_options[which], True, mode)
        if "min" in which:
            return (min([e.get_erange(which) for e in self._elements]), False, mode)
        return (max([e.get_erange(which) for e in self._elements]), False, mode)
    
    def set_range(self, which, value):
        self._axis_options[which] = value
        for e in self._elements:
            e.filter(which, value)

class Axes(BaseAxes):

    def __init__(self, nrows, ncols, index, fig):
        super().__init__()
        self._left = False
        self._neigh = None
        
        self._nrows = nrows
        self._ncols = ncols
        self._index = index - 1
        self._row = self._index // self._ncols
        self._col = self._index - self._row * self._ncols

        self._fig = fig

        def _posit_string(): # returns neighbour, neighbour corner, anchor
            i = self._index
            if i == 0:
                return None
            if self._col == 0:
                self._neigh = i - self._ncols
                self._left = True
                return self._neigh, "south", "north"
            self._neigh = i - 1
            return self._neigh, "east", "west"

        self._axis_options["name"] = f"p{index-1}"
        pos = _posit_string()
        if pos is not None:
            self._axis_options["at"] = f"{{(p{self._neigh}.{pos[1]})}}"
            self._axis_options["anchor"] = pos[2]

        self._secondary_y = None

        self._width = None
        self._height = None
        if self._fig._get_width():
            self._width= f"{self._fig._get_width() / ncols}cm"
        if self._fig._get_height():
            self._height = f"{self._fig._get_height() / nrows}cm"

        self._xticks = True


    def _update_size(self):
        if self._fig._get_width():
            self._width= f"{self._fig._get_width() / self._ncols}cm"
        if self._fig._get_height():
            self._height = f"{self._fig._get_height() / self._nrows}cm"

    def loglog(self, x, y, *args, base=10, **kwargs):
        self._axis_options["xmode"] = "log"
        self._axis_options["ymode"] = "log"
        self._axis_options["log basis x"] = base
        self._axis_options["log basis y"] = base
        self._plot(x, y, **kwargs)

    def semilogx(self, x, y, *args, base=10, **kwargs):
        self._axis_options["xmode"] = "log"
        self._axis_options["log basis x"] = base
        self._plot(x, y, **kwargs)

    def vlines(self, x, ymin, ymax, colors="k", linestyles="solid", **kwargs):
        def _pad_or_truncate(some_list, target_len):
            return some_list[:target_len] + [some_list[-1]]*(target_len - len(some_list))
        def _to_list(x):
            if x is None:
                return []
            if isinstance(x, (int, float, str)):
                return [x]
            return list(x)
        xs = _to_list(x)
        ymins = _pad_or_truncate(_to_list(ymin), len(xs))
        ymaxs = _pad_or_truncate(_to_list(ymax), len(xs))
        colorss = _pad_or_truncate(_to_list(colors), len(xs))
        lss = _pad_or_truncate(_to_list(linestyles), len(xs))
        for i in range(len(xs)):
            if i == 0 and "label" in kwargs:
                self._plot([xs[i]]*2, [ymins[i], ymaxs[i]], None, None, None, c=colorss[i], ls=lss[i], label=kwargs["label"])
            else:
                self._plot([xs[i]]*2, [ymins[i], ymaxs[i]], None, None, None, c=colorss[i], ls=lss[i])

    def set_xlabel(self, label):
        self._axis_options["xlabel"] = f"{{{label}}}"

    def set_title(self, title):
        self._axis_options["title"] = f"{{{title}}}"

    def grid(self, visible=True, which="major"):

        if not visible:
            self._axis_options["grid"] = "none"
            return

        if which == "major":
            self._axis_options["grid"] = "major"

        elif which == "minor":
            self._axis_options["minor grid style"] = "{dotted}"
            self._axis_options["grid"] = "both"

        elif which == "both":
            self._axis_options["grid"] = "both"

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
            self._axis_options["xmin"] = left
        if right is not None:
            self._axis_options["xmax"] = right

    def set_xscale(self, *args):
        if "log" in args:
            self._axis_options["xmode"] = "log"

    def set_xticks(self, ticks, labels=None):
        if ticks:
            s_ticks = map(str, ticks)
            self._axis_options["xtick"]=f"{{{','.join(s_ticks)}}}"
            if labels and len(labels)==len(ticks):
                self._axis_options["xticklabels"]=f"{{{','.join(labels)}}}"
            elif labels is not None and len(labels) == 0:
                self._axis_options["xticklabels"]=r"{}"
        else:
            self._axis_options["xticks"]=r"{}"
            self._xticks = False

    def set_xticklabels(self, labels):
        if labels:
            self._axis_options["xticklabels"]=f"{{{','.join(labels)}}}"
        else:
            self._axis_options["xticklabels"]=r"{}"

    def twinx(self):
        self._secondary_y = Secondary(self, fig=self._fig)
        return self._secondary_y

    def _axis_option_string(self):
        self._update_size()
        if self._width:
            self._axis_options["width"] = self._width
        if self._height:
            self._axis_options["height"] = self._height
        if self._left:
            self._axis_options["yshift"] = f"-{self._fig._get_spacing(self._row, self._col)}cm"
        else:
            self._axis_options["xshift"] = f"{self._fig._get_spacing(self._row, self._col)}cm"
        axis_opt_str = ""
        if self._axis_args:
            axis_opt_str += ",\n".join(self._axis_args)
        if self._axis_options:
            if axis_opt_str: axis_opt_str += ",\n"
            axis_opt_str += ",\n".join(f"{k}={v}" for k, v in self._axis_options.items())
        return axis_opt_str

    
    def _margins(self):
        left = TikzConfig.LEFT_PADDING * self._yticks + TikzConfig.Y_LABEL_PADDING * ("ylabel" in self._axis_options)
        right = TikzConfig.RIGHT_PADDING
        top = TikzConfig.TOP_PADDING + TikzConfig.TITLE_PADDING * ("title" in self._axis_options)
        bottom = TikzConfig.BOTTOM_PADDING * self._xticks + TikzConfig.X_LABEL_PADDING * ("xlabel" in self._axis_options)
        if self._secondary_y is not None:
            right += self._secondary_y._padding()

        return left, right, top, bottom
    
    def _get_row(self):
        return self._row
    def _get_col(self):
        return self._col
    def _get_nrows(self):
        return self._nrows
    def _get_ncols(self):
        return self._ncols
    
class Secondary(BaseAxes):
    def __init__(self, primary):
        super().__init__()
        self._primary = primary

        self._axis_options["axis y line*"] = "right"
        self._axis_options["axis x line"] = "none"
        self._axis_options["at"] = f"{{({primary._axis_options["name"]}.south west)}}"
        self._axis_options["anchor"] = "south west"
        self._axis_options["y label style"] = r"{at={(1.1,0.5)}, rotate=180}"

        self._fig = primary._fig

    def _axis_option_string(self):
        if self._primary._width:
            self._axis_options["width"] = self._primary._width
        if self._primary._height:
            self._axis_options["height"] = self._primary._height
        axis_opt_str = ""
        if self._axis_args:
            axis_opt_str += ",\n".join(self._axis_args)
        if self._axis_options:
            if axis_opt_str: axis_opt_str += ",\n"
            axis_opt_str += ",\n".join(f"{k}={v}" for k, v in self._axis_options.items())
        return axis_opt_str
    
    def _padding(self):
        return TikzConfig.SEC_Y_PADDING + TikzConfig.SEC_Y_LABEL_PADDING * ("ylabel" in self._axis_options)