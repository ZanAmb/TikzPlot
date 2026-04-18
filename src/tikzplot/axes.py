import numpy as _np
import matplotlib.pyplot as _plt

from .elements import Graph
from .config import TikzConfig
from .state import _next_imshow_num, main_name
from .latex_special import tex_text

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

        self._add_legend = ""

    def _plot(self, x, y, settings=None, xerr=None, yerr=None, **style):
        e = Graph(self, (x, y), settings, xerr=xerr, yerr=yerr, **style)
        self._elements.append(e)
        return e

    def _check_kwargs(self, func, allowed, **kwargs):
        blacklist = set(kwargs) - allowed
        for b in blacklist:
            raise Warning(f"Ignoring unknown kwarg for {func}: {b}")
        return {k: v for k, v in kwargs.items() if k in allowed}

    def plot(self, *args, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("plot", kws, **kwargs)
        if len(args) == 1:
            y = args[0]
            return self._plot(range(len(y)), y, **kwargs)
        elif len(args) == 2:
            x, y = args
            return self._plot(x, y, **kwargs)
        else:
            x,y,fmt = args[:3]
            return self._plot(x,y,fmt=fmt, **kwargs)

    def scatter(self, x, y, *args, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "marker", "markersize", "s", "label"}
        kwargs = self._check_kwargs("scatter", kws, **kwargs)

        if "s" in kwargs:
            kwargs["ms"] = kwargs.pop("s")

        return self._plot(x, y, **kwargs, ls="")

    def semilogy(self, x, y, *args, **kwargs):
        kws = {"fmt", "base", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("semilogy", kws, **kwargs)
        self._axis_options["ymode"] = "log"
        if "base" in kwargs:
            self._axis_options["log basis y"] = kwargs["base"]
        return self._plot(x, y, **kwargs)

    def errorbar(self, x, y, *args, **kwargs):
        kws = {"xerr", "yerr", "fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("errorbar", kws, **kwargs)
        if len(args) == 1:
            return self._plot(x, y, **kwargs, yerr=args[0])
        elif len(args) == 2:
            return self._plot(x, y, **kwargs, yerr=args[0], fmt=args[1])
        else:
            return self._plot(x, y, **kwargs)

    def stem(self, *args, **kwargs):
        kws = {"orientation", "linefmt", "markerfmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("stem", kws, **kwargs)
        if "linefmt" in kwargs:
            kwargs["fmt"] = kwargs.pop("linefmt")
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
            return self._plot(x,y,settings=["ycomb"], **kwargs)
        else:
            return self._plot(y,x,settings=["xcomb"], **kwargs)

    def fill_between(self, x, y1, y2=None, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "label"}
        kwargs = self._check_kwargs("fill_between", kws, **kwargs)
        def _check_instance(xs, ys, pname):
            for el in self._elements:
                if el._check_equal(xs,ys):
                    return el._try_set_pname(pname)
                else:
                    return None
        name1 = self._fig._get_free_path_name()
        name2 = self._fig._get_free_path_name()
        if isinstance(y1, (int, float)):
            y1 = _np.asarray([y1] * len(x))
        inst = _check_instance(x,y1,name1)
        if inst is None:
            self._plot(x,y1,path_name=name1, alpha=0)
        else:
            name1 = inst

        if y2 is not None:
            if isinstance(y1, (int, float)):
                y2 = _np.asarray([y2] * len(x))
            inst = _check_instance(x,y2,name2)
            if inst is None:
                self._plot(x,y2,path_name=name2, alpha=0)
            else:
                name2 = inst
        else:
            xs = [min(x), max(x)]
            ys = [0,0]
            inst = _check_instance(xs,ys,name2)
            if inst is None:
                self._plot(xs,ys,path_name=name2, alpha=0)
            else:
                name2 = inst
        e = Graph(self, f"fill between [of={name1} and {name2}]",settings=None, xerr=None, yerr=None, **kwargs)
        self._elements.append(e)
        return e
        
    def hlines(self, y, xmin, xmax, colors="k", linestyles="solid", **kwargs):
        kws = {"label"}
        kwargs = self._check_kwargs("hlines", kws, **kwargs)
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
                return self._plot([xmins[i], xmaxs[i]], [ys[i]]*2, None, None, None, c=colorss[i], ls=lss[i], label=kwargs["label"])
            else:
                return self._plot([xmins[i], xmaxs[i]], [ys[i]]*2, None, None, None, c=colorss[i], ls=lss[i])

    def hist(self, x, bins=10, density=False,**kwargs):
        #kws = {"alpha", "color", "c", "label"}
        #kwargs = self._check_kwargs("hist", kws, **kwargs)
        try:
            iter(x)
            iter(x[0])
            datasets = x
        except:
            datasets = [x]
        all_data = _np.concatenate(datasets)
        edges = _np.histogram_bin_edges(all_data, bins=bins)
        for data in datasets:
            counts, _ = _np.histogram(data, edges, density=density)
            centers = (edges[:-1] + edges[1:]) / 2
        widths = edges[1:] - edges[:-1]
        settings = []
        if "orientation" in kwargs and kwargs["orientation"] == "horizontal":
            settings.append("xbar")
        else:
            settings.append("ybar")
        settings.append("fill")
        if "rwidth" in kwargs:
            settings.append(f"bar width={widths.mean()*kwargs['rwidth']}")
        else:
            settings[0] += " interval"
        if "range" in kwargs:
            if settings[0] == "xbar":
                self.set_ylim(kwargs["range"])
            else:
                self.set_xlim(kwargs["range"])
        if "cumulative" in kwargs and kwargs["cumulative"]:
            counts = _np.cumsum(counts)

        return self._plot(centers, counts, settings=settings, **kwargs)

    def set_ylabel(self, label):
        self._axis_options["ylabel"] = f"{{{tex_text(label)}}}"

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

    def set_yscale(self, *args, **kwargs):
        kws = {"base"}
        kwargs = self._check_kwargs("set_yscale", kws, **kwargs)
        if "log" in args:
            self._axis_options["ymode"] = "log"
        if "base" in kwargs:
            self._axis_options["log basis y"] = kwargs["base"]

    def set_yticks(self, ticks, labels=None):
        if ticks:
            s_ticks = map(str, ticks)
            self._axis_options["ytick"]=f"{{{','.join(s_ticks)}}}"
            if labels and len(labels)==len(ticks):
                self._axis_options["yticklabels"]=f"{{{tex_text(','.join(labels))}}}"
            elif labels is not None and len(labels) == 0:
                self._axis_options["yticklabels"]=r"{}"
        else:
            self._axis_options["yticks"]=r"{}"
            self._yticks = False

    def set_yticklabels(self, labels):
        if labels:
            self._axis_options["yticklabels"]=f"{{{tex_text(','.join(labels))}}}"
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
        if "ncols" in kwargs:
            self._axis_options["legend columns"] = kwargs["ncols"]
        if len(args) == 2:
            self._add_legend = args
        elif len(args) == 1:
            labs = args[0]
            if len(labs) > len(self._elements):
                print("Legend: more labels than elements")
            else:
                for i in range(len(labs)):
                    self._elements[i]._set_label(tex_text(labs[i]))

    def _add_legend_entries(self):
        if self._add_legend == "": return ""
        axs, labs = self._add_legend
        output = ""
        if len(axs) != len(labs):
            print("Legend: different number of plots and labels, ignoring.")
            return ""
        for i in range(len(axs)):
            output += f"\n\\addlegendimage{{{axs[i]._style_string()}}}"
            output += f"\n\\addlegendentry{{{tex_text(labs[i])}}}"
        return output
        
    def _content_tex(self, filename):
        ouptut = "\n".join(e._to_tex(filename) for e in self._elements)
        ouptut += self._add_legend_entries()
        return ouptut
    
    def _get_hard_range(self,which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self._axis_options:
            mode = self._axis_options[arg]
        if which in self._axis_options:
            for e in self._elements:
                e._filter(which, self._axis_options[which])
            return (self._axis_options[which], mode)
        return None, mode
    
    def _get_range(self, which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self._axis_options:
            mode = self._axis_options[arg]
        if which in self._axis_options:
            for e in self._elements:
                e._filter(which, self._axis_options[which])
            return (self._axis_options[which], True, mode)
        if "min" in which:
            return (min([e._get_erange(which) for e in self._elements]), False, mode)
        return (max([e._get_erange(which) for e in self._elements]), False, mode)
    
    def _get_limit(self, which):
        arg = f"{which[0]}mode"
        mode = "lin"
        base = 10
        if arg in self._axis_options:
            mode = self._axis_options[arg]
            arg = f"log basis {which[0]}"
            if arg in self._axis_options:
                base = self._axis_options[arg]
        if which in self._axis_options:
            return self._axis_options[which], mode, base
        else: return None, mode, base

    def _set_range(self, which, value):
        self._axis_options[which] = value
        for e in self._elements:
            e._filter(which, value)

    def _num_points(self):
        return [e._num_points() for e in self._elements]
    
    def _reduce_points(self, limit):
        for e in self._elements:
            e._reduce_points(limit)

    def _add_col(self, r,g,b):
        self._fig._add_col(r,g,b)

    def set(self, **kwargs):
        defined = {"ylim": self.set_ylim, "ylabel": self.set_ylabel, "yscale": self.set_yscale, "yticklabels": self.set_yticklabels, "yticks": self.set_yticks}
        for attr in defined:
            if attr in kwargs:
                defined[attr](kwargs.pop(attr))

class Axes(BaseAxes):

    def __init__(self, nrows, ncols, index, fig, polar):
        super().__init__()
        self._left = False
        self._neigh = None
        
        self._nrows = nrows
        self._ncols = ncols
        self._index = index - 1
        self._row = self._index // self._ncols
        self._col = self._index - self._row * self._ncols

        self._fig = fig
        self._imshow = None

        self._defcol_counter = 0
        self._colorbar = ""
        self._cbar_h = False
        self._polar = polar

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

        self._axis_options["alias" if TikzConfig.USE_GROUPPLOTS else "name"] = f"p{index-1}"
        pos = _posit_string()
        if pos is not None and not TikzConfig.USE_GROUPPLOTS:
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

    def loglog(self, x, y, *args, **kwargs):
        kws = {"base", "fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("loglog", kws, **kwargs)
        self._axis_options["xmode"] = "log"
        self._axis_options["ymode"] = "log"
        if "base" in kwargs:
            base = kwargs["base"]
            self._axis_options["log basis x"] = base
            self._axis_options["log basis y"] = base
        return self._plot(x, y, **kwargs)

    def semilogx(self, x, y, *args, **kwargs):
        kws = {"base", "fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("semilogx", kws, **kwargs)
        self._axis_options["xmode"] = "log"
        if "base" in kwargs:
            self._axis_options["log basis x"] = kwargs["base"]
        return self._plot(x, y, **kwargs)

    def vlines(self, x, ymin, ymax, colors="k", linestyles="solid", **kwargs):
        kws = {"label"}
        kwargs = self._check_kwargs("vlines", kws, **kwargs)
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
                return self._plot([xs[i]]*2, [ymins[i], ymaxs[i]], None, None, None, c=colorss[i], ls=lss[i], label=kwargs["label"])
            else:
                return self._plot([xs[i]]*2, [ymins[i], ymaxs[i]], None, None, None, c=colorss[i], ls=lss[i])

    def imshow(self, *args, **kwargs):
        #kws = {"fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        #kwargs = self._check_kwargs("imshow", kws, **kwargs)
        self._imshow = (args, kwargs)
        self._axis_args.add("axis on top")
        self._axis_options["enlargelimits"] = "false"
        #self._fig._add_global("\\pgfplotsset{set layers}")
        data = args[0]
        m, M = _np.min(data), _np.max(data)
        if "cmap" in kwargs:
            cmap = kwargs["cmap"]
        else:
            cmap = "viridis"
        return (self, cmap, m, M)
    
    def set_xlabel(self, label):
        self._axis_options["xlabel"] = f"{{{tex_text(label)}}}"

    def set_title(self, title):
        self._axis_options["title"] = f"{{{tex_text(title)}}}"

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

    def set_xscale(self, *args, **kwargs):
        kws = {"base"}
        kwargs = self._check_kwargs("set_xscale", kws, **kwargs)
        if "log" in args:
            self._axis_options["xmode"] = "log"
        if "base" in kwargs:
            self._axis_options["log basis x"] = kwargs["base"]

    def set_xticks(self, ticks, labels=None):
        if ticks:
            s_ticks = map(str, ticks)
            self._axis_options["xtick"]=f"{{{','.join(s_ticks)}}}"
            if labels and len(labels)==len(ticks):
                self._axis_options["xticklabels"]=f"{{{tex_text(','.join(labels))}}}"
            elif labels is not None and len(labels) == 0:
                self._axis_options["xticklabels"]=r"{}"
        else:
            self._axis_options["xticks"]=r"{}"
            self._xticks = False

    def set_xticklabels(self, labels):
        if labels:
            self._axis_options["xticklabels"]=f"{{{tex_text(','.join(labels))}}}"
        else:
            self._axis_options["xticklabels"]=r"{}"

    def twinx(self):
        if self._polar:
            raise Exception("Cannot create twinx() on polar plot.")
        self._secondary_y = Secondary(self)
        return self._secondary_y
    
    def _export_imshow(self, *args, **kwargs):
        if "xmode" in self._axis_options and self._axis_options["xmode"] == "log":
            base = 10
            if "log basis x" in self._axis_options:
                base = self._axis_options["log basis x"]
            _plt.xscale("log", base=base)
        if "ymode" in self._axis_options and self._axis_options["ymode"] == "log":
            base = 10
            if "log basis y" in self._axis_options:
                base = self._axis_options["log basis y"]
            _plt.yscale("log", base=base)
        _plt.axis("off")
        _plt.imshow(*args, **kwargs)
        im_name = f"{str(main_name()[1]).removesuffix('.py')}_{TikzConfig.IMSHOW_SAVENAME}{_next_imshow_num()}.pdf"
        _plt.savefig(im_name,bbox_inches='tight', pad_inches=0)
        return im_name

    def _axis_option_string(self):
        self._update_size()
        if self._width:
            self._axis_options["width"] = self._width
        if self._height:
            self._axis_options["height"] = self._height
        if not TikzConfig.USE_GROUPPLOTS:
            if self._left:
                self._axis_options["yshift"] = f"-{self._fig._get_spacing(self._row, self._col)}cm"
            else:
                self._axis_options["xshift"] = f"{self._fig._get_spacing(self._row, self._col)}cm"
        if self._imshow:
            im_name = self._export_imshow(*self._imshow[0], **self._imshow[1]).replace(r"\\", r"/")
            dims = _np.shape(self._imshow[0][0])
            bounds = [0, dims[1], 0, dims[0]]
            if "extent" in self._imshow[1]:
                bounds = self._imshow[1]["extent"]
            xm, xM, ym, yM = bounds
            self._elements.insert(0, Graph(self, f"graphics [xmin={xm}, xmax={xM}, ymin={ym}, ymax={yM}] {{{im_name}}}",settings=None, xerr=None, yerr=None, onlayer="axis background"))
        axis_opt_str = ""
        if self._axis_args:
            axis_opt_str += ",\n".join(self._axis_args)
        if TikzConfig.SCHOOL_AXIS:
            axis_opt_str += f",\n axis lines=middle,\n xlabel style={{at={{(ticklabel* cs:{1+TikzConfig.SCHOOL_AXIS_LABEL_MARGIN})}},anchor=north}},\n ylabel style={{at={{(ticklabel* cs:{1+TikzConfig.SCHOOL_AXIS_LABEL_MARGIN})}},anchor=east}},"
        if self._axis_options:
            if axis_opt_str: axis_opt_str += ",\n"
            axis_opt_str += ",\n".join(f"{k}={v}" for k, v in self._axis_options.items())
        axis_opt_str += self._colorbar
        return axis_opt_str

    
    def _margins(self):
        left = TikzConfig.LEFT_PADDING * self._yticks + TikzConfig.Y_LABEL_PADDING * ("ylabel" in self._axis_options)
        right = TikzConfig.RIGHT_PADDING + TikzConfig.CBAR_X_MARGIN * (self._colorbar != "" and not self._cbar_h)
        top = TikzConfig.TOP_PADDING + TikzConfig.TITLE_PADDING * ("title" in self._axis_options)
        bottom = TikzConfig.BOTTOM_PADDING * self._xticks + TikzConfig.X_LABEL_PADDING * ("xlabel" in self._axis_options) + TikzConfig.CBAR_Y_MARGIN * (self._colorbar != "" and self._cbar_h)
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
    def _get_defcol(self):
        self._defcol_counter += 1
        return self._defcol_counter - 1
    def _show_colorbar(self, cbar, horizontal=False):
        self._colorbar = ",\n" + cbar
        self._cbar_h = horizontal
    def _get_index(self):
        return self._index
    
    def _to_tex(self, filename):
        lines = []
        lines2 = []
        if TikzConfig.USE_GROUPPLOTS:
            lines.append("\\nextgroupplot")
        if self._polar:
            lines.append("\\begin{polaraxis}")
        elif not TikzConfig.USE_GROUPPLOTS:
            lines.append("\\begin{axis}")
        lines.append(f"[{self._axis_option_string()}]")
        lines.append(self._content_tex(filename))
        if self._polar:
            lines.append("\\begin{polaraxis}")
        elif not TikzConfig.USE_GROUPPLOTS:
            lines.append("\\end{axis}")
        if self._secondary_y is not None:
            lines2.append("\\begin{axis}")
            lines2.append(f"[{self._secondary_y._axis_option_string()}]")
            lines2.append(self._secondary_y._content_tex(filename))
            lines2.append("\\end{axis}")
        return lines, lines2

    def set(self, **kwargs):
        defined = {"title": self.set_title, "xlim": self.set_xlim, "xlabel": self.set_xlabel, "xscale": self.set_xscale, "xticklabels": self.set_xticklabels, "xticks": self.set_xticks}
        for attr in defined:
            if attr in kwargs:
                defined[attr](kwargs.pop(attr))

        super().set(**kwargs)
    
class Secondary(BaseAxes):
    def __init__(self, primary):
        super().__init__()
        self._primary = primary

        self._axis_options["axis y line*"] = "right"
        self._axis_options["axis x line"] = "none"
        self._axis_options["at"] = f"{{({primary._axis_options['alias' if 'alias' in primary._axis_options else 'name']}.south west)}}"
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
    
    def _get_defcol(self):
        return self._primary._get_defcol()
    
    def _get_index(self):
        return self._primary._get_index()