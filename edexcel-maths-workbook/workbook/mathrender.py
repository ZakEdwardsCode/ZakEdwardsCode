"""Turn rich text ("words and $maths$") into reportlab flowables.

Maths is typeset with matplotlib's mathtext (pure Python, no LaTeX install
needed) and embedded as high-resolution inline images that sit on the
text baseline.
"""
from __future__ import annotations

import hashlib
import re
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import MathTextParser
from PIL import Image
from reportlab.platypus import Paragraph

matplotlib.rcParams["mathtext.fontset"] = "stix"
DPI = 400
_PARSER = MathTextParser("agg")
_CACHE: dict[tuple, tuple] = {}
_DIR = Path(tempfile.mkdtemp(prefix="wb-math-"))
_TOKEN = re.compile(r"(\$\$.+?\$\$|\$.+?\$)", re.S)


def math_image(tex: str, size: float = 10.5):
    """Render $tex$ to a PNG. Returns (path, width_pt, height_pt, depth_pt)."""
    key = (tex, size)
    if key in _CACHE:
        return _CACHE[key]
    r = _PARSER.parse(f"${tex}$", dpi=DPI, prop=FontProperties(size=size))
    img = r.image
    arr = img if hasattr(img, "shape") else img.as_array()
    alpha = arr.astype("uint8")
    rgba = Image.new("RGBA", (alpha.shape[1], alpha.shape[0]), (0, 0, 0, 0))
    rgba.putalpha(Image.fromarray(alpha, mode="L"))
    name = hashlib.md5(f"{tex}|{size}".encode()).hexdigest() + ".png"
    path = _DIR / name
    rgba.save(path)
    k = 72 / DPI
    out = (str(path), alpha.shape[1] * k, alpha.shape[0] * k, r.depth * k)
    _CACHE[key] = out
    return out


def markup(text: str, size: float = 10.5) -> str:
    """Convert rich text into reportlab paragraph markup with inline images."""
    out = []
    for tok in _TOKEN.split(text):
        if not tok:
            continue
        if tok.startswith("$$"):
            p, w, h, d = math_image(tok[2:-2], size * 1.15)
            out.append(f'<br/><img src="{p}" width="{w:.2f}" height="{h:.2f}" valign="{-d:.2f}"/><br/>')
        elif tok.startswith("$"):
            p, w, h, d = math_image(tok[1:-1], size)
            out.append(f'<img src="{p}" width="{w:.2f}" height="{h:.2f}" valign="{-d:.2f}"/>')
        else:
            s = escape(tok).replace("\n", "<br/>")
            s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
            out.append(s)
    return "".join(out)


def rich(text: str, style, size: float | None = None) -> Paragraph:
    return Paragraph(markup(text, size or style.fontSize), style)
