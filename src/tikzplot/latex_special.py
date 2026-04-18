import re

TEXT_MAP = str.maketrans({
    '%': r'\%',
    '$': r'\$',
    '&': r'\&',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}',
    '\\': r'\textbackslash{}',
})

MATH_MAP = str.maketrans({
    "%": r"\%",
    "#": r"\#",
    "&": r"\&",
})

def tex_text(sa: str) -> str:
    math_mode = False
    i = 0
    n = len(sa)
    out = []

    while i < n:
        s = sa[i]

        # Handle $$ (display math)
        if s == "$":
            if i + 1 < n and sa[i + 1] == "$":
                math_mode = not math_mode
                out.append("$$")
                i += 2
                continue
            else:
                math_mode = not math_mode
                out.append("$")
                i += 1
                continue

        # Skip already escaped characters (e.g. \%, \_)
        if s == "\\" and i + 1 < n:
            out.append(sa[i:i+2])
            i += 2
            continue

        if not math_mode:
            # Special handling for underscore in text mode
            if s == "_":
                out.append(r"\_")
            else:
                out.append(s.translate(TEXT_MAP))
        else:
            # Math mode: lighter escaping
            out.append(s.translate(MATH_MAP))

        i += 1

    return "".join(out)