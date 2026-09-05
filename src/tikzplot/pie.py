import numpy as _np

from .colors import _tex_color
from .config import TikzConfig

class Pie:
    def __init__(self, ax, x, explode=None, labels=None, colors=None, autopct=None, pctdistance=0.6, labeldistance=1.1, radius=1, startangle=0, counterclock=True, wedgeprops=None, rotate_labels=False, normalize=True, at=None):
        self._axes = ax
        self._x = x
        self._explode = explode
        self._labels = labels
        self._colors = colors
        self._autopct = autopct
        self._pctdistance = pctdistance
        self._labeldistance = labeldistance
        self._radius = radius
        self._startangle = startangle
        self._counterclock = counterclock
        self._wedgeprops = wedgeprops or {}
        self._normalize = normalize
        self._textprops = None
        self._rotate_labels = rotate_labels
        self._alignment = "auto"
        self._at = at

    def _match_color(self, input):
        ccode, op = _tex_color(input)
        if not isinstance(op, bool):
            self._opacity = op
        if isinstance(ccode, str):
            return ccode
        r,g,b=ccode
        self._axes._add_col(r,g,b)
        return f"c{r:.3f}{g:.3f}{b:.3f}".replace(".", "")

    def _add_labels(self, labels, distance=0.6, textprops=None, rotate=False, alignment="auto"):
        self._labels = labels
        self._labeldistance = distance
        if self._textprops is not None:
            self._textprops = self._textprops | textprops
        self._rotate_labels = rotate
        self._alignment = alignment

    def _to_tex(self, *args, **kwargs):
        options = {}
        w,h = self._axes._axis_options.get("width", 6), self._axes._axis_options.get("height", 4)
        size = min(float(w.removesuffix("cm")), float(h.removesuffix("cm")))
        n = len(self._x)
        if self._at is not None:
            options["at"] = f"{{({self._at})}}"
        scale_fac = TikzConfig.PIE_SIZE_FRACTION * size / 2
        if self._radius is not None:
            if isinstance(self._radius, (int, float)):
                r = self._radius * scale_fac
                options["outer radius"] = r
            else:
                self._radius = _np.asarray(self._radius)
                if len(self._radius) != n: raise ValueError(f"Length of radius ({len(self._radius)}) does not match number of wedges ({n})")
                r = [v * scale_fac for v in self._radius]
                options["outer radius{list}"] = "{" + ",".join(str(v) for v in r) + "}"
        if "width" in self._wedgeprops:
            options["inner radius"] = self._wedgeprops["width"] * scale_fac
        else:
            options["inner radius"] = 0
        if self._explode is not None:
            if isinstance(self._explode, (int, float)):
                options["explode"] = self._explode * scale_fac
            else:
                e = [v * scale_fac for v in self._explode]
                options["explode{list}"] = "{" + ",".join(str(v) for v in e) + "}"
        if self._labels:
            if len(self._labels) != n: raise ValueError(f"Length of labels ({len(self._labels)}) does not match number of wedges ({n})")
            options["data{list}"] = "{" + ",".join(str(v) for v in self._labels) + "}"
        if self._normalize:
            total = sum(self._x)
            if total != 0:
                self._x = [v / total for v in self._x]
        if self._autopct:
            options["wheel data{list}"] = "{" + ",".join(self._autopct % (100 * d) for d in self._x).replace("%", "\\%") + "}"
        if self._colors is None:
            self._colors = [self._match_color("C" + str(i)) for i in range(n)]
        else:
            self._colors = [self._match_color(c) for c in self._colors]
        if self._pctdistance is not None:
            options["wheel data pos"] = self._pctdistance
        if self._labeldistance is not None:
            options["data pos"] = self._labeldistance * 0.85
            options["data sep"] = 0
        if self._counterclock:
            options["counterclockwise"] = None
        if self._startangle is not None and self._startangle != 0:
            options["start angle"] = _np.deg2rad(self._startangle)
        if self._rotate_labels:
            if "data style" not in options:
                options["data style"] = {}
            options["data style"]["rotate"] = "\\WCdataangle"
            if self._alignment == "auto" or self._alignment == "outer":
                options["data style"]["right"] = {}
            options["data style"]["right"] = {}
        output = []
        for k,v in options.items():
            if v is None:
                output.append(f"{k}")
            elif isinstance(v, dict):
                inner = "{"
                for k2,v2 in v.items():
                    if v2 is None:
                        inner += f"{k2},"
                    else:
                        inner += f"{k2}={v2},"
                inner = inner.removesuffix(",")
                inner += "}"
                output.append(f"{k}={inner}")
            else:
                output.append(f"{k}={v}")
        return f"\\wheelchart[{',\n'.join(output)}]\n{{{', '.join(f'{self._x[i]}/{self._colors[i]}/' for i in range(n))}}}"

    def _style_string(self):
        assert self._colors is not None and len(self._colors) == len(self._x)
        return [f"fill={self._colors[i]}" for i in range(len(self._colors))]

    
    def _num_points(self):
        return 1
    
    def _reduce_points(self, max_points):
        pass