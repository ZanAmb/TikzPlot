from typing import Any, Iterable
import copy

import numpy as _np
import matplotlib.pyplot as _plt

from .elements import Graph3
from .texts import Text3
from .config import TikzConfig
from .colorbar import Colorbar
from .state import _next_imshow_num, main_name
from .latex_special import tex_text
from .colors import _tex_color

class Axes3:
    def __init__(self, nrows, ncols, index, fig):
        self._elements: dict[int, list] = {0: []}
        self._axis_options = {}
        self._axis_args = set()
        self._legend_on = False
        self._overlay_legend = False
        self._overlay_legend_entries = []
        self._overlay_special: dict[int, dict[str, Any]] = {}
        self._xticks = True
        self._yticks = True
        self._zticks = True
        self._fig = None
        if TikzConfig.USE_DECIMAL_COMMA:
            self._axis_args.add(f"/pgf/number format/.cd, use comma, 1000 sep={{{TikzConfig.THOUSANDS_SEP}}}")
        else:
            self._axis_args.add(f"/pgf/number format/.cd, 1000 sep={{{TikzConfig.THOUSANDS_SEP}}}")

        self._add_legend = []
        self._legend_lab_col: Any = None
        self._coordinates = {}
        self._cmap_bar = None

        self._ext_xmin = False
        self._ext_xmax = False
        self._ext_ymin = False
        self._ext_ymax = False
        self._ext_zmin = False
        self._ext_zmax = False

        self._int_xmin = None
        self._int_xmax = None
        self._int_ymin = None
        self._int_ymax = None
        self._int_zmin = None
        self._int_zmax = None

        self._preferred_lims = {}
        self._bar_labels = {}

        self._left = False
        self._neigh = None
        
        self._nrows = nrows
        self._ncols = ncols
        self._index = index - 1
        self._row = self._index // self._ncols
        self._col = self._index - self._row * self._ncols

        self._fig = fig
        self._style = self._fig._style
        
        self._defcol_counter = {0: 0}
        self._colorbar = ""
        self._cbar_h = False

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

        self._width = None
        self._height = None
        if self._fig._get_width():
            self._width= f"{self._fig._get_width() / ncols}cm"
        if self._fig._get_height():
            self._height = f"{self._fig._get_height() / nrows}cm"

        self._style_defaults()

    def _style_defaults(self):
        _gs = self._style._get_grid_cycle()
        if _gs is not None:
            self.grid(**_gs)
        _bcgnd = self._style._get_background_cycle()
        if _bcgnd is not None:
            self._axis_options["axis background/.style"] = f"{{{_bcgnd}}}"
        _add_settgs = self._style._get_additional_settings()
        if _add_settgs is not None:
            self._axis_options = _add_settgs | self._axis_options

    def _get_overlay(self):
        return sorted(self._elements.keys())[-1]
    def _get_all_elements(self):
        return [i for l in self._elements.values() for i in l]
    def _get_free_overlay(self):
        if len(self._elements[self._get_overlay()]) > 0:
            new_overlay = self._get_overlay() + 1
            self._elements[new_overlay] = []
            return new_overlay
        return self._get_overlay()
    def _add_overlay_legend_entry(self, entry):
        self._overlay_legend_entries.append(entry)
    def _get_element_overlay(self, element):
        for overlay, elements in self._elements.items():
            if element in elements:
                return overlay
        return None
    def _update_levels(self, which, new_level):
        if which not in self._preferred_lims:
            self._preferred_lims[which] = new_level
        else:
            if which in ["xmin", "ymin"]:
                self._preferred_lims[which] = min(self._preferred_lims[which], new_level)
            elif which in ["xmax", "ymax"]:
                self._preferred_lims[which] = max(self._preferred_lims[which], new_level)
    def _check_approximate_equal(self, a, b, tol=1e-5):
        return _np.count_nonzero(_np.abs(_np.asarray(a) - _np.asarray(b))/_np.max(_np.abs(b)) > tol) == 0

    def _update_axis_options(self, key, value):
        accepted = {"label style": (dict, " "), "tick style": (dict, " "), "tick label style": (dict, " "), "tick align": (str, "")}
        if isinstance(value, dict):
            value = value.copy()
        if key.startswith(("x", "y")):
            k = key.removeprefix("x").removeprefix("y").strip()
            set_ax = ("x" if key.startswith("x") else "y") + accepted[k][1]
            other_ax = ("y" if set_ax.strip() == "x" else "x") + accepted[k][1]
            if k not in accepted:
                self._axis_options[key] = value
            elif k in self._axis_options:
                if accepted[k][0] != type(value):
                    raise ValueError(f"Value for {key} must be of type {accepted[k][0].__name__}.")
                if accepted[k][0] == dict:
                    common_props = self._axis_options[k].copy()
                    setting_axis = {}
                    other_axis = {}
                    for vk in list(value.keys()).copy():
                        if vk in common_props:
                            if common_props[vk] == value[vk]:
                                value.pop(vk)
                            else:
                                other_axis[vk] = common_props.pop(vk)
                                self._axis_options[k].pop(vk)
                                setting_axis[vk] = value[vk]
                        else:
                            setting_axis[vk] = value[vk]
                    if other_axis:
                        if f"{other_ax}{k}" not in self._axis_options:
                            self._axis_options[f"{other_ax}{k}"] = {}
                        self._axis_options[f"{other_ax}{k}"].update(other_axis)
                    if setting_axis:
                        if f"{set_ax}{k}" not in self._axis_options:
                            self._axis_options[f"{set_ax}{k}"] = {}
                        self._axis_options[f"{set_ax}{k}"].update(setting_axis)
                    if common_props:
                        self._axis_options[k].update(common_props)
                elif accepted[k][0] == str:
                    if self._axis_options[k] != value:
                        self._axis_options[f"{set_ax}{k}"] = value
                        self._axis_options[f"{other_ax}{k}"] = self._axis_options.pop(k)                        
            else:
                if key not in self._axis_options and accepted[k][0] == dict:
                    self._axis_options[key] = {}
                if accepted[k][0] == dict:
                    self._axis_options[key].update(value)
                else:
                    self._axis_options[key] = value
        else:
            if key not in accepted:
                self._axis_options[key] = value
            elif accepted[key][0] != type(value):
                raise ValueError(f"Value for {key} must be of type {accepted[key][0].__name__}.")
            else:
                if "x" + accepted[key][1] + key in self._axis_options:
                    if accepted[key][0] == dict:
                        for vk in list(value.keys()).copy():
                            if vk in self._axis_options["x" + accepted[key][1] + key]:
                                self._axis_options["x" + accepted[key][1] + key].pop(vk)
                    elif accepted[key][0] == str:
                        self._axis_options.pop("x" + accepted[key][1] + key)
                if "y" + accepted[key][1] + key in self._axis_options:
                    if accepted[key][0] == dict:
                        for vk in list(value.keys()).copy():
                            if vk in self._axis_options["y" + accepted[key][1] + key]:
                                self._axis_options["y" + accepted[key][1] + key].pop(vk)
                    elif accepted[key][0] == str:
                        self._axis_options.pop("y" + accepted[key][1] + key)
                if key not in self._axis_options and accepted[key][0] == dict:
                    self._axis_options[key] = {}
                if accepted[key][0] == dict:
                    self._axis_options[key].update(value)
                self._axis_options[key] = value


    def _parse_entry(self, k, v):
        if v is None:
            return f"{k}"
        if isinstance(v, dict):
            return f"{k}={{" + ",\n".join(f"{kk}={vv}" for kk, vv in v.items() if vv != {}) + "}"
        return f"{k}={v}"

    def _plot(self, xs, ys, zs, zdir="z", settings={}, xerr=None, yerr=None, zerr=None, overlay=None, note=None, **style):
        spec = None
        if self._get_overlay() in self._overlay_special:
            spec = ",\n".join([self._parse_entry(k, v) for k, v in self._overlay_special[self._get_overlay()].items()])
        if note != spec:
            self._get_free_overlay()

        if isinstance(zs, (float,int)):
            zs = [zs] * len(xs)
        if zdir == "y":
            xs, ys, zs = ys, zs, xs
        elif zdir == "x":
            xs, ys, zs = zs, xs, ys
        e = Graph3(self, (xs, ys, zs), settings, xerr=xerr, yerr=yerr, zerr=zerr, **style)
        if overlay is None:
            overlay = self._get_overlay()
        self._elements[overlay].append(e)
        return e

    def _check_kwargs(self, func, allowed, **kwargs):
        blacklist = set(kwargs) - allowed
        for b in blacklist:
            raise Warning(f"Ignoring unknown kwarg for {func}: {b}")
        return {k: v for k, v in kwargs.items() if k in allowed}

    def plot(self, xs, ys, zs, zdir="z", **kwargs):
        kws = {"fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("plot", kws, **kwargs)
        if isinstance(zs, (int, float)):
            zs = [zs] * len(xs)
        return self._plot(xs, ys, zs, zdir, **kwargs)

    def scatter(self, xs, ys, zs=0, zdir="z", *args, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "marker", "markersize", "s", "label", "cmap", "vmin", "vmax"}
        kwargs = self._check_kwargs("scatter", kws, **kwargs)

        if "s" in kwargs:
            s = kwargs.pop("s")
            if not isinstance(s, (int, float)):
                s = [i/50 for i in s]
            else:
                s /= 50
            kwargs["ms"] = s

        try:
            c = kwargs.get("c", kwargs.get("color", None))
            if c is None: raise ValueError("No color specified")
            if len(c) == len(xs):
                if isinstance(c[0], (int, float)):
                    if "cmap" not in kwargs:
                        kwargs["cmap"] = Colorbar(cmap="viridis", lower=min(c), upper=max(c))
                    else:
                        cmap = kwargs["cmap"]
                        if isinstance(cmap, str):
                            vmin = kwargs.pop("vmin", min(c))
                            vmax = kwargs.pop("vmax", max(c))
                            kwargs["cmap"] = Colorbar(cmap=cmap, lower=vmin, upper=vmax)
                    if self._cmap_bar and self._cmap_bar != kwargs["cmap"]:
                        raise Warning("Multiple colormaps on same axis! Only one per axis is allowed.")
                    else:
                        self._cmap_bar = kwargs["cmap"]
        except: pass
        
        return self._plot(xs, ys, zs, zdir, **kwargs, ls="", settings={"scatter": None})
    
    def plot_surface(self, X, Y, Z, **kwargs):
        kws = {"alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "label"}
        kwargs = self._check_kwargs("plot", kws, **kwargs)
        return self._plot(X, Y, Z, settings={"surf": None,  "mesh/rows": X.shape[0]} , **kwargs)
    
    def plot_wireframe(self, X, Y, Z, **kwargs):
        kws = {"alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "label"}
        kwargs = self._check_kwargs("plot", kws, **kwargs)
        return self._plot(X, Y, Z, settings={"mesh": None,  "mesh/rows": X.shape[0]} , **kwargs)

    def errorbar(self, x, y, z, zerr=None, yerr=None, xerr=None, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("errorbar", kws, **kwargs)
        return self._plot(x, y, z, xerr=xerr,yerr=yerr, zerr=zerr, **kwargs)

    """def stem(self, x, y, z, **kwargs):
        kws = {"orientation", "linefmt", "markerfmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("stem", kws, **kwargs)
        if "linefmt" in kwargs:
            kwargs["fmt"] = kwargs.pop("linefmt")
        orinet = "z"
        if "orientation" in kwargs:
            orinet = kwargs.pop("orientation")
        return self._plot(x,y,z,settings=[f"{orinet}comb"], **kwargs)"""

    def fill_between(self, x1, y1, z1, x2, y2, z2, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "facecolor", "fc", "label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("fill_between", kws, **kwargs)
        def _check_instance(xs, ys, zs, pname):
            for el in self._elements[self._get_overlay()]:
                if el._check_equal(xs,ys,zs):
                    return el._try_set_pname(pname)
            return None
        assert self._fig is not None
        self._fig._add_required_package("\\usepackage{fillbetween}")
        name1 = self._fig._get_free_path_name()
        name2 = self._fig._get_free_path_name()
        if isinstance(y1, (int, float)):
            y1 = _np.asarray([y1] * len(x1))
        if isinstance(z1, (int, float)):
            z1 = _np.asarray([z1] * len(x1))
        inst = _check_instance(x1,y1,z1,name1)
        if inst is None:
            self._plot(x1,y1,z1,path_name=name1, alpha=0)
        else:
            name1 = inst

        if y2 is not None:
            if isinstance(y2, (int, float)):
                y2 = _np.asarray([y2] * len(x2))
            if isinstance(z2, (int, float)):
                z2 = _np.asarray([z2] * len(x2))
            inst = _check_instance(x2,y2,z2,name2)
            if inst is None:
                self._plot(x2,y2,z2,path_name=name2, alpha=0)
            else:
                name2 = inst
        """else:
            xs = [min(x), max(x)]
            ys = [0,0]
            inst = _check_instance(xs,ys,name2)
            if inst is None:
                self._plot(xs,ys,path_name=name2, alpha=0)
            else:
                name2 = inst"""
        e = Graph3(self, f"fill between [of={name1} and {name2}]",settings={}, xerr=None, yerr=None, zerr=None, **kwargs)
        self._elements[self._get_overlay()].append(e)
        return e

    """def hist(self, x, bins=10, density=False,**kwargs):
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
            settings.append(f"bar width={widths.mean()*kwargs["rwidth"]}")
        else:
            settings[0] += " interval"
        if "range" in kwargs:
            if settings[0] == "xbar":
                self.set_ylim(kwargs["range"])
            else:
                self.set_xlim(kwargs["range"])
        if "cumulative" in kwargs and kwargs["cumulative"]:
            counts = _np.cumsum(counts)

        return self._plot(centers, counts, settings=settings, **kwargs)"""
    
    def text(self, x, y, z, s, **kwargs):
        kws = {"alpha", "color", "c", "fontsize", "size", "backgroundcolor", "horizontalalignment", "ha", "verticalalignment", "va", "rotation", "label"}
        kwargs = self._check_kwargs("text", kws, **kwargs)
        if "fontsize" in kwargs or "size" in kwargs:
            kwargs["fontsize"] = kwargs.pop("size", kwargs.pop("fontsize"))
        on_top = kwargs.pop("on_top", True)            
        txt = Text3(self, x, y, z, s, **kwargs)
        self._elements[self._get_overlay()].append(txt)

    def set_title(self, title, **kwargs):
        kws = {"fontsize", "color", "c", "loc"}
        kwargs = self._check_kwargs("set_title", kws, **kwargs)
        st = {}
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "loc" in kwargs:
            loc = kwargs["loc"]
            if loc not in ["left", "center", "right"]:
                raise Warning(f"Invalid loc: {loc}. Must be one of 'left', 'center', or 'right'.")
            if loc == "left":
                st["at"] = "{(0.0,1.0)}"
                st["anchor"] = "south west"
            elif loc == "right":
                st["at"] = "{(1.0,1.0)}"
                st["anchor"] = "south east"
            else:
                st["at"] = {}
                st["anchor"] = {}
        if st:
            self._update_axis_options("title style", st)
        self._axis_options["title"] = f"{{{tex_text(title)}}}"
    
    def set_xlabel(self, label, **kwargs):
        kws = {"fontsize", "color", "c", "loc", "rotate"}
        kwargs = self._check_kwargs("set_xlabel", kws, **kwargs)
        st = {}
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "loc" in kwargs:
            loc = kwargs["loc"]
            if loc not in ["left", "center", "right"]:
                raise Warning(f"Invalid loc: {loc}. Must be one of 'left', 'center', or 'right'.")
            if loc == "left":
                st["at"] = "{(xticklabel cs:0)}"
                st["anchor"] = "north west"
            elif loc == "right":
                st["at"] = "{(xticklabel cs:1)}"
                st["anchor"] = "north east"
            else:
                st["at"] = {}
                st["anchor"] = {}
        if "rotate" in kwargs:
            if kwargs["rotate"] not in ["vertical", "horizontal"]:
                raise Warning(f"Invalid rotate: {kwargs['rotate']}. Must be one of 'vertical' or 'horizontal'.")
            if kwargs["rotate"] == "vertical":
                st["rotate"] = "90"
            else:
                st["rotate"] = {}
        if st:
            self._update_axis_options("x label style", st)
        self._axis_options["xlabel"] = f"{{{tex_text(label)}}}"

    def set_ylabel(self, label, **kwargs):
        kws = {"fontsize", "color", "c", "loc", "rotate"}
        kwargs = self._check_kwargs("set_ylabel", kws, **kwargs)
        st = {}
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "loc" in kwargs:
            loc = kwargs["loc"]
            if loc not in ["top", "center", "bottom"]:
                raise Warning(f"Invalid loc: {loc}. Must be one of 'top', 'center', or 'bottom'.")
            if loc == "top":
                st["at"] = "{(yticklabel cs:1)}"
                st["anchor"] = "south east"
            elif loc == "bottom":
                st["at"] = "{(yticklabel cs:0)}"
                st["anchor"] = "south east"
            else:
                st["at"] = {}
                st["anchor"] = {}
        if "rotate" in kwargs:
            if kwargs["rotate"] not in ["vertical", "horizontal"]:
                raise Warning(f"Invalid rotate: {kwargs['rotate']}. Must be one of 'vertical' or 'horizontal'.")
            if kwargs["rotate"] == "horizontal":
                st["rotate"] = "-90"
            else:
                st["rotate"] = {}
        if st:
            self._update_axis_options("y label style", st)
        self._axis_options["ylabel"] = f"{{{tex_text(label)}}}"

    def set_zlabel(self, label, **kwargs):
        kws = {"fontsize", "color", "c", "loc", "rotate"}
        kwargs = self._check_kwargs("set_zlabel", kws, **kwargs)
        st = {}
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "loc" in kwargs:
            loc = kwargs["loc"]
            if loc not in ["left", "center", "right"]:
                raise Warning(f"Invalid loc: {loc}. Must be one of 'left', 'center', or 'right'.")
            if loc == "left":
                st["at"] = "{(zticklabel cs:0)}"
                st["anchor"] = "south west"
            elif loc == "right":
                st["at"] = "{(zticklabel cs:1)}"
                st["anchor"] = "south east"
            else:
                st["at"] = {}
                st["anchor"] = {}
        if "rotate" in kwargs:
            if kwargs["rotate"] not in ["vertical", "horizontal"]:
                raise Warning(f"Invalid rotate: {kwargs['rotate']}. Must be one of 'vertical' or 'horizontal'.")
            if kwargs["rotate"] == "horizontal":
                st["rotate"] = "-90"
            else:
                st["rotate"] = {}
        if st:
            self._update_axis_options("z label style", st)
        self._axis_options["zlabel"] = f"{{{tex_text(label)}}}"

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

    def set_zlim(self, *args, **kwargs):
        bottom = None
        top = None
        for k in kwargs:
            if k not in ["bottom", "top"]:
                print(f"Invalid argument {kwargs.pop(k)} in zlim")

        if len(args) == 1:
            bottom, top = args[0]
        elif len(args) == 2:
            bottom, top = args
        elif len(args) > 2:
            raise ValueError("set_zlim accepts at most 2 positional arguments")

        if "bottom" in kwargs:
            bottom = kwargs["bottom"]
        if "top" in kwargs:
            top = kwargs["top"]

        if bottom is not None:
            self._axis_options["zmin"] = bottom
        if top is not None:
            self._axis_options["zmax"] = top

    def set_xscale(self, *args, **kwargs):
        kws = {"base"}
        kwargs = self._check_kwargs("set_xscale", kws, **kwargs)
        if "log" in args:
            self._axis_options["xmode"] = "log"
        if "base" in kwargs:
            self._axis_options["log basis x"] = kwargs["base"]

    def set_yscale(self, *args, **kwargs):
        kws = {"base"}
        kwargs = self._check_kwargs("set_yscale", kws, **kwargs)
        if "log" in args:
            self._axis_options["ymode"] = "log"
        if "base" in kwargs:
            self._axis_options["log basis y"] = kwargs["base"]
    
    def set_zscale(self, *args, **kwargs):
        kws = {"base"}
        kwargs = self._check_kwargs("set_zscale", kws, **kwargs)
        if "log" in args:
            self._axis_options["zmode"] = "log"
        if "base" in kwargs:
            self._axis_options["log basis z"] = kwargs["base"]

    def set_xticks(self, ticks, labels=None, **kwargs):
        kws = {"color", "c", "fontsize"}
        kwargs = self._check_kwargs("set_xticks", kws, **kwargs)
        st = {}
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if st:
            self._update_axis_options("x tick style", st)
        if ticks:
            s_ticks = map(str, ticks)
            self._axis_options["xtick"]=f"{{{','.join(s_ticks)}}}"
            if labels is not None and len(labels)==len(ticks):
                self._axis_options["xticklabels"]=f"{{{tex_text(','.join(labels))}}}"
            elif labels is not None and len(labels) == 0:
                self._axis_options["xticklabels"]=r"{}"
                self._xticks = False
        else:
            self._axis_options["xticks"]=r"{}"
            self._xticks = False

    def set_yticks(self, ticks, labels=None, **kwargs):
        kws = {"color", "c", "fontsize"}
        kwargs = self._check_kwargs("set_yticks", kws, **kwargs)
        st = {}
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if st:
            self._update_axis_options("y tick style", st)
        if ticks:
            s_ticks = map(str, ticks)
            self._axis_options["ytick"]=f"{{{','.join(s_ticks)}}}"
            if labels is not None and len(labels)==len(ticks):
                self._axis_options["yticklabels"]=f"{{{tex_text(','.join(labels))}}}"
            elif labels is not None and len(labels) == 0:
                self._axis_options["yticklabels"]=r"{}"
                self._yticks = False
        else:
            self._axis_options["yticks"]=r"{}"
            self._yticks = False

    def set_zticks(self, ticks, labels=None, **kwargs):
        kws = {"color", "c", "fontsize"}
        kwargs = self._check_kwargs("set_zticks", kws, **kwargs)
        st = {}
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if st:
            self._update_axis_options("z tick style", st)
        if ticks:
            s_ticks = map(str, ticks)
            self._axis_options["ztick"]=f"{{{','.join(s_ticks)}}}"
            if labels is not None and len(labels)==len(ticks):
                self._axis_options["zticklabels"]=f"{{{tex_text(','.join(labels))}}}"
            elif labels is not None and len(labels) == 0:
                self._axis_options["zticklabels"]=r"{}"
                self._zticks = False
        else:
            self._axis_options["zticks"]=r"{}"
            self._zticks = False

    def set_xticklabels(self, labels, **kwargs):
        kws = {"color", "c", "fontsize"}
        kwargs = self._check_kwargs("set_xticklabels", kws, **kwargs)
        st = {}
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if st:
            self._update_axis_options("x tick label style", st)
        if labels:
            self._axis_options["xticklabels"]=f"{{{tex_text(','.join(labels))}}}"
        else:
            self._axis_options["xticklabels"]=r"{}"
            self._xticks = False

    def set_yticklabels(self, labels, **kwargs):
        kws = {"color", "c", "fontsize"}
        kwargs = self._check_kwargs("set_yticklabels", kws, **kwargs)
        st = {}
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if st:
            self._update_axis_options("y tick label style", st)
        if labels:
            self._axis_options["yticklabels"]=f"{{{tex_text(','.join(labels))}}}"
        else:
            self._axis_options["yticklabels"]=r"{}"
            self._yticks = False

    def set_zticklabels(self, labels, **kwargs):
        kws = {"color", "c", "fontsize"}
        kwargs = self._check_kwargs("set_zticklabels", kws, **kwargs)
        st = {}
        if "color" in kwargs or "c" in kwargs:
            c = kwargs.get("color", kwargs.get("c", None))
            st["text"] = self._match_color(c)
        if "fontsize" in kwargs:
            st["font"] = self._tex_fontsize(kwargs["fontsize"])
        if st:
            self._update_axis_options("z tick label style", st)
        if labels:
            self._axis_options["zticklabels"]=f"{{{tex_text(','.join(labels))}}}"
        else:
            self._axis_options["zticklabels"]=r"{}"
            self._zticks = False

    def tick_params(self, axis="both", **kwargs):
        kws = {"color", "c", "labelsize", "labelcolor", "colors", "direction", "top", "bottom", "left", "right"}
        kwargs = self._check_kwargs("tick_params", kws, **kwargs)
        if axis not in ["x", "y", "z", "both"]:
            raise Warning(f"Invalid axis: {axis}. Must be one of 'x', 'y', 'z', or 'both'.")
        X_POS_MAP = {"top": (True, False), "bottom": (False, True), "both": (True, True), "none": (False, False)}
        Y_POS_MAP = {"left": (True, False), "right": (False, True), "both": (True, True), "none": (False, False)}
        xt_b, xt_t = X_POS_MAP.get(kwargs.pop("xtick pos", "both"), (True, True))
        yt_l, yt_r = Y_POS_MAP.get(kwargs.pop("ytick pos", "both"), (True, True))
        zt_l, zt_r = Y_POS_MAP.get(kwargs.pop("ztick pos", "both"), (True, True))
        prefix = "x" if axis == "x" else ("y" if axis == "y" else "z")
        if "bottom" in kwargs:
            if axis in ["y", "z"]:
                raise Warning("Cannot set 'bottom' for y/z-axis.")
            xt_b = kwargs.pop("bottom")
        if "top" in kwargs:
            if axis in ["y", "z"]:
                raise Warning("Cannot set 'top' for y/z-axis.")
            xt_t = kwargs.pop("top")
        if "left" in kwargs:
            if axis == "x":
                raise Warning("Cannot set 'left' for x-axis.")
            if axis == "z":
                zt_l = kwargs.pop("left")
            else:
                yt_l = kwargs.pop("left")
        if "right" in kwargs:
            if axis == "x":
                raise Warning("Cannot set 'right' for x-axis.")
            if axis == "z":
                zt_r = kwargs.pop("right")
            else:
                yt_r = kwargs.pop("right")
        X_INV = {v: k for k, v in X_POS_MAP.items()}
        Y_INV = {v: k for k, v in Y_POS_MAP.items()}
        self._axis_options["xtick pos"] = X_INV[(xt_t, xt_b)]
        self._axis_options["ytick pos"] = Y_INV[(yt_l, yt_r)]
        self._axis_options["ztick pos"] = Y_INV[(zt_l, zt_r)]
        if "colors" in kwargs:
            c = self._match_color(kwargs.pop("colors"))
            self._update_axis_options(prefix + " tick style", {"draw": c})
            self._update_axis_options(prefix + " tick label style", {"text": c})
        if "color" in kwargs or "c" in kwargs:
            c = self._match_color(kwargs.get("color", kwargs.get("c")))
            self._update_axis_options(prefix + " tick style", {"draw": c})
        if "labelcolor" in kwargs:
            c = self._match_color(kwargs["labelcolor"])
            self._update_axis_options(prefix + " tick label style", {"text": c})
        if "labelsize" in kwargs:
            fs = kwargs["labelsize"]
            self._update_axis_options(prefix + " tick label style", {"font": self._tex_fontsize(fs)})
        if "direction" in kwargs:
            direction = kwargs["direction"]
            if direction not in ["in", "out", "inout"]:
                raise Warning(f"Invalid direction: {direction}. Must be one of 'in', 'out', or 'inout'.")
            TICK_DIR_MAP = {"in": "inside", "out": "outside", "inout": "center"}
            self._update_axis_options(prefix + "tick align", TICK_DIR_MAP[direction])
        if self._axis_options["xtick pos"] == "both":
            self._axis_options.pop("xtick pos")
        elif self._axis_options["xtick pos"] == "none":
            self._update_axis_options("xtick style", {"draw": self._axis_options.pop("xtick pos")})
        if self._axis_options["ytick pos"] == "both":
            self._axis_options.pop("ytick pos")
        elif self._axis_options["ytick pos"] == "none":
            self._update_axis_options("ytick style", {"draw": self._axis_options.pop("ytick pos")})
        if self._axis_options["ztick pos"] == "both":
            self._axis_options.pop("ztick pos")
        elif self._axis_options["ztick pos"] == "none":
            self._update_axis_options("ztick style", {"draw": self._axis_options.pop("ztick pos")})

    _LEGEND_LOC_MAP = ["best", "upper right", "upper left", "lower_left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center"]
    _ANCHOR_MAP = {"top": "north", "bottom": "south", "upper": "north", "lower": "south", "left": "west", "right": "east", "center": "center"}
    _FONT_SIZE_MAP = {"xx-small": "tiny", "x-small": "scriptsize", "small": "footnotesize", "medium": "small", "large": "normalsize", "x-large": "large", "xx-large": "Large"}

    def _tex_fontsize(self, fs):
        if isinstance(fs, str):
            if fs in ["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]:
                return f"\\{self._FONT_SIZE_MAP[fs]}"
            else:
                raise Warning(f"Invalid fontsize: {fs}. Must be one of 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', or 'xx-large'.")
        elif isinstance(fs, int) and fs > 0:
            return f"\\fontsize{{{fs}}}{{{round(fs*1.2)}}}\\selectfont"
        else:
            raise Warning(f"Invalid fontsize: {fs}. Must be a string or a positive integer.")

    def _match_color(self, input):
        if input == "none":
            return "none"
        ccode, op = _tex_color(input, self._style)
        if isinstance(ccode, str):
            return ccode
        r,g,b = ccode
        self._add_col(r,g,b)
        return f"c{r:.3f}{g:.3f}{b:.3f}".replace(".", "")

    def legend(self, *args, **kwargs):
        kws = ["loc", "anchor", "ncols", "facecolor", "edgecolor", "labelcolor", "frameon", "fontsize"]
        legend_string = {}
        if "loc" in kwargs:
            loc = kwargs["loc"]
            lx = ly = posit = None
            if isinstance(loc, tuple):
                try:
                    lx,ly=float(loc[0]), float(loc[1])
                    posit = "south west"
                except: 
                    print(f"Error parsing legend location: {loc}")
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

            if lx is not None and ly is not None:
                legend_string["at"] = "{(" + f"{lx},{ly}" + r")}"
            if posit is not None and len(posit):
                legend_string["anchor"] = posit
        if "anchor" in kwargs:
            anchor = kwargs["anchor"]
            if anchor in ["north", "south", "east", "west", "center", "north west", "north east", "south west", "south east"]:
                legend_string["anchor"] = anchor
            else:
                print(f"Invalid anchor: {anchor}. Must be one of 'north', 'south', 'east', 'west', 'center', 'north west', 'north east', 'south west', or 'south east'.")

        if "facecolor" in kwargs:
            ccode = self._match_color(kwargs["facecolor"])
            if ccode is not None:
                legend_string["fill"] = ccode
        if "edgecolor" in kwargs:
            ccode = self._match_color(kwargs["edgecolor"])
            if ccode is not None:
                legend_string["draw"] = ccode
        if "labelcolor" in kwargs:
            ccode = self._match_color(kwargs["labelcolor"])
            if ccode is not None:
                self._legend_lab_col = ccode
        if "frameon" in kwargs and not kwargs["frameon"]:
            legend_string["draw"] = "none"                      
        if "legend style" in self._axis_options:
            self._axis_options["legend style"].update(legend_string)
        else:
            self._axis_options["legend style"] = legend_string
        if "fontsize" in kwargs:
            fs = kwargs["fontsize"]
            legend_string["font"] = self._tex_fontsize(fs)
        self._legend_on = True
        if "ncols" in kwargs:
            self._axis_options["legend columns"] = kwargs["ncols"]
        if len(args) == 2:
            self._add_legend = list(args)
        elif len(args) == 1:
            labs = args[0]
            if len(labs) > len(self._elements):
                print("Legend: more labels than elements")
            else:
                all_elements = self._get_all_elements()
                for i in range(len(labs)):
                    all_elements[i]._set_label(tex_text(labs[i]))
    def view_init(self, elev=None, azim=None, roll=None):
        if elev == None:
            elev = TikzConfig.DEFAULT_3D_ELEV
        if azim == None:
            azim = TikzConfig.DEFAULT_3D_AZIM
        #if roll == None:
        #    roll = TikzConfig.DEFAULT_3D_ROLL
        self._axis_options["view"] = f"{{{90+azim}}}{{{elev}}}"
        #self._axis_options["rotate around z"] = f"{{{roll}}}" 

    def _add_legend_entries(self):
        if self._add_legend == []: return ""
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
        ouptut = "\n".join(e._to_tex(filename) for e in self._get_all_elements())
        ouptut += self._add_legend_entries()
        return ouptut
    
    def _get_hard_range(self,which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self._axis_options:
            mode = self._axis_options[arg]
        if which in self._axis_options:
            for e in self._elements[self._get_overlay()]:
                e._filter(which, self._axis_options[which])
            return (self._axis_options[which], mode)
        return None, mode
    
    def _get_range(self, which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self._axis_options:
            mode = self._axis_options[arg]
        if which in self._axis_options:
            for e in self._elements[self._get_overlay()]:
                e._filter(which, self._axis_options[which])
            return (self._axis_options[which], True, mode)
        if "min" in which:
            return (min([e._get_erange(which) for e in self._get_all_elements()]), False, mode)
        return (max([e._get_erange(which) for e in self._get_all_elements()]), False, mode)
    
    def _set_range(self, which, value):
        self._axis_options[which] = value
        for e in self._get_all_elements():
            e._filter(which, value)

    def _num_points(self):
        return [e._num_points() for e in self._get_all_elements()]
    
    def _reduce_points(self, limit):
        logx, logy = False, False
        if "xmode" in self._axis_options and self._axis_options["xmode"] == "log":
            logx = True
        if "ymode" in self._axis_options and self._axis_options["ymode"] == "log":
            logy = True
        for e in self._get_all_elements():
            e._reduce_points(limit, logx, logy)

    def _add_col(self, r,g,b):
        assert self._fig is not None
        self._fig._add_col(r,g,b)

    def _update_size(self):
        assert self._fig is not None
        if self._fig._get_width():
            self._width= f"{self._fig._get_width() / self._ncols}cm"
        if self._fig._get_height():
            self._height = f"{self._fig._get_height() / self._nrows}cm"

    def grid(self, visible=True, which="major", **kwargs):
        if not visible:
            self._axis_options["grid"] = "none"
            return
        selector = which + " "
        if which == "major":
            if "grid" in self._axis_options and self._axis_options["grid"] == "minor":
                self._axis_options["grid"] = "both"
            else:
                self._axis_options["grid"] = "major"

        elif which == "minor":
            if "grid" in self._axis_options and self._axis_options["grid"] == "major":
                self._axis_options["grid"] = "both"
            else:
                self._axis_options["grid"] = "minor"

        elif which == "both":
            self._axis_options["grid"] = "both"
            selector = ""
        
        if kwargs:
            accepted_kwargs = {"color", "c", "linestyle", "ls", "linewidth", "lw", "alpha"}
            kwargs = self._check_kwargs("grid", accepted_kwargs, **kwargs)
            g = Graph3(self, None, {}, None, None, **kwargs)._style_string()
            self._axis_options[f"{selector}grid style"] = f"{{{g}}}"

    def set_minorticks_num(self, num):
        self._axis_options["minor tick num"] = num

    def _axis_option_string(self):
        if self._elements[self._get_overlay()] == [] and self._get_overlay() > 0:
            del self._elements[self._get_overlay()]
        if self._get_overlay() > 0:
            self._ext_xmax = self._ext_xmin = self._ext_ymax = self._ext_ymin = True
            if self._legend_on:
                self._overlay_legend = True
                self._legend_on = False
        alias = self._axis_options.pop("alias", self._axis_options.pop("name", None))
        self._update_size()
        if self._width:
            self._axis_options["width"] = self._width
        if self._height:
            self._axis_options["height"] = self._height
        if not TikzConfig.USE_GROUPPLOTS:
            assert self._fig is not None
            if self._left:
                self._axis_options["yshift"] = f"-{self._fig._get_spacing(self._row, self._col)}cm"
            else:
                self._axis_options["xshift"] = f"{self._fig._get_spacing(self._row, self._col)}cm"
        axis_opt_str = ""
        if self._axis_args:
            axis_opt_str += ",\n".join(self._axis_args)
        #if TikzConfig.SCHOOL_AXIS:
        #    axis_opt_str += f",\n axis lines=middle,\n xlabel style={{at={{(ticklabel* cs:{1+TikzConfig.SCHOOL_AXIS_LABEL_MARGIN})}},anchor=north}},\n ylabel style={{at={{(ticklabel* cs:{1+TikzConfig.SCHOOL_AXIS_LABEL_MARGIN})}},anchor=east}},"
        if self._axis_options:
            if axis_opt_str: axis_opt_str += ",\n"
            for k, v in self._axis_options.items():
                if v != {}:
                    entry = self._parse_entry(k,v)
                    axis_opt_str += entry + ",\n"
        axis_opt_str = axis_opt_str.removesuffix(",,\n")
        if self._colorbar:
            axis_opt_str += self._colorbar
        elif self._cmap_bar:
            axis_opt_str += f"colormap={self._cmap_bar._generate_tex_colormap(self._cmap_bar._cmap)},\n"
        return axis_opt_str
    
    def _margins(self):
        left = TikzConfig.LEFT_PADDING * self._yticks + TikzConfig.Y_LABEL_PADDING * ("ylabel" in self._axis_options)
        right = TikzConfig.RIGHT_PADDING + TikzConfig.CBAR_X_MARGIN * (self._colorbar != "" and not self._cbar_h)
        top = TikzConfig.TOP_PADDING + TikzConfig.TITLE_PADDING * ("title" in self._axis_options)
        bottom = TikzConfig.BOTTOM_PADDING * self._xticks + TikzConfig.X_LABEL_PADDING * ("xlabel" in self._axis_options) + TikzConfig.CBAR_Y_MARGIN * (self._colorbar != "" and self._cbar_h)

        return left, right, top, bottom
    
    def _get_row(self):
        return self._row
    def _get_col(self):
        return self._col
    def _get_nrows(self):
        return self._nrows
    def _get_ncols(self):
        return self._ncols
    def _get_defcol(self, index = 0):
        if index not in self._defcol_counter:
            self._defcol_counter[index] = 0
        self._defcol_counter[index] += 1
        return self._defcol_counter[index] - 1
    def _show_colorbar(self, cbar, horizontal=False):
        self._colorbar = ",\n" + cbar
        self._cbar_h = horizontal
    def _get_index(self):
        return self._index
    
    def _to_tex(self, filename, single):
        lines = []
        if TikzConfig.USE_GROUPPLOTS and not single:
            lines.append("\\nextgroupplot")
            lines.append(f"[{self._axis_option_string()}]")
            lines.append(self._content_tex(filename))
        else:
            lines.append("\\begin{axis}")
            lines.append(f"[{self._axis_option_string()}]")
            lines.append(self._content_tex(filename))
            lines.append("\\end{axis}")
        return lines, []
    
    def set(self, **kwargs):
        defined = {"title": self.set_title, "xlim": self.set_xlim, "xlabel": self.set_xlabel, "xscale": self.set_xscale, "xticklabels": self.set_xticklabels, "xticks": self.set_xticks, "ylim": self.set_ylim, "ylabel": self.set_ylabel, "yscale": self.set_yscale, "yticklabels": self.set_yticklabels, "yticks": self.set_yticks, "zlim": self.set_zlim, "zlabel": self.set_zlabel, "zscale": self.set_zscale, "zticklabels": self.set_zticklabels, "zticks": self.set_zticks}
        for attr in defined:
            if attr in kwargs:
                defined[attr](kwargs.pop(attr))

    def set_facecolor(self, color):
        ccode, _ = _tex_color(color, self._style)
        if isinstance(ccode, str):
            self._axis_options["axis background/.style"] = f"{{fill={ccode}}}"
        else:
            r,g,b = ccode
            self._add_col(r,g,b)
            self._axis_options["axis background/.style"] = f"{{fill=c{r:.3f}{g:.3f}{b:.3f}}}".replace(".", "")
