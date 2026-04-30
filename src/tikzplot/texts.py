from .colors import _tex_color

class Text:
    def __init__(self, ax, x, y, s, **kwargs):
        self._axes = ax
        self._x = x
        self._y = y
        self._s = s
        self._kwargs = kwargs
        self._color = False
        self._opacity = 1
        self._fsize = None
        self._label = kwargs.get("label", None)
        self._visible = True

    _FONT_SIZES = {"xx-small": r"\tiny", "x-small": r"\scriptsize", "small": r"\footnotesize", "medium": r"\normalsize", "large": r"\large", "x-large": r"\Large", "xx-large": r"\LARGE"}

    def match_color(self, input):
            self._has_color = True
            ccode, op = _tex_color(input)
            if not isinstance(op, bool):
                self._opacity = op
            if isinstance(ccode, str):
                return ccode
            r,g,b=ccode
            self._axes._add_col(r,g,b)
            return f"c{r:.3f}{g:.3f}{b:.3f}".replace(".", "")

    def _style_string(self):
        output = []
        if "color" in self._kwargs or "c" in self._kwargs:
            self._color = self.match_color(self._kwargs.get("color") or self._kwargs.get("c"))
        if "alpha" in self._kwargs:
            self._opacity = self._kwargs["alpha"]
        if "fontsize" in self._kwargs or "size" in self._kwargs:
            size = self._kwargs.get('fontsize') or self._kwargs.get('size')
            if size in self._FONT_SIZES:
                self._fsize = self._FONT_SIZES[size]
            else:
                raise ValueError(f"Font size {size} not recognized. Valid sizes are: {', '.join(self._FONT_SIZES.keys())}")
        if "backgroundcolor" in self._kwargs:
            bg_color = self.match_color(self._kwargs["backgroundcolor"])
            output.append(f"fill={bg_color}")
        if "horizontalalignment" in self._kwargs or "ha" in self._kwargs:
            ha = self._kwargs.get("horizontalalignment") or self._kwargs.get("ha")
            if ha in {"center", "left", "right"}:
                if ha in {"left", "right"}:
                    output.append(ha)
            else:
                raise ValueError(f"Horizontal alignment {ha} not recognized. Valid options are: center, left, right.")
        if "verticalalignment" in self._kwargs or "va" in self._kwargs:
            va = self._kwargs.get("verticalalignment") or self._kwargs.get("va")
            if va in {"center", "top", "bottom"}:
                if va == "top":
                    output.append("above")
                elif va == "bottom":
                    output.append("below")
            else:
                raise ValueError(f"Vertical alignment {va} not recognized. Valid options are: center, top, bottom.")
        if "rotation" in self._kwargs:
            if isinstance(self._kwargs["rotation"], str):
                if self._kwargs["rotation"] == "vertical":
                    output.append("rotate=90")
                elif self._kwargs["rotation"] == "horizontal":
                    pass
            elif isinstance(self._kwargs["rotation"], (int, float)):
                output.append(f"rotate={self._kwargs['rotation']}")
            else:
                raise ValueError(f"Rotation value {self._kwargs['rotation']} not recognized. Valid options are: vertical, horizontal, or a numeric angle.")
        if self._opacity < 1:
            output.insert(0,f"opacity={self._opacity}")
        if self._color:
            output.insert(0,f"color={self._color}")
        return ", ".join(output)


    def _to_tex(self, _):
        if self._visible:
            return f"\\node[{self._style_string()}] at (axis cs:{self._x},{self._y}) {{{self._fsize or ''}{self._s}}};"
        else:
            return ""
    
    def _set_label(self, label):
        self._label = label

    def _filter(self, which, value):
        if (which == "xmin" and self._x < value) or (which == "xmax" and self._x > value) or (which == "ymin" and self._y < value) or (which == "ymax" and self._y > value):
            self._visible = False
    
    def _get_erange(self, which):
        if which in {"xmin", "xmax"}:
            return self._x
        elif which in {"ymin", "ymax"}:
            return self._y
    
    def _num_points(self):
        return 1
    
    def _reduce_points(self, max_points):
        pass

class Text3(Text):
    def __init__(self, ax, x, y, z, s, **kwargs):
        super().__init__(ax, x, y, s, **kwargs)
        self._z = z

    def _to_tex(self, _):
        if self._visible:
            return f"\\node[{self._style_string()}] at (axis cs:{self._x},{self._y},{self._z}) {{{self._fsize or ''}{self._s}}};"
        else:
            return ""
    
    def _get_erange(self, which):
        if which in {"xmin", "xmax"}:
            return self._x
        elif which in {"ymin", "ymax"}:
            return self._y
        elif which in {"zmin", "zmax"}:
            return self._z