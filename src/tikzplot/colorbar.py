import numpy as _np
from .axes import Graph
from .config import TikzConfig

class _Colorbar:
    def __init__(self, im=None, **kwargs):
        self._axis = None
        self._cmap = None
        self._lower = 0
        self._upper = 1
        #self._ticks = None
        #self._log = False
        self._label = None
        self._width = 0.3

        if im is not None:
            self._axis, self._cmap, self._lower, self._upper = im

        if "cmap" in kwargs:
            self._cmap = kwargs["cmap"]
        if "lower" in kwargs:
            self._lower = kwargs["lower"]
        if "upper" in kwargs:
            self._upper = kwargs["upper"]
        """if "ticks" in kwargs:
            self._ticks = kwargs["ticks"]
        if "scale" in kwargs and kwargs["scale"]:
            self._log = True"""
        if "label" in kwargs:
            self._label = kwargs["label"]
        if "width" in kwargs:
            self._width = kwargs["width"]
        self._axis._show_colorbar(str(self))

    dictionary = {
        'viridis': [(0.2670, 0.0049, 0.3294), (0.2297, 0.3224, 0.5457), (0.1276, 0.5670, 0.5505), (0.3692, 0.7889, 0.3853), (0.9932, 0.9062, 0.1439)],
        'plasma':  [(0.0504, 0.0298, 0.5280), (0.4927, 0.0132, 0.6602), (0.7982, 0.2802, 0.4697), (0.9733, 0.5854, 0.2319), (0.9400, 0.9752, 0.1313)],
        'inferno': [(0.0015, 0.0005, 0.0139), (0.3415, 0.0624, 0.4298), (0.7359, 0.2159, 0.3302), (0.9784, 0.5545, 0.0313), (0.9883, 0.9983, 0.6449)],
        'magma':   [(0.0015, 0.0012, 0.0133), (0.3119, 0.0729, 0.4831), (0.7100, 0.2128, 0.4770), (0.9631, 0.5038, 0.3801), (0.9871, 0.9744, 0.7298)],
        'cividis': [(0.0000, 0.1351, 0.3049), (0.1915, 0.3121, 0.4354), (0.4863, 0.4893, 0.4754), (0.7838, 0.6865, 0.4430), (0.9957, 0.9092, 0.2178)],
        'coolwarm': [(0.2298, 0.2987, 0.7537), (0.8650, 0.8650, 0.8650), (0.7057, 0.0155, 0.1502)],
        'RdBu':     [(0.4039, 0.0000, 0.1216), (0.9686, 0.9686, 0.9686), (0.0196, 0.1882, 0.3804)],
        'seismic':  [(0.0000, 0.0000, 0.3000), (1.0000, 1.0000, 1.0000), (0.5000, 0.0000, 0.0000)],
        'PRGn':     [(0.2510, 0.0000, 0.2941), (0.9686, 0.9686, 0.9686), (0.0000, 0.2667, 0.1059)],
        'Greys':   [(1.0000, 1.0000, 1.0000), (0.0000, 0.0000, 0.0000)],
        'Blues':   [(0.9686, 0.9843, 0.9922), (0.0314, 0.1882, 0.4196)],
        'Reds':    [(1.0000, 0.9608, 0.9412), (0.4039, 0.0000, 0.0510)],
        'Greens':  [(0.9686, 0.9882, 0.9608), (0.0000, 0.2667, 0.1059)],
        'Oranges': [(0.9961, 0.9412, 0.8510), (0.4980, 0.1529, 0.0157)],
        'Purples': [(0.9922, 0.9922, 0.9922), (0.2510, 0.0000, 0.4471)],
        'YlOrRd':  [(1.0000, 1.0000, 0.8000), (0.9961, 0.7020, 0.2196), (0.5020, 0.0000, 0.1490)],
        'jet':     [(0.0000, 0.0000, 0.5000), (0.0000, 1.0000, 1.0000), (0.5000, 1.0000, 0.5000), (1.0000, 1.0000, 0.0000), (0.5000, 0.0000, 0.0000)],
        'hsv':     [(1.0000, 0.0000, 0.0000), (0.0000, 1.0000, 0.0000), (0.0000, 0.0000, 1.0000), (1.0000, 0.0000, 0.0000)],
        'terrain': [(0.2000, 0.2000, 0.6000), (0.0000, 0.6000, 0.0000), (0.6000, 0.6000, 0.0000), (1.0000, 1.0000, 1.0000)]
}
    def generate_tex_colormap(self, cmap_name):
        rev = False
        if cmap_name.endswith("_r"):
            rev = True
            cmap_name = cmap_name.removesuffix("_r")
        if cmap_name not in self.dictionary:
            raise Exception(f"% Error: {cmap_name} not found in dictionary")
        colors = self.dictionary[cmap_name]
        if rev: colors=reversed(colors)
        output = [r"{urgb}{"]
        for r, g, b in colors:
            output.append(f"    rgb=({r:.4f}, {g:.4f}, {b:.4f})")
        output.append("}")        
        return "\n".join(output)
    
    def __str__(self):
        lines = []
        lines.append(f"colormap={self.generate_tex_colormap(self._cmap)},")
        lines.append("colorbar,")
        lines.append(r"colorbar style={")
        if TikzConfig.USE_DECIMAL_COMMA:
            lines.append("/pgf/number format/use comma,")
        lines.append(f"width={self._width}cm,")
        if self._label:
            lines.append(f"title={{{self._label}}},")
            lines.append(f"title style={{at={{(3,0.5)}}, anchor=south, rotate=-90}},")

        lines.append(r"},")
        lines.append(f"point meta min={{{self._lower}}},")
        lines.append(f"point meta max={{{self._upper}}}")

        return "\n".join(lines)
    
Colorbar = _Colorbar