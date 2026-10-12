from .colors import _tex_color

class Arrow:
    _LINE_MAP = {"--": "dashed", ":": "dotted", "-.": "dashdotted", "-":"solid"}
    def __init__(self, ax, x1, y1, x2, y2, coordinate1, coordinate2, **kwargs):
        self._axes = ax
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._coordinate1 = coordinate1
        self._coordinate2 = coordinate2
        self._kwargs = kwargs
        self._opacity = 1
        self._visible = True

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
        if "arrowstyle" in self._kwargs:
            allowed = {"<", ">", "|", "stealth", "latex"}
            arstyle = self._kwargs["arrowstyle"]
            arstyle = arstyle.split("-")
            if not all(s in allowed for s in arstyle):
                raise ValueError(f"Arrow style {self._kwargs['arrowstyle']} not recognized. Valid options should consist of: {allowed}, separated by -.")
            output.append(self._kwargs["arrowstyle"])
        if "color" in self._kwargs or "c" in self._kwargs:
            self._color = self.match_color(self._kwargs.get("color") or self._kwargs.get("c"))
        if "alpha" in self._kwargs:
            self._opacity = self._kwargs["alpha"]
        if "line width" in self._kwargs or "lw" in self._kwargs:
            output.append("line width=" + str(self._kwargs.get("line width") or self._kwargs.get("lw")))
        if "linestyle" in self._kwargs or "ls" in self._kwargs:
            ls = self._kwargs.get("linestyle") or self._kwargs.get("ls")
            if ls in self._LINE_MAP:
                ls = self._LINE_MAP[ls]
            elif ls not in self._LINE_MAP.values():
                raise ValueError(f"Line style {ls} not recognized. Valid options are: {list(self._LINE_MAP.keys())}.")
            output.append("line style=" + str(ls))
        if self._opacity < 1:
            output.insert(0,f"opacity={self._opacity}")
        if self._color:
            output.insert(0,f"color={self._color}")
        return ", ".join(output)

    def _to_tex(self, *args, **kwargs):
        if self._visible:
            if self._coordinate1 is not None:
                return f"\\coordinate {self._coordinate1} at (axis cs:{self._x1},{self._y1});"
        else:
            return ""
        
    def _to_tex_fin(self):
        if self._visible:
            if self._coordinate1 is not None and self._coordinate2 is not None:
                return f"\\draw[{self._style_string()}] {self._coordinate2} -- {self._coordinate1};"
        else:
            return ""

    def _filter(self, which, label):
        pass

    def _get_erange(self, which):
        if which == "xmin":
            return min(self._x1, self._x2)
        elif which == "xmax":
            return max(self._x1, self._x2)
        elif which == "ymin":
            return min(self._y1, self._y2)
        elif which == "ymax":
            return max(self._y1, self._y2)

    def _num_points(self):
        return 2
    
    def _reduce_points(self, max_points):
        pass