import subprocess
import tempfile
import re
import os
import shutil

from .config import TikzConfig

def _get_sizes(pgf_code: str, preambule: str, alias:str|None) -> tuple[float, float, float, float, float, float]:
    if alias is None:
        alias = "myplot"
    c = pgf_code.split("[")
    c[1] = f"name={alias}," + c[1]
    if TikzConfig.SCALE_ONLY_AXIS:
        c[1] = "scale only axis," +c[1]
    pgf_code = "[".join(c)
    latex_document = r"\documentclass[border=0pt]{standalone}" + "\n" + preambule + r"""
    \begin{document}
    \begin{tikzpicture}

    """ + pgf_code + r"""

    \path (""" + alias + r""".south west); \pgfgetlastxy{\axXSW}{\axYSW}
    \path (""" + alias + r""".north east); \pgfgetlastxy{\axXNE}{\axYNE}

    \path (current bounding box.south west); \pgfgetlastxy{\figXSW}{\figYSW}
    \path (current bounding box.north east); \pgfgetlastxy{\figXNE}{\figYNE}

    \typeout{RAW_DATA:\figXSW,\figYSW,\figXNE,\figYNE,\axXSW,\axYSW,\axXNE,\axYNE}

    \end{tikzpicture}
    \end{document}
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, "layout.tex")
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_document)
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "layout.tex"],
            cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        clean_stdout = proc.stdout.replace("\n", "").replace("\r", "")

        match = re.search(
            r"RAW_DATA:([\d.-]+)pt,([\d.-]+)pt,([\d.-]+)pt,([\d.-]+)pt,([\d.-]+)pt,([\d.-]+)pt,([\d.-]+)pt,([\d.-]+)pt",
            clean_stdout
        )
        if not match:
            log_path = os.path.join(tmpdir, "layout.log")
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8", errors="ignore") as log_file:
                    print("--- LaTeX Log Output ---")
                    print(log_file.read()[-1200:])
            raise RuntimeError("Failed to extract dimensions from LaTeX log.")

        fx0, fy0, fx1, fy1, ax0, ay0, ax1, ay1 = map(float, match.groups())

    pt_to_cm = 2.54 / 72.27

    left_padding   = (ax0 - fx0) * pt_to_cm
    axis_width     = (ax1 - ax0) * pt_to_cm
    right_padding  = (fx1 - ax1) * pt_to_cm

    bottom_padding = (ay0 - fy0) * pt_to_cm
    axis_height    = (ay1 - ay0) * pt_to_cm
    top_padding    = (fy1 - ay1) * pt_to_cm

    return left_padding, right_padding, top_padding, bottom_padding, axis_width, axis_height

def _can_compile_tex(compiler="pdflatex") -> bool:
    if not shutil.which(compiler):
        return False

    minimal_tex = r"\documentclass{article}\begin{document}\end{document}"

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, "test.tex")
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(minimal_tex)

            # Run compiler in nonstop mode to prevent waiting for user input on errors
            result = subprocess.run(
                [compiler, "-interaction=nonstopmode", "test.tex"],
                cwd=tmpdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,  # Safety timeout in seconds
            )
            return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError, Exception):
        return False