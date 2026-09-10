import numpy as _np
import copy

from .axes import Axes
from .axes3d import Axes3
from .config import TikzConfig
from .border_finder import _can_compile_tex

class Figure:

    def __init__(self, style):
        self._axes = {}
        self._style = style
        self._width = TikzConfig.DEFAULT_WIDTH
        self._height = TikzConfig.DEFAULT_HEIGHT

        self._sharex = None
        self._sharey = None

        self._nrows = 0
        self._ncols = 0

        self._spacings = None

        self._tight_params = {}
        
        self._last_path_num = 0

        self._col_dict = {}

        self._globals = set()
        self._spies = []
        self._external = []

        self._num_coordinates = 0

        self._texts = []

        self._lims = {"xmin": {}, "xmax": {}, "ymin": {}, "ymax": {}, "zmin": {}, "zmax": {}}

        self._required_packages: dict[str, int] = {} # int for priority: 0-tikz, 1-pgfplots, 2-other packages, 3-pgfplotsset, 4-tikzlibraries, 5-pgfplotslibraries

        self._mosaic = {}
        self._wratios, self._hratios = None, None
        self._xshare: list[list] = []
        self._yshare: list[list] = []

    def add_subplot(self, *args, sharex=None, sharey=None, projection=None, polar=False):
        nrows = ncols = index = 1
        if len(args) == 0: pass
        elif len(args) == 1:
            q = args[0]
            if isinstance(q, int) and q >= 111:
                nrows, ncols, index = int(str(args[0])[0]), int(str(args[0])[1]), int(str(args[0])[2])
        elif len(args) == 3:
            nrows, ncols, index = args
            if not (isinstance(nrows, int) and isinstance(ncols, int) and isinstance(index, int)):
                raise ValueError("nrows, ncols, index must be integers")
        else:
            raise ValueError("Invalid number of arguments for add_subplot")

        if projection=="3d":
            ax = Axes3(nrows, ncols, index, self)
        else:
            pol: bool = projection=="polar" or polar
            ax = Axes(nrows, ncols, index, self, pol)
        if self._nrows != 0 and self._ncols != 0 and (self._nrows != nrows or self._ncols != ncols):
            raise ValueError("Cannot add subplot with different nrows/ncols than existing subplots")
        self._nrows = nrows
        self._ncols = ncols
        if index in self._axes:
            return self._axes[index]
        self._axes[index] = ax
        if sharex:
            self._sharex = sharex
        if sharey:
            self._sharey = sharey
        return ax

    def subplots(self, nrows=1, ncols=1, sharex=None, sharey=None, subplot_kw=None, **kwargs):
        axes = self._add_subplots(nrows, ncols, sharex, sharey, subplot_kw)
        if nrows * ncols == 1:
            return axes[0]
        grid = []
        k = 0
        for _ in range(nrows):
            row = []
            for _ in range(ncols):
                row.append(axes[k])
                k += 1
            grid.append(row)
        grid = _np.asarray(grid)
        if grid.shape[0] == 1:
            grid = grid[0]
        else:
            assert len(grid.shape) == 2
            if grid.shape[1] == 1:
                grid = grid[:,0]
        if "figsize" in kwargs:
            self.set_size_inches(kwargs["figsize"])
        return grid
      
    def _add_subplots(self, nrows, ncols, sharex=None, sharey=None, subplot_kw=None):
        grid = []
        if sharex:
            self._sharex = sharex
        if sharey:
            self._sharey = sharey
        for i in range(1, nrows * ncols + 1):
            if subplot_kw:
                if "projection" in subplot_kw:
                    ax = self.add_subplot(nrows, ncols, i, sharex=sharex, sharey=sharey, projection=subplot_kw["projection"])
                else:
                    ax = self.add_subplot(nrows, ncols, i, sharex=sharex, sharey=sharey)
            else:
                ax = self.add_subplot(nrows, ncols, i, sharex=sharex, sharey=sharey)
            grid.append(ax)
        return grid
    
    def subplot_mosaic(self, mosaic, *, sharex=False, sharey=False, width_ratios=None, height_ratios=None, empty_sentinel=".", subplot_kw=None, **kwargs):
        if not TikzConfig.USE_GROUPPLOTS:
            raise Warning("subplot_mosaic is only available when using groupplots (TikzConfig.USE_GROUPPLOTS). Command will be ignored.")
        if isinstance(mosaic, str):
            mosaic = [list(row) for row in mosaic.splitlines() if row]
        nrows = len(mosaic)
        ncols = max(len(row) for row in mosaic)
        for r in range(nrows):
            if len(mosaic[r]) < ncols:
                raise ValueError(f"All rows of mosaic must have the same length.")
        grid = {}
        for r in reversed(range(nrows)):
            for c in range(ncols):
                n = mosaic[r][c]
                if r < nrows - 1 and c > 0 and mosaic[r+1][c] == mosaic[r][c-1] != n:
                    raise ValueError(f"Invalid mosaic: {n} is not a contiguous block")
                if n != empty_sentinel:
                    if n in grid:
                        if grid[n]["r"] < r or grid[n]["c"] > c:
                            raise ValueError(f"Invalid mosaic: {n} is not a contiguous block")
                        for i in range(grid[n]["r"], r+1):
                            for j in range(grid[n]["c"], c+1):
                                if i == r and j == c:
                                    continue
                                if mosaic[i][j] != n:
                                    raise ValueError(f"Invalid mosaic: {n} is not a contiguous block")
                        grid[n]["nr"] = max(grid[n]["nr"], grid[n]["r"] - r + 1)
                        grid[n]["nc"] = max(grid[n]["nc"], c - grid[n]["c"] + 1)
                    else:
                        grid[n] = dict(r=r, c=c, nr=1, nc=1)
        for n in grid:
            grid[n]["ax"] = self.add_subplot(nrows, ncols, ncols * grid[n]["r"] + grid[n]["c"] + 1, sharex=sharex, sharey=sharey)
        self._mosaic = grid
        if width_ratios is not None:
            if len(width_ratios) != ncols:
                raise ValueError(f"width_ratios must have length {ncols}")
            self._wratios = list(width_ratios)
        if height_ratios is not None:
            if len(height_ratios) != nrows:
                raise ValueError(f"height_ratios must have length {nrows}")
            self._hratios = list(height_ratios)
        return {n: grid[n]["ax"] for n in grid}

    def _inset(self, ax, position, relsize=1, sharex=False, sharey=False):
        if not TikzConfig.USE_GROUPPLOTS:
            raise Warning("inset_axes is only available when using groupplots (TikzConfig.USE_GROUPPLOTS).")
        if not self._mosaic:
            for ax in self._axes.values():
                self._mosaic[ax._index] = dict(r=ax._get_row(), c=ax._get_col(), nr=1, nc=1, ax=ax)

        ax_n = next(n for n in self._mosaic if self._mosaic[n]["ax"] == ax)
        target_r = self._mosaic[ax_n]["r"]
        target_c = self._mosaic[ax_n]["c"]
        target_nr = self._mosaic[ax_n]["nr"]            
        target_nc = self._mosaic[ax_n]["nc"]            
        target_r_top = target_r - target_nr + 1

        def insert_col(idx):
            self._ncols += 1
            for n in self._mosaic:
                cc = self._mosaic[n]["c"]
                nnc = self._mosaic[n]["nc"]
                cc_right = cc + nnc - 1
                if cc >= idx:
                    self._mosaic[n]["c"] += 1
                elif cc < idx and cc_right >= idx:
                    self._mosaic[n]["nc"] += 1
        def insert_row(idx):
            self._nrows += 1
            for n in self._mosaic:
                rr = self._mosaic[n]["r"]
                nnr = self._mosaic[n]["nr"]
                rr_top = rr - nnr + 1
                if rr_top >= idx:
                    self._mosaic[n]["r"] += 1
                elif rr_top < idx and rr >= idx:
                    self._mosaic[n]["r"] += 1
                    self._mosaic[n]["nr"] += 1
        def get_free_name():
            n = 1
            while True:
                nm = f"i{n}"
                if nm not in self._mosaic:
                    return nm
                n += 1
        sum_h, sum_w = 0, 0
        if position in ("above", "below") and self._hratios is not None:
            h_slice = self._hratios[target_r_top : target_r_top + target_nr]
            sum_h = sum(h_slice) if h_slice else 0
        if position in ("left", "right") and self._wratios is not None:
            w_slice = self._wratios[target_c : target_c + target_nc]
            sum_w = sum(w_slice) if w_slice else 0

        new_name = get_free_name()
        if position == "left":
            insert_col(target_c)
            new_axes = Axes(self._nrows, self._ncols, 0, self, False)
            self._mosaic[new_name] = dict(r=target_r, c=target_c, nr=target_nr, nc=1, ax=new_axes)
            if self._wratios is not None:
                self._wratios.insert(target_c, sum_w * relsize)
        elif position == "right":
            insert_col(target_c + target_nc)
            new_axes = Axes(self._nrows, self._ncols, 0, self, False)
            self._mosaic[new_name] = dict(r=target_r, c=target_c + target_nc, nr=target_nr, nc=1, ax=new_axes)
            if self._wratios is not None:
                self._wratios.insert(target_c + target_nc, sum_w * relsize)
        elif position == "above":
            insert_row(target_r_top)
            new_axes = Axes(self._nrows, self._ncols, 0, self, False)
            self._mosaic[new_name] = dict(r=target_r_top, c=target_c, nr=1, nc=target_nc, ax=new_axes)
            if self._hratios is not None:
                self._hratios.insert(target_r_top, sum_h * relsize)
        else: # below
            insert_row(target_r + 1)
            new_axes = Axes(self._nrows, self._ncols, 0, self, False)
            self._mosaic[new_name] = dict(r=target_r + 1, c=target_c, nr=1, nc=target_nc, ax=new_axes)
            if self._hratios is not None:
                self._hratios.insert(target_r + 1, sum_h * relsize)

        if sharex:
            self._xshare.append([ax, new_axes])
        if sharey:
            self._yshare.append([ax, new_axes])
        temp = {}
        for n in self._mosaic:
            nax = self._mosaic[n]["ax"]
            i = self._mosaic[n]["c"] + 1 + (self._mosaic[n]["r"]) * self._ncols
            nax._new_pos(self._nrows, self._ncols, i)
            temp[i] = nax
        self._axes = temp.copy()
        return new_axes

    def set_size_inches(self, *args):
        if isinstance(args[0], tuple):
            args = args[0]
        try:
            w,h = args
            self._width = w * 2.5
            self._height = h * 2.5
            for ax in self._axes.values():
                ax._update_size()
        except:
            pass

    def delaxes(self, ax):
        if ax in self._axes.values():
            key = [k for k, v in self._axes.items() if v == ax][0]
            del self._axes[key]
            del ax
    
    def _compute_group_spacing(self, cpy=None):
        grid = _np.zeros((self._nrows, self._ncols, 6))
        for i, ax in self._axes.items():
            if cpy is None:
                grid[ax._get_row(), ax._get_col()][:4] = _np.array(ax._margins())
            else:
                cpy._check_required_packages()
                pre = "\n".join(cpy._required_packages.keys())
                szs = cpy._axes[i]._simulated_margins(pre)
                grid[ax._get_row(), ax._get_col()] = _np.array(szs)
        l = grid[:, :, 0]
        r = grid[:, :, 1]
        t = grid[:, :, 2]
        b = grid[:, :, 3]
        if "rect" in self._tight_params:
            w, h = self._width / self._ncols, self._height / self._nrows
            l += self._tight_params["rect"][0] * w
            r += (1-self._tight_params["rect"][2]) * w
            b += self._tight_params["rect"][1] * h
            t += (1-self._tight_params["rect"][3]) * h
        if self._nrows > 1:
             row_spacing = _np.max(b[:-1, :], axis=1) + _np.max(t[1:, :], axis=1)
        else:
            row_spacing = [0]
        if self._ncols > 1:
            col_spacing = _np.max(r[:, :-1], axis=0) + _np.max(l[:, 1:], axis=0)
        else:
            col_spacing = [0]
        if "h_pad" in self._tight_params:
            row_spacing += self._tight_params["h_pad"]
        if "w_pad" in self._tight_params:
            col_spacing += self._tight_params["w_pad"]
        if cpy is not None:
            aw, ah = _np.sum(_np.max(grid[:, :, 4], axis=0)), _np.sum(_np.max(grid[:, :, 5], axis=1))
            mw = _np.max(l[:, 0]) + _np.max(r[:, -1]) + max(col_spacing) * (self._ncols - 1) + aw
            mh = _np.max(t[0, :]) + _np.max(b[-1, :]) + max(row_spacing) * (self._nrows - 1) + ah
            wrs, hrs = self._wratios, self._hratios
            if wrs is None:
                wrs = [1] * self._ncols
            if hrs is None:
                hrs = [1] * self._nrows
            aw += self._width - mw
            ah += self._height - mh
            unit_w, unit_h = aw / sum(wrs), ah / sum(hrs)
            for ax in self._axes.values():
                r,c = ax._get_row(), ax._get_col()
                nr, nc = next(((d["nr"], d["nc"]) for d in self._mosaic.values() if d["ax"] == ax), (1, 1))
                if nr > 1 or nc > 1:
                    rows = [r - i for i in range(nr)]
                    cols = [c + i for i in range(nc)]
                    w = unit_w * sum([wrs[c] for c in cols]) + max(col_spacing) * (nc - 1)
                    h = unit_h * sum([hrs[r] for r in rows]) + max(row_spacing) * (nr - 1)
                    ax._update_size(w, h)
                    ax._update_placeholder_size(unit_w * wrs[c], unit_h * hrs[r])
                else:
                    ax._update_size(unit_w * wrs[c], unit_h * hrs[r])
        self._spacings = row_spacing, col_spacing

    def _get_prim_size(self, ax):
        r,c = ax._get_row(), ax._get_col()
        nr, nc = next(((d["nr"], d["nc"]) for d in self._mosaic.values() if d["ax"] == ax), (1, 1))
        def default():
            if self._wratios is not None:
                w = self._width * self._wratios[c] / sum(self._wratios)
            else:
                w = self._width / self._ncols
            if self._hratios is not None:
                h = self._height * self._hratios[r] / sum(self._hratios)
            else:
                h = self._height / self._nrows
            return w, h
        if nr > 1 or nc > 1:
            rows = [r - i for i in range(nr)]
            cols = [c + i for i in range(nc)]
            w = 0
            if self._wratios is not None:
                w = self._width * sum([self._wratios[c] for c in cols]) / sum(self._wratios)
            else:
                w = self._width * nc / self._ncols
            h = 0
            if self._hratios is not None:
                h = self._height * sum([self._hratios[r] for r in rows]) / sum(self._hratios)
            else:
                h = self._height * nr / self._nrows
            ax._update_placeholder_size(*default())
            return w, h
        return default()


    def _get_spacing(self, row, col):
        if not self._spacings:
            self._compute_group_spacing()
        assert self._spacings is not None
        if col == 0:
            if row == 0:
                return 0
            return self._spacings[0][row-1]
        return self._spacings[1][col-1]
    
    def _charcode(self, n):
        result = []
        while n > 0:
            n -= 1
            n, r = divmod(n, 26)
            result.append(chr(ord('a') + r))
        return ''.join(reversed(result))
    
    def _next_limname(self, which, value):
        d2 = {v: k for k, v in self._lims[which].items()}
        if value in d2.keys():
            return d2[value]
        dct = self._lims[which]
        n = len(dct)+1
        nm = "\\" + which + self._charcode(n)
        self._lims[which][nm] = value
        return nm
    
    def _get_limname(self, which, name):
        return self._lims[which].get(name)
    
    def _range_setting(self, min_val, max_val, mode):
        if min_val is not None and max_val is not None and min_val < max_val:
            if mode == "lin":
                d = max_val - min_val
                min_val -= d * TikzConfig.SHARED_AXIS_REL_MARGIN
                max_val += d * TikzConfig.SHARED_AXIS_REL_MARGIN
        
            else:
                d = (max_val / min_val) ** TikzConfig.SHARED_AXIS_REL_MARGIN
                min_val /= d
                max_val *= d

            return min_val, max_val
        return None, None
    
    def _shared_ranges(self):
        shared_x = []
        shared_y = []
        if self._sharex and self._sharex != "none":
            if self._sharex == "all" or self._sharex == True:
                shared_x = [self._axes.values()]
            if self._sharex == "row":
                shared_x = [[] for _ in range(self._nrows)]
                for ax in self._axes.values():
                    shared_x[ax._get_row()].append(ax)
            elif self._sharex == "col":
                shared_x = [[] for _ in range(self._ncols)]
                for ax in self._axes.values():
                    shared_x[ax._get_col()].append(ax)
        if self._sharey and self._sharey != "none":
            if self._sharey == "all" or self._sharey == True:
                shared_y = [self._axes.values()]
            if self._sharey == "row":
                shared_y = [[] for _ in range(self._nrows)]
                for ax in self._axes.values():
                    shared_y[ax._get_row()].append(ax)
            elif self._sharey == "col":
                shared_y = [[] for _ in range(self._ncols)]
                for ax in self._axes.values():
                    shared_y[ax._get_col()].append(ax)
        shared_x += self._xshare
        shared_y += self._yshare

        def merger(groups):
            sets = [set(g) for g in groups]
            merged = True
            while merged:
                merged = False
                new_sets = []
                while sets:
                    s = sets.pop()
                    i = 0
                    while i < len(sets):
                        if s & sets[i]:
                            s |= sets.pop(i)
                            merged = True
                        else:
                            i += 1
                    new_sets.append(s)
                sets = new_sets
            return [list(s) for s in sets]
        shared_x = merger(shared_x)
        shared_y = merger(shared_y)

        def set_ax_ranges(which, group):        
            hard_min_vals = []
            hard_max_vals = []
            mode = "lin"
            for ax in group:
                hmin, m = ax._get_hard_range(which + "min")
                if m == "log":
                    mode = "log"
                if hmin is not None:
                    hard_min_vals.append(hmin)
        
                hmax, m = ax._get_hard_range(which + "max")
                if m == "log":
                    mode = "log"
                if hmax is not None:
                    hard_max_vals.append(hmax)
        
            if hard_min_vals or hard_max_vals:
                min_val = min(hard_min_vals) if hard_min_vals else None
                max_val = max(hard_max_vals) if hard_max_vals else None
        
                if min_val is not None:
                    for ax in group:
                        ax._set_range(which + "min", min_val)
        
                if max_val is not None:
                    for ax in group:
                        ax._set_range(which + "max", max_val)
                
            mins = [ax._get_range(which + "min") for ax in group]
            maxes = [ax._get_range(which + "max") for ax in group]
        
            min_val = min(r[0] for r in mins)
            max_val = max(r[0] for r in maxes)
            mode = "log" if "log" in [r[2] for r in mins] else "lin"
            min_val, max_val = self._range_setting(min_val, max_val, mode)
            for ax in group:
                if hard_min_vals == []:
                    ax._set_range(which + "min", min_val)
                if hard_max_vals == []:
                    ax._set_range(which + "max", max_val)        
        
        for group in shared_x:
            set_ax_ranges("x", group)
        
        for group in shared_y:
            set_ax_ranges("y", group)

    def _add_spy(self, zoom, size, **kwargs):
        sp_str = f"\\spy [size={size}cm, magnification={zoom}"
        bck = ""
        n = len(self._spies)
        if "shape" in kwargs and kwargs["shape"] == "circle":
            sp_str += ", circle"
            bck = f"\\fill[white] (spyviewr{n}) circle ({size/2}cm);\n"
        else:
            bck = f"\\fill[white] ($(spyviewr{n}) + (-{size/2}cm,-{size/2}cm)$) rectangle ($(spyviewr{n}) + ({size/2}cm,{size/2}cm)$);\n"
        if "connect" in kwargs and kwargs["connect"]:
            sp_str += ", connect spies"
        sp_str += f"] on (spypoint{n}) in node at (spyviewr{n});"
        self._spies.append(bck + sp_str)
        return n

    def _add_external(self, content):
        self._external.append(content)
    
    def _reduce_points(self):
        counts = [0]
        for ax in self._axes.values():
            counts += ax._num_points()
        counts = [min(c, TikzConfig.MAX_POINTS_PER_ELEMENT) for c in counts]
        limit = max(counts)
        if sum(counts) > TikzConfig.MAX_POINTS_PER_FIGURE:
            lo, hi = 0, max(counts)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                total = sum(min(c, mid) for c in counts)
                if total <= TikzConfig.MAX_POINTS_PER_FIGURE:
                    lo = mid
                else:
                    hi = mid - 1
            limit = lo

        for ax in self._axes.values():
            ax._reduce_points(limit)

    def _to_tex(self, filename, png=False, standalone=None, print_requirements=False):
        single = self._nrows * self._ncols == 1
        if not self._axes:
            return ""
        self._shared_ranges()
        if TikzConfig.REDUCE_NUM_POINTS:
            self._reduce_points()
        lines0 = [g for g in self._globals]
        lines = []
        lines2 = []
        if self._spies:
            lines0.append("\\begin{tikzpicture}[spy using outlines={}]")
        else:
            lines0.append("\\begin{tikzpicture}")
        nrows = self._nrows
        ncols = self._ncols
        for i in range(1, 1 + nrows * ncols):
            if i not in self._axes:
                self._axes[i] = Axes(nrows, ncols, -i, self, False)
        if TikzConfig.USE_GROUPPLOTS and not single:
            if TikzConfig.SIMULATE_SIZES:
                if _can_compile_tex():
                    self_copy = copy.deepcopy(self)
                    for ax in self_copy._axes.values():
                        ax._hidable = False
                        #ax._elements = {0: []}
                    self._compute_group_spacing(self_copy)
                else:
                    print("TikzConfig.SIMULATE_SIZES is enabled, but local pdflatex compiling is not available. Groupplot spacings will not use simulation, which might produce unsatisfactory results.")
                    self._compute_group_spacing()
            else:
                self._compute_group_spacing()
            assert self._spacings is not None
            q = f"\\begin{{groupplot}}[group style={{group size={ncols} by {nrows}"
            if len(self._spacings[0]) > 0 and len(self._spacings[1]) > 0:
                q += f", horizontal sep={max(self._spacings[1])}cm, vertical sep={max(self._spacings[0])}cm"
            q += f"}}"
            if TikzConfig.SCALE_ONLY_AXIS:
                q += ", scale only axis"
            lines.append(q + "]")
        for i in range(nrows * ncols):
            ax = self._axes[i + 1]
            prim, sec = ax._to_tex(filename, single)
            lines += prim
            if sec:
                lines2 += sec
        if TikzConfig.USE_GROUPPLOTS and not single:
            lines.append("\\end{groupplot}")
        lines += lines2
        for spy in self._spies:
            lines.append(spy)
        for text in self._texts:
            lines.append(text._to_tex_fin())
        for ext in self._external:
            lines.append(ext._to_tex())
        lines.append("\\end{tikzpicture}")
        for c in self._col_dict:
            r,g,b=self._col_dict[c]
            lines0.insert(1,f"\\definecolor{{{c}}}{{rgb}}{{{r:.3f}, {g:.3f}, {b:.3f}}}")
        preambule = ""
        stdalone = TikzConfig.STANDALONE if standalone is None else standalone
        if stdalone:
            if png:
                preambule += "\\documentclass[tikz,border=2pt,convert={density=300,outext=.png}]{standalone}\n"
            else:
                preambule += "\\documentclass[tikz,border=2pt]{standalone}\n"
            self._check_required_packages()
            preambule += "\n".join(self._required_packages.keys()) + "\n"
            preambule += "\\begin{document}\n"
        if print_requirements and not stdalone:
            self._check_required_packages()
            print("Required packages:")
            for p in self._required_packages.keys():
                print(p)
        fin = ""
        if stdalone:
            fin += "\\end{document}"
        for k in self._lims.keys():
            for j in self._lims[k]:
                lines0.append(f"\\def{j}{{{self._lims[k][j]}}}")
        lines = lines0 + lines
        output = preambule + "\n" + "\n".join(lines) + "\n" + fin
        return output

    def _add_indents(self, content):
        lines = content.split("\n")
        depth = 0
        mathmode = False
        output = []
        for line in lines:
            if len(line.strip()) == 0 or line.strip() == ",":
                continue
            if line.strip().startswith("\\end{") and depth > 0:
                depth -= 1
            output.append("\t" * depth + line)
            if line.strip().startswith("\\begin{"):
                depth += 1
            for c in line.strip():
                if c == "$":
                    mathmode = not mathmode
                if not mathmode:
                    if c == "{" or c == "[":
                        depth += 1
                    elif c == "}" or c == "]" and depth > 0:
                        depth -= 1
        return "\n".join(output)
            

    def _save(self, filename, standalone=None, print_requirements=False):
        content = self._to_tex(filename, png=False, standalone=standalone, print_requirements=print_requirements)
        if not TikzConfig.SAVE_DATAPOINTS or (TikzConfig.SAVE_DATAPOINTS and not TikzConfig.UPDATE_DATA_ONLY):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self._add_indents(content))

    def _save_image(self, filename):
        content = self._to_tex(filename, png=True)
        if not TikzConfig.SAVE_DATAPOINTS or (TikzConfig.SAVE_DATAPOINTS and not TikzConfig.UPDATE_DATA_ONLY):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self._add_indents(content))

    def _get_width(self):
        return self._width
    
    def _get_height(self):
        return self._height
    
    def clear(self):
        self.__init__(style=self._style)

    def _get_free_path_name(self):
        self._last_path_num += 1
        return f"path{self._last_path_num}"
    
    def _add_col(self, r,g,b):
        code = f"c{r:.3f}{g:.3f}{b:.3f}".replace(".", "")
        self._col_dict[code] = (r,g,b)

    def _add_global(self, setting):
        self._globals.add(setting)

    def _next_coordinate_name(self):
        self._num_coordinates += 1
        return f"(coordinate{self._num_coordinates})"
    
    def _add_text(self, text):
        self._texts.append(text)

    def tight_layout(self, h_pad=0, w_pad=0, rect=(0,0,1,1)):
        TikzConfig.SCALE_ONLY_AXIS = True
        if not TikzConfig.USE_GROUPPLOTS:
            print("Tight layout is only available when using groupplots (TikzConfig.USE_GROUPPLOTS). Command will be ignored.")
        elif _can_compile_tex():
            TikzConfig.SIMULATE_SIZES = True
            for q in rect:
                if not (0 <= q <= 1):
                    raise ValueError("rect values must be in the range [0, 1]")
            tight_params = {"h_pad": h_pad, "w_pad": w_pad, "rect": rect}
            self._tight_params |= tight_params
        else:
            print("Tight layout requires local pdflatex compiling, which is not available. Command will be ignored.")
        

    def _add_required_package(self, package):
        if package not in self._required_packages:
            if package.startswith("\\usepackage"):
                self._required_packages[package] = 2
            elif package.startswith("\\pgfplotsset"):
                self._required_packages[package] = 3
            elif package.startswith("\\usetikzlibrary"):
                self._required_packages[package] = 4
            elif package.startswith("\\usepgfplotslibrary"):
                self._required_packages[package] = 5
            else:
                self._required_packages[package] = 6

    def _check_required_packages(self):
        single = self._nrows * self._ncols == 1
        self._required_packages["\\usepackage{tikz}"] = 0
        self._required_packages["\\usepackage{pgfplots}"] = 1
        if TikzConfig.USE_GROUPPLOTS and not single:
            self._required_packages["\\usepgfplotslibrary{groupplots}"] = 5
        self._required_packages[f"\\pgfplotsset{{compat={TikzConfig.TIKZ_COMPAT}}}"] = 3
        if TikzConfig.USE_XCOLOR:
            self._required_packages["\\usepackage{xcolor}"] = 2
        if self._spies:
            self._required_packages["\\usetikzlibrary{spy}"] = 4
        self._required_packages = dict(sorted(self._required_packages.items(), key=lambda item: item[1]))
