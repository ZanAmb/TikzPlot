from multiprocessing import parent_process
from typing import Any, Iterable
import copy

import numpy as _np
import matplotlib.pyplot as _plt
from scipy import datasets

from .elements import Graph
from .texts import Text
from .config import TikzConfig
from .colorbar import Colorbar
from .state import _next_imshow_num, main_name
from .latex_special import tex_text
from .colors import _tex_color

class BaseAxes:
    def __init__(self):
        self._elements: dict[int, list] = {0: []}
        self._axis_options = {}
        self._axis_args = set()
        self._legend_on = False
        self._overlay_legend = False
        self._overlay_legend_entries = []
        self._overlay_special: dict[int, dict[str, Any]] = {}
        self._yticks = True
        self._fig = None
        if TikzConfig.USE_DECIMAL_COMMA:
            self._axis_args.add(f"/pgf/number format/.cd, use comma, 1000 sep={{{TikzConfig.THOUSANDS_SEP}}}")
        else:
            self._axis_args.add(f"/pgf/number format/.cd, 1000 sep={{{TikzConfig.THOUSANDS_SEP}}}")

        self._add_legend = []
        self._legend_lab_col: Any = None
        self._coordinates = {}
        self._cmap_bar = None

        self._ext_ymin = False
        self._ext_ymax = False

        self._int_ymin = None
        self._int_ymax = None

        self._preferred_lims = {}
        self._bar_labels = {}

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

    def _plot(self, x, y, settings={}, xerr=None, yerr=None, overlay=None, note=None, **style):
        spec = None
        if self._get_overlay() in self._overlay_special:
            spec = ",\n".join([self._parse_entry(k, v) for k, v in self._overlay_special[self._get_overlay()].items()])
        if note != spec:
            self._get_free_overlay()
            
        if isinstance(self, Axes) and self._polar:
            x = _np.rad2deg(x)
        e = Graph(self, (x, y), settings, xerr=xerr, yerr=yerr, **style)
        if overlay is None:
            overlay = self._get_overlay()
        if TikzConfig.USE_GROUPPLOTS and ("axvspan" in settings or "axhspan" in settings):
            self._elements[overlay].insert(0, e)
        else:
            self._elements[overlay].append(e)
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
            if len(c) == len(x):
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
        
        return self._plot(x, y, **kwargs, ls="", settings={"scatter": None})
                        
    def semilogy(self, x, y, *args, **kwargs):
        kws = {"fmt", "base", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        kwargs = self._check_kwargs("semilogy", kws, **kwargs)
        self._axis_options["ymode"] = "log"
        if "base" in kwargs:
            self._axis_options["log basis y"] = kwargs["base"]
        return self._plot(x, y, **kwargs)

    def errorbar(self, x, y, *args, **kwargs):
        kws = {"xerr", "yerr", "fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label", "capsize", "ecolor", "elinewidth", "elinestyle"}
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
        else:
            raise Warning("Invalid number of args for stem.")
        if "orientation" in kwargs:
            o = kwargs.pop("orientation")
            if o == "horizontal":
                vert = False
        if vert:
            return self._plot(x,y,settings={"ycomb": None}, **kwargs)
        else:
            return self._plot(y,x,settings={"xcomb": None}, **kwargs)

    def fill_between(self, x, y1, y2=None, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "facecolor", "fc", "label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("fill_between", kws, **kwargs)
        def _check_instance(xs, ys, pname):
            for el in self._elements[self._get_overlay()]:
                if el._check_equal(xs,ys):
                    return el._try_set_pname(pname)
                else:
                    return None
        assert self._fig is not None
        self._fig._add_required_package("\\usepgfplotslibrary{fillbetween}")
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
            if isinstance(y2, (int, float)):
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
        if "facecolor" in kwargs or "fc" in kwargs:
            kwargs["color"] = kwargs.pop("facecolor", kwargs.pop("fc", None))
            kwargs.pop("fc", None)
        if not("color" in kwargs or "c" in kwargs):
            assert isinstance(self, Axes) or isinstance(self, Secondary)
            kwargs["color"] = f"C{self._get_defcol(1)}"            
        e = Graph(self, f"fill between [of={name1} and {name2}]",settings={}, xerr=None, yerr=None, **kwargs)
        self._elements[self._get_overlay()].append(e)
        return e

    def fill_betweenx(self, y, x1, x2=None, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "facecolor", "fc", "label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("fill_between", kws, **kwargs)
        def _check_instance(xs, ys, pname):
            for el in self._elements[self._get_overlay()]:
                if el._check_equal(xs,ys):
                    return el._try_set_pname(pname)
                else:
                    return None
        assert self._fig is not None
        self._fig._add_required_package("\\usepgfplotslibrary{fillbetween}")
        name1 = self._fig._get_free_path_name()
        name2 = self._fig._get_free_path_name()
        if isinstance(x1, (int, float)):
            x1 = _np.asarray([x1] * len(y))
        inst = _check_instance(x1,y,name1)
        if inst is None:
            self._plot(x1,y,path_name=name1, alpha=0)
        else:
            name1 = inst

        if x2 is not None:
            if isinstance(x2, (int, float)):
                x2 = _np.asarray([x2] * len(y))
            inst = _check_instance(x2,y,name2)
            if inst is None:
                self._plot(x2,y,path_name=name2, alpha=0)
            else:
                name2 = inst
        else:
            xs = [0, 0]
            ys = [min(y), max(y)]
            inst = _check_instance(xs,ys,name2)
            if inst is None:
                self._plot(xs,ys,path_name=name2, alpha=0)
            else:
                name2 = inst
        if "facecolor" in kwargs or "fc" in kwargs:
            kwargs["color"] = kwargs.pop("facecolor", kwargs.pop("fc", None))
            kwargs.pop("fc", None)
        if not("color" in kwargs or "c" in kwargs):
            assert isinstance(self, Axes) or isinstance(self, Secondary)
            kwargs["color"] = f"C{self._get_defcol(1)}"            
        e = Graph(self, f"fill between [of={name1} and {name2}]",settings={}, xerr=None, yerr=None, **kwargs)
        self._elements[self._get_overlay()].append(e)
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
                self._plot([xs[i]]*2, [ymins[i], ymaxs[i]], None, None, None, c=colorss[i], ls=lss[i], label=kwargs["label"])
            else:
                self._plot([xs[i]]*2, [ymins[i], ymaxs[i]], None, None, None, c=colorss[i], ls=lss[i])

    def hist(self, x, bins=10, density=False,**kwargs):
        kws = {"alpha", "color", "c", "label", "facecolor", "fc", "edgecolor", "ec", "orientation", "rwidth", "cumulative", "range", "histtype", "weights", "cumulative", "align", "stacked", "fill", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("hist", kws, **kwargs)
        if isinstance(x, (list, tuple)) and len(x) > 0 and isinstance(x[0], (list, tuple, _np.ndarray)):
            try:
                datasets = [_np.asarray(ds, dtype=_np.float64) for ds in x]
                if any(ds.ndim != 1 for ds in datasets):
                    raise ValueError("Nested datasets must all be 1-dimensional.")
            except (ValueError, TypeError):
                x_arr = _np.asarray(x)
                if x_arr.ndim == 2:
                    datasets = [x_arr[:, i] for i in range(x_arr.shape[1])]
                else:
                    raise ValueError("Invalid dataset structure.")
        else:
            x_arr = _np.asarray(x)
            if x_arr.ndim == 1:
                datasets = [x_arr]
            elif x_arr.ndim == 2:
                datasets = [x_arr[:, i] for i in range(x_arr.shape[1])]
            else:
                raise ValueError(f"Input must be 1D or 2D, got {x_arr.ndim}D.")

        stack = kwargs.pop("stacked", False)
        datas = {}
        for kw in ["color", "c", "facecolor", "fc", "edgecolor", "ec", "label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"]:
            if kw in kwargs:
                if isinstance(kwargs[kw], (list)):
                    if len(kwargs[kw]) != len(datasets):
                        raise Warning(f"Length of {kw} does not match number of datasets.")
                    prop = kwargs.pop(kw)
                else:
                    prop = [kwargs.pop(kw)] * len(datasets)
                for i in range(len(datasets)):
                    if i not in datas:
                        datas[i] = {}
                    datas[i][kw] = prop[i]
        all_data = _np.concatenate(datasets)
        edges = _np.histogram_bin_edges(all_data, bins=bins, weights=kwargs.get("weights", None), range=kwargs.get("range", None))
        widths = edges[1:] - edges[:-1]
        offset = 0
        settings = {}
        if "rwidth" not in kwargs:
            kwargs["rwidth"] = 1
        orientation = kwargs.pop("orientation", "vertical")
        hist_type = kwargs.pop("histtype", "bar")
        if hist_type not in ["bar", "barstacked", "step", "stepfilled"]:
            raise Warning(f"Invalid histtype: {hist_type}.")
        if hist_type == "barstacked":
            stack = True
            hist_type = "bar"
        elif hist_type == "stepfilled":
            hist_type = "bar"
            kwargs["rwidth"] = 1
        elif hist_type == "step":
            kwargs["rwidth"] = 1
        intervals = False
        if ("rwidth" in kwargs or (len(datasets) > 1 and not stack)) and isinstance(bins, int):
            if stack or len(datasets) == 1:
                settings["thickness"] = widths.mean()*kwargs['rwidth']
            else:
                if "rwidth" in kwargs:
                    settings["thickness"] = widths.mean()*kwargs['rwidth']/(len(datasets)+1)
                    offset = widths.mean() * kwargs['rwidth'] / (len(datasets) + 1)
                else:
                    settings["thickness"] = widths.mean()/(len(datasets)+1)
                    offset = widths.mean() / (len(datasets) + 1)
        else:
            intervals = True
        base_settings = settings.copy()
        outputs = []
        totals, _ = _np.histogram(all_data, edges, density=False, weights=kwargs.get("weights", None), range=kwargs.get("range", None))
        tot_sum = totals.sum()
        align = kwargs.pop("align", "mid")
        if align not in ["left", "mid", "right"]:
            raise Warning(f"Invalid align: {align}. Must be 'left', 'mid', or 'right'.")
        bottom = None
        old_counts = _np.zeros(len(edges)-1, dtype=_np.float64)
        
        for i in range(len(datasets)):
            data = datasets[i]
            settings = base_settings.copy()
            kws = datas.get(i, {})
            passing_args = ["facecolor", "fc", "color", "c", "edgecolor", "ec", "label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"]
            for a in passing_args:
                if a in kws:
                    settings[a] = kws[a]
            counts, _ = _np.histogram(data, edges, density=density, weights=kwargs.get("weights", None), range=kwargs.get("range", None))
            if intervals and "rwidth" in kwargs:
                ws = widths
                if align == "mid":
                    xs = edges[:-1] + widths * (1-kwargs["rwidth"])/2
                    ws = widths * kwargs["rwidth"]
                elif align == "left":
                    xs = edges[:-1]
                    ws = widths * kwargs["rwidth"]
                else: # align == "right"
                    xs = edges[1:] - widths * kwargs["rwidth"]
                    ws = widths * kwargs["rwidth"]

                if self._check_approximate_equal(ws, ws[0]*_np.ones_like(ws)):
                    ws = float(ws[0])
                settings["thickness"] = ws
            else:
                xs = (edges[:-1] + edges[1:]) / 2
            if offset > 0:
                settings["group_offset"] = f"{offset*(i - len(datasets)/2 + 0.5)}"
            if "cumulative" in kwargs and kwargs["cumulative"]:
                counts = _np.cumsum(counts)
            if stack:
                if density:
                    set_counts, _ = _np.histogram(data, edges, density=False, weights=kwargs.get("weights", None), range=kwargs.get("range", None))
                    counts = counts * _np.sum(set_counts) / tot_sum
                counts = _np.asarray(counts, dtype=_np.float64)
                new_counts = counts + old_counts
                bottom = old_counts.copy()
                old_counts = new_counts.copy()
            if intervals:
                settings["align"] = "edge"
            else:
                settings["align"] = "center"
                if align == "left":
                    xs += widths.mean()*kwargs.get("rwidth", 1)/2
                elif align == "right":
                    xs -= widths.mean()*kwargs.get("rwidth", 1)/2
            if hist_type == "step":
                    if stack:
                        counts += old_counts
                        old_counts = counts.copy()
                    settings.pop("facecolor", None)
                    settings.pop("fc", None)
                    settings.pop("fill", None)
                    settings.pop("thickness", None)
                    settings.pop("align", None)
                    self.step([edges[0]] + list(edges), [0] + list(counts) + [0], where="pre", **settings)
            else:
                if bottom is not None:
                    settings["edge"] = bottom
                e = self._common_bar(xs, counts, settings=settings, **settings)
                outputs.append(e)
        return outputs

    def bar(self, x, height, width=0.8, bottom=None, **kwargs):
        kws = {"alpha", "align", "color", "c", "facecolor", "fc", "edgecolor", "ec", "linewidth", "lw", "tick_label", "label", "xerr", "yerr", "ecolor", "capsize", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance", "tick_label"}
        kwargs = self._check_kwargs("bar", kws, **kwargs)
        kwargs["width"] = width
        if bottom is not None:
            kwargs["bottom"] = bottom
        if "width" in kwargs:
            kwargs["thickness"] = kwargs.pop("width")
        kwargs["edge"] = kwargs.pop("bottom", 0)

        return self._common_bar(x, height, orientation="vertical", **kwargs)

    def barh(self, y, width, height=0.8, left=None, **kwargs):
        kws = {"alpha", "align", "color", "c", "facecolor", "fc", "edgecolor", "ec", "linewidth", "lw", "tick_label", "label", "xerr", "yerr", "ecolor", "capsize", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("barh", kws, **kwargs)
        kwargs["height"] = height
        if left is not None:
            kwargs["left"] = left
        if "height" in kwargs:
            kwargs["thickness"] = kwargs.pop("height")
        kwargs["edge"] = kwargs.pop("left", 0)

        return self._common_bar(y, width, orientation="horizontal", **kwargs)

    def grouped_bar(self, heights, **kwargs):
        kws = {"positions", "tick_labels", "labels", "group_spacing", "bar_spacing", "orientation", "colors", "alpha", "edgecolor", "ec", "facecolor", "fc", "linewidth", "lw", "linestyle", "ls", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("grouped_bar", kws, **kwargs)
        if isinstance(heights, dict):
            if "labels" not in kwargs:
                kwargs["labels"] = list(heights.keys())
            heights = list(heights.values())
        if isinstance(heights, (list, tuple)) and len(heights) > 0 and isinstance(heights[0], (list, tuple, _np.ndarray)):
            try:
                datasets = [_np.asarray(ds, dtype=_np.float64) for ds in heights]
                if any(ds.ndim != 1 for ds in datasets):
                    raise ValueError("Nested datasets must all be 1-dimensional.")
            except (ValueError, TypeError):
                h_arr = _np.asarray(heights)
                if h_arr.ndim == 2:
                    datasets = [h_arr[:, i] for i in range(h_arr.shape[1])]
                else:
                    raise ValueError("Invalid dataset structure.")
        else:
            h_arr = _np.asarray(heights)
            if h_arr.ndim == 1:
                datasets = [h_arr]
            elif h_arr.ndim == 2:
                datasets = [h_arr[:, i] for i in range(h_arr.shape[1])]
            else:
                raise ValueError(f"Input must be 1D or 2D, got {h_arr.ndim}D.")

        xs = kwargs.pop("positions", range(len(datasets[0])))
        if len(xs) != len(datasets[0]):
            raise Warning("Length of positions does not match length of datasets.")
        if _np.diff(xs).min() != _np.diff(xs).max():
            raise Warning("Positions must be equidistant.")
        dist = _np.diff(xs).min()
        settings = {}
        if "rwidth" not in kwargs:
            kwargs["rwidth"] = 1
        orientation = kwargs.pop("orientation", "vertical")
        group_spacing = kwargs.pop("group_spacing", 1.5)
        bar_spacing = kwargs.pop("bar_spacing", 0.0)
        bar_widths_num = len(datasets) * (1 + bar_spacing) + group_spacing
        bar_width = dist / bar_widths_num
        settings["thickness"] = bar_width

        if "tick_labels" in kwargs:
            tick_labels = kwargs.pop("tick_labels")
            if len(tick_labels) != len(xs):
                raise Warning("Length of tick_labels does not match length of positions.")
            if orientation == "vertical":
                if isinstance(self, Axes):
                    self.set_xticks(xs, tick_labels)
                elif isinstance(self, Secondary):
                    self._primary.set_xticks(xs, tick_labels)
            else:
                self.set_yticks(xs, tick_labels)

        datas = {}
        for kw in ["colors", "alpha", "facecolor", "fc", "edgecolor", "ec", "labels", "linestyle", "ls", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"]:
            if kw in kwargs:
                if isinstance(kwargs[kw], (list)):
                    if len(kwargs[kw]) != len(datasets):
                        raise Warning(f"Length of {kw} does not match number of datasets.")
                    prop = kwargs.pop(kw)
                else:
                    prop = [kwargs.pop(kw)] * len(datasets)
                for i in range(len(datasets)):
                    if i not in datas:
                        datas[i] = {}
                    datas[i][kw.removesuffix("s")] = prop[i]
        base_settings = settings.copy()
        bars = []
        for i in range(len(datasets)):
            offset = (i - len(datasets)/2 + 0.5) * bar_width * (1 + bar_spacing)
            data = datasets[i]
            settings = base_settings.copy()
            kws = datas.get(i, {})
            passing_args = ["alpha", "facecolor", "fc", "color", "c", "edgecolor", "ec", "label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"]
            for a in passing_args:
                if a in kws:
                    settings[a] = kws[a]
            bars.append(self._common_bar(xs, data, orientation=orientation, **settings, group_offset=offset))   
        return bars         

    def _common_bar(self, k, v, orientation="vertical", **kwargs):
        #if orientation == "vertical":
        #    self._int_ymax = self._int_ymin = 0
        #else:
        #    self._int_xmax = self._int_xmin = 0
        settings = {}
        element_args = {}
        bar_type = None
        overlay = None
        if isinstance(k, float):
            k = _np.asarray([k])
        else:
            k = _np.asarray(k)
        def set_tick_labels(labels):
            if orientation == "vertical":
                if isinstance(self, Axes):
                    self.set_xticks(k, labels)
                elif isinstance(self, Secondary):
                    self._primary.set_xticks(k, labels)
            else:
                if isinstance(self, Axes):
                    self.set_yticks(k, labels)
                elif isinstance(self, Secondary):
                    self._primary.set_yticks(k, labels)
        if isinstance(k[0], str):
            labels = k
            k = range(len(labels))
            set_tick_labels(labels)
        elif "tick_label" in kwargs:
            labels = kwargs.pop("tick_label")
            if len(labels) != len(k):
                raise Warning("Length of tick_label does not match length of values.")
            set_tick_labels(labels)
        k = _np.asarray(k, dtype=_np.float64)
        if isinstance(v, float):
            v = _np.asarray([v], dtype=_np.float64)
        else:
            v = _np.asarray(v, dtype=_np.float64)
        edge = kwargs.pop("edge", 0)
        thickness = kwargs.pop("thickness", 0.8)
        align = kwargs.pop("align", "center")
        if isinstance(edge, float):
            edge = _np.asarray([edge] * len(v))
        else:
            edge = _np.asarray(edge)
        const_thick = isinstance(thickness, float | int)
        if const_thick:
            settings["bar width"] = thickness
            offset = kwargs.pop("group_offset", 0)
            if isinstance(offset, float | int):
                k = k + _np.array([offset] * len(k), dtype=_np.float64)
            else:
                k = k + _np.asarray(offset, dtype=_np.float64)
            if align == "edge":
                if const_thick:
                    k = k + _np.asarray([thickness/2] * len(k))
                else:
                    k = k + _np.asarray(thickness)/2
        else:
            coordinates, values = [], []
            thickness = _np.asarray(thickness)
            for i in range(len(k)):
                if align == "edge":
                    coordinates.append(k[i])
                    coordinates.append(k[i] + thickness[i])
                else:
                    coordinates.append(k[i] - thickness[i]/2)
                    coordinates.append(k[i] + thickness[i]/2)
                if i < len(v):
                    values.append(v[i])
                else:
                    values.append(0)
                values.append(0)
            k, v = _np.asarray(coordinates), _np.asarray(values)
        if const_thick:
            bar_type = "ybar" if orientation == "vertical" else "xbar"
        else:
            bar_type = "ybar interval" if orientation == "vertical" else "xbar interval"
        settings[bar_type] = None
        levels = edge + v
        m, M = min(levels), max(levels)
        self._update_levels("ymin" if orientation == "vertical" else "xmin", min(m, 0))
        self._update_levels("ymax" if orientation == "vertical" else "xmax", M)

        if _np.count_nonzero(edge) > 0:
            lower = self._get_overlay()
            if bar_type + " stacked" in self._overlay_special.get(lower, {}):
                bedx = _np.zeros_like(edge, dtype=_np.float64)
                bedy = _np.zeros_like(edge, dtype=_np.float64)
                for el in self._elements[lower]:
                    if orientation == "vertical":
                        bedx = el._get_points()[0] if el._get_points()[0] is not None else 0
                        bedy += el._get_points()[1] if el._get_points()[1] is not None else 0
                    else:
                        bedy = el._get_points()[0] if el._get_points()[0] is not None else 0
                        bedx += el._get_points()[1] if el._get_points()[1] is not None else 0
                if orientation == "vertical":
                    if self._check_approximate_equal(bedx, k) and self._check_approximate_equal(bedy, edge):
                        overlay = lower
                else:
                    if self._check_approximate_equal(bedy, k) and self._check_approximate_equal(bedx, edge):
                        overlay = lower
            if overlay is None:
                if len(self._elements[self._get_overlay()]) > 0 and self._elements[self._get_overlay()][-1]._check_equal(k, edge):
                    if len(self._elements[lower]) == 1:
                        if lower not in self._overlay_special:
                            self._overlay_special[lower] = {}
                        self._overlay_special[lower].update({bar_type + " stacked": None})
                        overlay = lower
                    else:
                        current = self._get_free_overlay()
                        self._elements[current].append(self._elements[lower].pop()) # move the stacking bed to new overlay
                        self._overlay_special[current] = {bar_type + " stacked": None}
                        overlay = current
                else: # no bed, plot invisible bed
                    current = self._get_free_overlay()
                    self._overlay_special[current] = {bar_type + " stacked": None}
                    self._plot(k, edge, alpha=0)
                    overlay = current

        fill = kwargs.pop("facecolor", kwargs.pop("fc", kwargs.pop("color", kwargs.pop("c", None))))
        draw = kwargs.pop("edgecolor", kwargs.pop("ec", None))
        if fill:
            fill = self._match_color(fill)
        settings["fill"] = fill
        if draw:
            draw = self._match_color(draw)
            settings["draw"] = draw
        else:
            settings["draw"] = "none"
        for kw in ["label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"]:
            if kw in kwargs:
                element_args[kw] = kwargs.pop(kw)
        note = ",\n".join([self._parse_entry(k, v) for k, v in self._overlay_special.get(overlay, {}).items()]) if overlay in self._overlay_special else None
        if "label" in element_args:
            if orientation == "vertical":
                settings["ybar legend"] = None
            else:
                settings["xbar legend"] = None
            settings[bar_type] = None
        return self._plot(k, v, yerr=kwargs.get("yerr", None), xerr=kwargs.get("xerr", None), overlay=overlay, settings=settings, note=note, **element_args)

    def bar_label(self, container, labels=None, **kwargs):
        kws = {"alpha", "color", "c", "fontsize", "rotation", "fmt", "padding"}
        kwargs = self._check_kwargs("bar_label", kws, **kwargs)
        if not isinstance(container, Graph):
            raise Warning("Container must be a Graph object.")
        if labels is not None and labels != []:
            if len(labels) != len(container._x):
                raise Warning("Length of labels does not match number of bars.")  

        if "color" in kwargs or "c" in kwargs:
            c = kwargs.pop("color", kwargs.pop("c", None))
            kwargs["color_parsed"] = self._match_color(c)
        if "alpha" in kwargs:
            kwargs["opacity"] = kwargs.pop("alpha")
        if "fontsize" in kwargs:
            kwargs["fontsize_parsed"] = self._tex_fontsize(kwargs["fontsize"])
        o = self._get_element_overlay(container)
        if o not in self._bar_labels:
            self._bar_labels[o] = {}
        if labels != []:
            if labels is None:
                labels = container._y
            fmt = kwargs.pop("fmt", "%g")
            if not isinstance(fmt, str):
                raise Warning("fmt must be a string.")
            def format_label(q):
                if "{" in fmt and "}" in fmt:
                    return fmt.format(q)
                return fmt % q
            labels = [format_label(q) if isinstance(q, (int, float)) else q for q in labels]
            cleaned = ["".join(c for c in s if c.isdigit() or c in ".-") for s in labels]
            parsed = _np.array(cleaned, dtype=float)
            all_match = _np.allclose(container._y, parsed)
            if all_match:
                labels = None
        if labels is not None and labels != []:
            container._add_meta_column(labels)
        self._bar_labels[self._get_element_overlay(container)][container] = kwargs | {"bar_labels": labels}

    def stackplot(self, x, *args, **kwargs):
        kws = {"baseline", "labels", "colors", "alpha", "facecolor", "fc", "edgecolor", "ec", "linewidth", "lw", "linestyle", "ls", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("stackplot", kws, **kwargs)
        n = len(x)
        x = _np.asarray(x, dtype=_np.float64)
        if len(args) == 1:
            y = list(args[0])
        else:
            y = list(args)
        if isinstance(list(y)[0], int | float):
            y = [list(y)]
        y = _np.asarray(y, dtype=_np.float64)
        base_set = kwargs.pop("baseline", "zero")
        if base_set not in ["zero", "sym", "wiggle", "weighted_wiggle"]:
            raise Warning(f"Invalid baseline: {base_set}. Must be one of 'zero', 'sym', 'wiggle', or 'weighted_wiggle'.")
        if base_set == "zero":
            baseline = _np.zeros(n, dtype=_np.float64)
        elif base_set == "sym":
            baseline = -_np.sum(y, axis=0)/2
        elif base_set == "wiggle": # from matplotlib source
            m = y.shape[0]
            baseline = (y * (m - 0.5 - _np.arange(m)[:, None])).sum(0)
            baseline /= -m
        else: # weighted_wiggle; from matplotlib source
            total = _np.sum(y, 0)
            inv_total = _np.zeros_like(total)
            mask = total > 0
            inv_total[mask] = 1.0 / total[mask]
            increase = _np.hstack((y[:, 0:1], _np.diff(y)))
            below_size = total - _np.cumsum(y, axis=0, dtype=_np.promote_types(y.dtype, _np.float32))
            below_size += 0.5 * y
            move_up = below_size * inv_total
            move_up[:, 0] = 0.5
            center = (move_up - 0.5) * increase
            center = _np.cumsum(center.sum(0))
            baseline = center - 0.5 * total
        overlay = self._get_free_overlay()
        self._overlay_special[overlay] = {"stack plots": "y", "area style": None}
        if base_set != "zero":
            self._plot(x, baseline, overlay=overlay, alpha=0)
        datas = {}
        for kw in ["labels", "colors", "alpha", "facecolor", "fc", "edgecolor", "ec", "linewidth", "lw", "linestyle", "ls", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"]:
            if kw in kwargs:
                prop = kwargs.pop(kw)
                try:
                    prop = list(prop)
                except: pass
                if isinstance(prop, (list, tuple)):
                    if len(prop) != len(y):
                        raise Warning(f"Length of {kw} does not match number of datasets.")
                else:
                    prop = [prop] * len(y)
                datas[kw.removesuffix("s")] = prop
        if "label" in datas:
            self._overlay_special[overlay]["area legend"] = None
        output = []
        for i in range(len(y)):
            kws = {kw: datas[kw][i] for kw in datas}
            kws["_endnotes"] = r"\closedcycle"
            output.append(self._plot(x, y[i], overlay=overlay, settings={"fill": None}, **kws))
        return output

    def step(self, x, y, *args, **kwargs):
        kws = {"fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label", "where"}
        kwargs = self._check_kwargs("step", kws, **kwargs)
        WHERE_DICT = {"pre": "left", "post": "right", "mid": "mid"}
        where = WHERE_DICT.get(kwargs.pop("where", "pre"), None)
        settings = {f"const plot mark {where}": None}
        if len(args) == 1:
            kwargs["fmt"] = args[0]
        return self._plot(x,y,settings=settings, **kwargs)
    
    def axvline(self, x, ymin=0, ymax=1, **kwargs):
        kws = {"fmt", "base", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "label"}
        kwargs = self._check_kwargs("axvline", kws, **kwargs)
        self._ext_ymin = self._ext_ymax = True
        return self._plot(x, (ymin, ymax), settings={"axvline": None}, **kwargs)

    def axhline(self, y, xmin=0, xmax=1, **kwargs):
        kws = {"fmt", "base", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "label"}
        kwargs = self._check_kwargs("axhline", kws, **kwargs)
        if isinstance(self, Secondary):
            self._primary._ext_xmin = self._primary._ext_xmax = True
        else:
            self._ext_xmin = self._ext_xmax = True
        return self._plot((xmin, xmax), y, settings={"axhline": None}, **kwargs)

    def axvspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        kws = {"c", "color", "alpha", "label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("axvspan", kws, **kwargs)
        self._ext_ymin = self._ext_ymax = True
        if TikzConfig.USE_GROUPPLOTS:
            self._axis_args.add("set layers")
        return self._plot([xmin, xmax], [ymin, ymax], settings={"axvspan": None}, **kwargs)

    def axhspan(self, ymin, ymax, xmin=0, xmax=1, **kwargs):
        kws = {"c", "color", "alpha", "label", "hatch", "hatch_color", "hatch_linewidth", "hatch_distance"}
        kwargs = self._check_kwargs("axhspan", kws, **kwargs)
        if isinstance(self, Secondary):
            self._primary._ext_xmin = self._primary._ext_xmax = True
        else:
            self._ext_xmin = self._ext_xmax = True
        if TikzConfig.USE_GROUPPLOTS:
            self._axis_args.add("set layers")
        return self._plot([xmin, xmax], [ymin, ymax], settings={"axhspan": None}, **kwargs)

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
                if isinstance(self, Secondary):
                    st["anchor"] = "south west"
                else:
                    st["anchor"] = "south east"
            elif loc == "bottom":
                st["at"] = "{(yticklabel cs:0)}"
                if isinstance(self, Secondary):
                    st["anchor"] = "south west"
                else:
                    st["anchor"] = "south east"
            else:
                st["at"] = {}
                st["anchor"] = {}
        if "rotate" in kwargs:
            if kwargs["rotate"] not in ["vertical", "horizontal"]:
                raise Warning(f"Invalid rotate: {kwargs['rotate']}. Must be one of 'vertical' or 'horizontal'.")
            if kwargs["rotate"] == "horizontal":
                if isinstance(self, Secondary):
                    st["rotate"] = "-90"
                else:
                    st["rotate"] = "-90"
            else:
                st["rotate"] = {}
        if st:
            self._update_axis_options("y label style", st)
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
            self._update_axis_options("y tick style", st)
        if labels:
            self._axis_options["yticklabels"]=f"{{{tex_text(','.join(labels))}}}"
        else:
            self._axis_options["yticklabels"]=r"{}"
            self._yticks = False

    def tick_params(self, axis="both", **kwargs):
        kws = {"color", "c", "labelsize", "labelcolor", "colors", "direction", "top", "bottom", "left", "right"}
        kwargs = self._check_kwargs("tick_params", kws, **kwargs)
        if axis not in ["x", "y", "both"]:
            raise Warning(f"Invalid axis: {axis}. Must be one of 'x', 'y', or 'both'.")
        if isinstance(self, Secondary):
            if axis != "y":
                raise Warning("tick_params only supports axis='y' for secondary axes.")
        X_POS_MAP = {"top": (True, False), "bottom": (False, True), "both": (True, True), "none": (False, False)}
        Y_POS_MAP = {"left": (True, False), "right": (False, True), "both": (True, True), "none": (False, False)}
        xt_b, xt_t = X_POS_MAP.get(kwargs.pop("xtick pos", "both"), (True, True))
        yt_l, yt_r = Y_POS_MAP.get(kwargs.pop("ytick pos", "both"), (True, True))
        prefix = "x" if axis == "x" else ("y" if axis == "y" else "")
        if "bottom" in kwargs:
            if axis == "y":
                raise Warning("Cannot set 'bottom' for y-axis.")
            xt_b = kwargs.pop("bottom")
        if "top" in kwargs:
            if axis == "y":
                raise Warning("Cannot set 'top' for y-axis.")
            xt_t = kwargs.pop("top")
        if "left" in kwargs:
            if axis == "x":
                raise Warning("Cannot set 'left' for x-axis.")
            yt_l = kwargs.pop("left")
        if "right" in kwargs:
            if axis == "x":
                raise Warning("Cannot set 'right' for x-axis.")
            yt_r = kwargs.pop("right")
        X_INV = {v: k for k, v in X_POS_MAP.items()}
        Y_INV = {v: k for k, v in Y_POS_MAP.items()}
        self._axis_options["xtick pos"] = X_INV[(xt_t, xt_b)]
        self._axis_options["ytick pos"] = Y_INV[(yt_l, yt_r)]
        if self._axis_options["xtick pos"] == "both":
            self._axis_options.pop("xtick pos")
        if self._axis_options["ytick pos"] == "both":
            self._axis_options.pop("ytick pos")
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
        if isinstance(self, Axes) or isinstance(self, Secondary):
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

        if "facecolor" in kwargs and (isinstance(self, Axes) or isinstance(self, Secondary)):
            ccode = self._match_color(kwargs["facecolor"])
            if ccode is not None:
                legend_string["fill"] = ccode
        if "edgecolor" in kwargs and (isinstance(self, Axes) or isinstance(self, Secondary)):
            ccode = self._match_color(kwargs["edgecolor"])
            if ccode is not None:
                legend_string["draw"] = ccode
        if "labelcolor" in kwargs and (isinstance(self, Axes) or isinstance(self, Secondary)):
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

    def text(self, x, y, s, **kwargs):
        kws = {"alpha", "color", "c", "fontsize", "on_top", "size", "backgroundcolor", "horizontalalignment", "ha", "verticalalignment", "va", "rotation", "label"}
        kwargs = self._check_kwargs("text", kws, **kwargs)
        if "fontsize" in kwargs or "size" in kwargs:
            kwargs["fontsize"] = kwargs.pop("size", kwargs.pop("fontsize"))
        on_top = kwargs.pop("on_top", True)
        if on_top:
            assert self._fig is not None
            coord = self._fig._next_coordinate_name()
            txt = Text(self, x, y, coord, s, **kwargs)
            self._fig._add_text(txt)
        else:
            txt = Text(self, x, y, None, s, **kwargs)
        self._elements[self._get_overlay()].append(txt)

    def magnify(self, x_p, y_p, x_m, y_m, zoom, size, **kwargs):
        kws = {"shape", "connect"}
        kwargs = self._check_kwargs("magnify", kws, **kwargs)
        assert self._fig is not None
        n = self._fig._add_spy(zoom, size, **kwargs)
        self._coordinates.update({f"spypoint{n}": (x_p,y_p)})
        self._coordinates.update({f"spyviewr{n}": (x_m,y_m)})

    def _add_legend_entries(self):
        if self._add_legend == []: return ""
        axs, labs = self._add_legend
        output = ""
        if len(axs) != len(labs):
            print("Legend: different number of plots and labels, ignoring.")
            return ""
        for i in range(len(axs)):
            output += f"\n\\addlegendimage{{{axs[i]._style_string().replace('\n', ' ')}}}"
            if self._legend_lab_col:
                output += f"\\addlegendentry[{self._legend_lab_col}]{{{tex_text(labs[i])}}}"
            else:
                output += f"\\addlegendentry{{{tex_text(labs[i])}}}"
        return output
        
    def _content_tex(self, filename):
        element_strings = {i: "\n".join(e._to_tex(filename, self._legend_lab_col) for e in self._elements[i]) for i in self._elements.keys()}
        if self._legend_on:
            element_strings[self._get_overlay()] += self._add_legend_entries()
        for coord in self._coordinates:
            x,y = self._coordinates[coord]
            element_strings[self._get_overlay()] += f"\n\\coordinate ({coord}) at ({x},{y});"
        return element_strings
    
    def _get_hard_range(self,which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self._axis_options:
            mode = self._axis_options[arg]
        if which in self._axis_options:
            for e in self._get_all_elements():
                e._filter(which, self._axis_options[which])
            return (self._axis_options[which], mode)
        return None, mode
    
    def _get_range(self, which):
        arg = f"{which[0]}mode"
        mode = "lin"
        if arg in self._axis_options:
            mode = self._axis_options[arg]
        common = self._get_all_elements().copy()
        if "x" in which and isinstance(self,Axes) and self._secondary_y:
            common += self._secondary_y._get_all_elements()
        if which in self._axis_options:
            for e in common:
                e._filter(which, self._axis_options[which])
            return (self._axis_options[which], True, mode)
        values = [e._get_erange(which) for e in common]
        if which in self._preferred_lims:
            values.append(self._preferred_lims[which])
        values = [v for v in values if v is not None]
        if not values:
            return (None, False, mode)
        if "min" in which:
            return (min(values), False, mode)
        return (max(values), False, mode)
    
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
        if isinstance(self, Axes):
            if which == "xmin":
                self._ext_xmin = True
            if which == "xmax":
                self._ext_xmax = True
        if which == "ymin":
            self._ext_ymin = True
        if which == "ymax":
            self._ext_ymax = True
        for e in self._get_all_elements():
            e._filter(which, value)

    def _num_points(self):
        return [e._num_points() for e in self._get_all_elements()]
    
    def _reduce_points(self, limit):
        for e in self._get_all_elements():
            e._reduce_points(limit)

    def _add_col(self, r,g,b):
        assert self._fig is not None
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
        self._style = self._fig._style
        self._imshow = None

        self._defcol_counter = {0: 0}
        self._colorbar = ""
        self._cbar_h = False
        self._polar = polar

        self._ext_xmin = False
        self._ext_xmax = False

        self._int_xmin = None
        self._int_xmax = None

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

        self._style_defaults()

    def _style_defaults(self):
        _gs = self._style._get_grid_cycle()
        if _gs is not None:
            self.grid(**_gs)
        _bcgnd = self._style._get_background_cycle()
        if _bcgnd is not None:
            self._axis_options["axis background/.style"] = f"{{{_bcgnd}}}"
        _add_settgs = copy.deepcopy(self._style._get_additional_settings())
        if _add_settgs is not None:
            self._axis_options = _add_settgs | self._axis_options

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

    def imshow(self, *args, **kwargs):
        #kws = {"fmt", "alpha", "color", "c", "linestyle", "ls", "linewidth", "lw", "marker", "markersize", "ms", "label"}
        #kwargs = self._check_kwargs("imshow", kws, **kwargs)
        self._imshow = (args, kwargs)
        self._axis_options["enlargelimits"] = "false"
        #self._fig._add_global("\\pgfplotsset{set layers}")
        data = args[0]
        m, M = _np.min(data), _np.max(data)
        if "cmap" in kwargs:
            cmap = kwargs["cmap"]
        else:
            cmap = "viridis"
        return (self, cmap, m, M)
    
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
                st["rotate"] = "-90"
            else:
                st["rotate"] = {}
        if st:
            self._update_axis_options("x label style", st)
        self._axis_options["xlabel"] = f"{{{tex_text(label)}}}"

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
            g = Graph(self, None, {}, None, None, **kwargs)._style_string()
            self._axis_options[f"{selector}grid style"] = f"{{{g}}}"
            
    def set_minorticks_num(self, num):
        self._axis_options["minor tick num"] = num

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

    def twinx(self):
        if self._polar:
            raise Exception("Cannot create twinx() on polar plot.")
        self._secondary_y = Secondary(self)
        self._ext_xmin = self._ext_xmax = True
        self.tick_params(axis="y", right=False)
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
        _plt.savefig(im_name, bbox_inches='tight', pad_inches=0)
        return im_name

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
            self._elements[0].insert(0, Graph(self, f"graphics [xmin={xm}, xmax={xM}, ymin={ym}, ymax={yM}] {{{im_name}}}", settings={}, xerr=None, yerr=None, onlayer="axis background"))
        axis_opt_str = ""
        auxiliary_opt_str = ""
        if TikzConfig.SCHOOL_AXIS:
            axis_opt_str += f",\n axis lines=middle,\n xlabel style={{at={{(ticklabel* cs:{1+TikzConfig.SCHOOL_AXIS_LABEL_MARGIN})}},anchor=north}},\n ylabel style={{at={{(ticklabel* cs:{1+TikzConfig.SCHOOL_AXIS_LABEL_MARGIN})}},anchor=east}}"
            if ("xmin" in self._axis_options and self._axis_options["xmin"] == 0) or ("xmax" in self._axis_options and self._axis_options["xmax"] == 0):
                self._axis_options["extra x ticks"] = r"{0}"
            if ("ymin" in self._axis_options and self._axis_options["ymin"] == 0) or ("ymax" in self._axis_options and self._axis_options["ymax"] == 0):
                self._axis_options["extra y ticks"] = r"{0}"
        if TikzConfig.USE_GROUPPLOTS:
            if "set layers" in self._axis_args:
                self._axis_args.remove("set layers")
            if TikzConfig.SCHOOL_AXIS:
                axis_opt_str += f",\n set layers,\n axis line style={{on layer=axis foreground}}"
                auxiliary_opt_str += ",\n set layers"
            else:
                axis_opt_str += f",\nset layers=standard, cell picture=true, grid style={{on layer=axis grid}}"
                auxiliary_opt_str += "set layers=standard"
        if self._axis_args:
            axis_opt_str = ",\n".join(self._axis_args) + axis_opt_str
            if "set layers" in self._axis_args:
                auxiliary_opt_str += ",\n set layers"
        if self._ext_xmin or self._ext_xmax:
            lower = self._get_range("xmin")
            upper = self._get_range("xmax")
            xm, xM = self._fig._range_setting(lower[0], upper[0], lower[2])
            if self._ext_xmin:
                self._axis_options["xmin"] = self._fig._next_limname("xmin", self._axis_options.get("xmin", xm))
            if self._ext_xmax:
                self._axis_options["xmax"] = self._fig._next_limname("xmax", self._axis_options.get("xmax", xM))
        elif self._int_xmin is not None or self._int_xmax is not None:
            lower = self._get_range("xmin")
            upper = self._get_range("xmax")
            if self._int_xmin is not None and (lower[0] is None or lower[0] >= self._int_xmin):
                self._axis_options["xmin"] = self._int_xmin
            if self._int_xmax is not None and (upper[0] is None or upper[0] <= self._int_xmax):
                self._axis_options["xmax"] = self._int_xmax
        if self._ext_ymin or self._ext_ymax:
            lower = self._get_range("ymin")
            upper = self._get_range("ymax")
            ym, yM = self._fig._range_setting(lower[0], upper[0], lower[2])
            if self._ext_ymin:
                self._axis_options["ymin"] = self._fig._next_limname("ymin", self._axis_options.get("ymin", ym))
            if self._ext_ymax:
                self._axis_options["ymax"] = self._fig._next_limname("ymax", self._axis_options.get("ymax", yM))
        elif self._int_ymin is not None or self._int_ymax is not None:
            lower = self._get_range("ymin")
            upper = self._get_range("ymax")
            if self._int_ymin is not None and (lower[0] is None or lower[0] >= self._int_ymin):
                self._axis_options["ymin"] = self._int_ymin
            if self._int_ymax is not None and (upper[0] is None or upper[0] <= self._int_ymax):
                self._axis_options["ymax"] = self._int_ymax
        if self._axis_options:
            if axis_opt_str: axis_opt_str += ",\n"
            if auxiliary_opt_str: auxiliary_opt_str += ",\n"
            for k, v in self._axis_options.items():
                if v != {}:
                    entry = self._parse_entry(k,v)
                    axis_opt_str += entry + ",\n"
                    if k in ["xmin", "xmax", "ymin", "ymax", "xmode", "ymode", "log basis x", "log basis y", "width", "height", "at"]:
                        auxiliary_opt_str += entry + ",\n"
        axis_opt_str = axis_opt_str.removesuffix(",,\n")
        auxiliary_opt_str = auxiliary_opt_str.removesuffix(",,\n")
        if self._colorbar:
            axis_opt_str += self._colorbar
        elif self._cmap_bar:
            axis_opt_str += f"colormap={self._cmap_bar._generate_tex_colormap(self._cmap_bar._cmap)},\n"
        return axis_opt_str, "hide axis,\n" + auxiliary_opt_str, alias

    def _parse_entry(self, k, v):
        if v is None:
            return f"{k}"
        if isinstance(v, dict):
            return f"{k}={{" + ",\n".join(f"{kk}={vv}" for kk, vv in v.items() if vv != {}) + "}"
        return f"{k}={v}"
    
    def _margins(self):
        left = TikzConfig.LEFT_PADDING + TikzConfig.YTICK_PADDING * self._yticks + TikzConfig.Y_LABEL_PADDING * ("ylabel" in self._axis_options)
        right = TikzConfig.RIGHT_PADDING + TikzConfig.CBAR_X_MARGIN * (self._colorbar != "" and not self._cbar_h)
        top = TikzConfig.TOP_PADDING + TikzConfig.TITLE_PADDING * ("title" in self._axis_options)
        bottom = TikzConfig.BOTTOM_PADDING  + TikzConfig.XTICK_PADDING * self._xticks + TikzConfig.X_LABEL_PADDING * ("xlabel" in self._axis_options) + TikzConfig.CBAR_Y_MARGIN * (self._colorbar != "" and self._cbar_h)
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
        for k,v in self._elements.items():
            if k in self._bar_labels and len(self._bar_labels[k]) > 0:
                if k in self._overlay_special and ("xbar stacked" in self._overlay_special[k] or "ybar stacked" in self._overlay_special[k]):
                    self._overlay_special[k].update({"nodes near coords": None})
                    for e in self._elements[k].copy():
                        if e not in self._bar_labels[k]:
                            self.bar_label(e, labels=[])
                    for e in self._elements[k]:
                        self._bar_labels[k][e]["stacked"] = True
                for e in self._bar_labels[k]:
                    e._add_bar_labels(**self._bar_labels[k][e])
            """if isinstance(v, list) and len(v) > 1:
                reference = getattr(v[0], "_settings", {}) or {}
                common_style = {s: val for s, val in reference.items() if all((getattr(obj, "_settings", {}) or {}).get(s) == val for obj in v[1:])}
                forbidden = {"draw", "fill", "xbar", "ybar"}
                for f in forbidden:
                    common_style.pop(f, None)
                for key, val in common_style.items():
                    for e in v:
                        e._settings.pop(key, None)
                    self._overlay_special[k].update({key: val}) """
        lines = []
        lines2 = []
        if self._polar:
            self._fig._add_required_package("\\usepgfplotslibrary{polar}")
        main_ax, aux_ax, alias = self._axis_option_string()
        contents = self._content_tex(filename)
        if self._polar and TikzConfig.USE_GROUPPLOTS and not single:
            lines.append(f"\\nextgroupplot[alias={self._axis_options['alias']}, width={self._width}, height={self._height}, hide axis]")
            for i in self._elements.keys():
                spec = ",\n".join([self._parse_entry(k, v) for k, v in self._overlay_special.get(i, {}).items()]) + ",\n" if i in self._overlay_special else ""
                lines2.append("\\begin{polaraxis}[")
                if i == self._get_overlay():
                    lines2.append(f"{main_ax}{spec}\n]")
                else:
                    lines2.append(f"{aux_ax}{spec}\n]")
                lines2.append(contents[i])
                lines2.append("\\end{polaraxis}")
        else:
            if TikzConfig.USE_GROUPPLOTS and not single:
                lines.append("\\nextgroupplot[")
            if self._polar:
                lines.append("\\begin{polaraxis}[")
            elif not TikzConfig.USE_GROUPPLOTS or (TikzConfig.USE_GROUPPLOTS and single):
                lines.append("\\begin{axis}[")
            if self._get_overlay() == 0:
                spec = ",\n".join([self._parse_entry(k, v) for k, v in self._overlay_special.get(0, {}).items()]) + ",\n" if 0 in self._overlay_special else ""
                if self._secondary_y is not None or self._colorbar is not None:
                    lines.append(f"{main_ax}{spec}alias={alias}\n]")
                else:
                    lines.append(f"{main_ax}{spec}\n]")
                lines.append(contents[0])
            else:
                spec = ",\n".join([self._parse_entry(k, v) for k, v in self._overlay_special.get(0, {}).items()]) + ",\n" if 0 in self._overlay_special else ""
                lines.append(f"{aux_ax}{spec}alias={alias}\n]")
                lines.append(contents[0])
                for i in self._elements.keys():
                    spec = ",\n".join([self._parse_entry(k, v) for k, v in self._overlay_special.get(i, {}).items()]) + ",\n" if i in self._overlay_special else ""
                    if i == 0: continue
                    lines2.append("\\begin{axis}[")
                    if i == self._get_overlay():
                        lines2.append(f"{main_ax}{spec}at={{({alias}.south west)}}\n]")
                        lines2.append(contents[i])
                        lines2 += self._overlay_legend_entries
                        add_l = self._add_legend_entries()
                        if add_l:
                            lines2.append(add_l)
                    else:
                        lines2.append(f"{aux_ax}{spec}at={{({alias}.south west)}}\n]")
                        lines2.append(contents[i])
                    lines2.append("\\end{axis}")
            if self._polar:
                lines.append("\\end{polaraxis}")
            elif not TikzConfig.USE_GROUPPLOTS or (TikzConfig.USE_GROUPPLOTS and single):            
                lines.append("\\end{axis}")
            if self._secondary_y is not None:
                main_ax2, aux_ax2 = self._secondary_y._axis_option_string()
                contents2 = self._secondary_y._content_tex(filename)
                for i in self._secondary_y._elements.keys():
                    lines2.append("\\begin{axis}[")
                    spec = ",\n".join([self._parse_entry(k, v) for k, v in self._secondary_y._overlay_special.get(i, {}).items()]) + ",\n" if i in self._secondary_y._overlay_special else ""
                    if i == sorted(self._secondary_y._elements.keys())[-1]:
                        lines2.append(f"{main_ax2}{spec}\n]")
                    else:
                        lines2.append(f"{aux_ax2}{spec}\n]")
                    lines2.append(contents2[i])
                    if i == sorted(self._secondary_y._elements.keys())[-1]:
                        lines2 += self._secondary_y._overlay_legend_entries
                        add_l = self._secondary_y._add_legend_entries()
                        if add_l:
                            lines2.append(add_l)
                    lines2.append("\\end{axis}")
        return lines, lines2

    def set(self, **kwargs):
        defined = {"title": self.set_title, "xlim": self.set_xlim, "xlabel": self.set_xlabel, "xscale": self.set_xscale, "xticklabels": self.set_xticklabels, "xticks": self.set_xticks}
        for attr in defined:
            if attr in kwargs:
                defined[attr](kwargs.pop(attr))

        super().set(**kwargs)

    def set_facecolor(self, color):
        ccode, _ = _tex_color(color, self._style)
        if isinstance(ccode, str):
            self._axis_options["axis background/.style"] = f"{{fill={ccode}}}"
        else:
            r,g,b = ccode
            self._add_col(r,g,b)
            self._axis_options["axis background/.style"] = f"{{fill=c{r:.3f}{g:.3f}{b:.3f}}}".replace(".", "")
    
class Secondary(BaseAxes):
    def __init__(self, primary):
        super().__init__()
        self._primary = primary

        self._axis_options["axis y line*"] = "right"
        self._axis_options["axis x line"] = "none"
        self._axis_options["at"] = f"{{({primary._axis_options['alias' if 'alias' in primary._axis_options else 'name']}.south west)}}"
        self._axis_options["anchor"] = "south west"
        self._update_axis_options("y label style", {"at": f"{{({TikzConfig.SEC_YLABEL_LOC[0]},{TikzConfig.SEC_YLABEL_LOC[1]})}}", "rotate": 180})

        self._fig = primary._fig
        self._style = self._fig._style
        self._style_defaults()

    def _style_defaults(self):
        _add_settgs = copy.deepcopy(self._style._get_additional_settings())
        if _add_settgs is not None:
            self._axis_options = _add_settgs | self._axis_options

    def _axis_option_string(self):
        if self._primary._width:
            self._axis_options["width"] = self._primary._width
        if self._primary._height:
            self._axis_options["height"] = self._primary._height
        axis_opt_str = ""
        auxiliary_opt_str = ""
        if self._axis_args:
            axis_opt_str += ",\n".join(self._axis_args)
        if self._ext_ymin or self._ext_ymax:
            lower = self._get_range("ymin")
            upper = self._get_range("ymax")
            ym, yM = self._fig._range_setting(lower[0], upper[0], lower[2])
            if self._ext_ymin:
                self._axis_options["ymin"] = self._fig._next_limname("ymin", self._axis_options.get("ymin", ym))
            if self._ext_ymax:
                self._axis_options["ymax"] = self._fig._next_limname("ymax", self._axis_options.get("ymax", yM))
        self._axis_options["xmin"] = self._primary._axis_options["xmin"]
        self._axis_options["xmax"] = self._primary._axis_options["xmax"]
        if self._axis_options:
            if axis_opt_str: axis_opt_str += ",\n"
            if auxiliary_opt_str: auxiliary_opt_str += ",\n"
            def parse_entry(k,v):
                if isinstance(v, dict):
                    return f"{k}={{" + ",\n".join(f"{kk}={vv}" for kk, vv in v.items()) + "}"
                else:
                    return f"{k}={v}"
            for k, v in self._axis_options.items():
                entry = parse_entry(k,v)
                axis_opt_str += entry + ",\n"
                if k in ["xmin", "xmax", "ymin", "ymax", "xmode", "ymode", "log basis x", "log basis y", "width", "height", "at"]:
                    auxiliary_opt_str += entry + ",\n"
        return axis_opt_str, auxiliary_opt_str
    
    def _padding(self):
        return TikzConfig.SEC_Y_PADDING + TikzConfig.YTICK_PADDING * self._yticks + TikzConfig.SEC_Y_LABEL_PADDING * ("ylabel" in self._axis_options)
    
    def _get_defcol(self, index = 0):
        return self._primary._get_defcol(index)
    
    def _get_index(self):
        return self._primary._get_index()