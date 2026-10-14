"""Build ducktape exports from the mallard artwork."""

import base64
from pathlib import Path
from xml.etree import ElementTree as ET

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def tag(name: str) -> str:
    return f"{{{NS}}}{name}"


def save_svg(path: Path, root: ET.Element) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="  ")
    path.write_text(ET.tostring(root, encoding="unicode") + "\n")


def canvas(view_box: str, label: str) -> ET.Element:
    return ET.Element(tag("svg"), {"viewBox": view_box, "role": "img", "aria-label": label})


IMAGE_URI = "data:image/png;base64," + base64.b64encode((ROOT / "source/mark.png").read_bytes()).decode("ascii")
FONT = TTFont(ROOT / "source/fonts/LiberationSans-Bold.ttf")
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UNITS = FONT["head"].unitsPerEm


def add_mark(parent: ET.Element, x: float, y: float, width: float, height: float) -> None:
    # The inner viewBox trims transparent canvas without altering the artwork.
    frame = ET.SubElement(parent, tag("svg"), {
        "x": str(x), "y": str(y), "width": str(width), "height": str(height),
        "viewBox": "150 20 1220 940", "preserveAspectRatio": "xMidYMid meet",
    })
    ET.SubElement(frame, tag("image"), {
        "x": "0", "y": "0", "width": "1536", "height": "1024", "href": IMAGE_URI,
    })


def outlined_text(parent: ET.Element, value: str, x: float, baseline: float, size: float, color: str, spacing: float = 0) -> None:
    scale = size / UNITS
    group = ET.SubElement(parent, tag("g"), {"fill": color, "transform": f"translate({x} {baseline}) scale({scale:.8f} {-scale:.8f})"})
    cursor = 0
    for char in value:
        name = CMAP[ord(char)]
        pen = SVGPathPen(GLYPHS)
        GLYPHS[name].draw(pen)
        if path_data := pen.getCommands():
            ET.SubElement(group, tag("path"), {"d": path_data, "transform": f"translate({cursor:.2f} 0)"})
        cursor += FONT["hmtx"][name][0] + spacing / scale


def icon_svg(square: bool = False) -> ET.Element:
    root = canvas("0 0 1000 1000" if square else "0 0 1220 940", "Mallard in a roll of duct tape")
    if square:
        add_mark(root, 10, 115, 980, 755)
    else:
        add_mark(root, 0, 0, 1220, 940)
    return root


def lockup_svg(product: str | None, dark: bool) -> ET.Element:
    label = "ducktape" if product is None else f"ducktape {product.lower()}"
    root = canvas("0 0 940 290", label)
    add_mark(root, 0, 13, 342, 263)
    ink = "#f4f4f2" if dark else "#1b1d20"
    secondary = "#c8ccd0" if dark else "#565b62"
    outlined_text(root, "ducktape", 352, 151 if product else 181, 101, ink)
    if product:
        outlined_text(root, product, 359, 214, 28, secondary, spacing=5)
    return root


def png(svg: ET.Element, path: Path, width: int, height: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=ET.tostring(svg, encoding="utf-8"), write_to=str(path), output_width=width, output_height=height)


def main() -> None:
    assets = ROOT / "assets"
    exports = ROOT / "exports/png"
    save_svg(assets / "mark.svg", icon_svg())
    save_svg(assets / "favicon.svg", icon_svg(square=True))
    for size in (1024, 512, 256, 128, 64, 32):
        png(icon_svg(square=True), exports / f"mark-{size}.png", size, size)
    for mode in ("light", "dark"):
        generic = lockup_svg(None, mode == "dark")
        save_svg(assets / f"lockup-{mode}.svg", generic)
        png(generic, exports / f"lockup-{mode}-1200.png", 1200, 370)
        for repo, label in (
            ("ducktape-harness", "HARNESS"),
            ("ducktape-laya", "LAYA"),
            ("ducktape.nvim", "NVIM"),
            ("ducktape-provider", "PROVIDER"),
        ):
            save_svg(assets / "product" / f"{repo}-{mode}.svg", lockup_svg(label, mode == "dark"))


if __name__ == "__main__":
    main()
