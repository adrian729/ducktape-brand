from copy import deepcopy
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


def mark(small: bool = False, mono: bool = False) -> ET.Element:
    source = ET.parse(ROOT / "source/mark.svg").getroot()
    group = deepcopy(source.find(tag("g")))
    if small:
        for child in list(group):
            if child.get("id") in {"side", "ring-outer", "ring-inner", "nostril"}:
                group.remove(child)
    if mono:
        for element in group.iter():
            if element.get("fill") in {"#b9babd", "#83878b", "#bfc1c4", "#f6c82c"}:
                element.set("fill", "#ffffff")
            if element.get("stroke") == "#a0a4a8":
                element.set("stroke", "#1b1d20")
    return group


FONT = TTFont(ROOT / "source/fonts/LiberationSans-Bold.ttf")
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UNITS = FONT["head"].unitsPerEm


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


def icon_svg(small: bool = False, mono: bool = False, square: bool = False) -> ET.Element:
    root = canvas("0 0 520 520" if square else "0 0 520 400", "Duck in a roll of duct tape")
    holder = ET.SubElement(root, tag("g"), {"transform": "translate(0 60)"}) if square else root
    holder.append(mark(small=small, mono=mono))
    return root


def lockup_svg(product: str | None, dark: bool) -> ET.Element:
    label = "ducktape" if product is None else f"ducktape {product.lower()}"
    root = canvas("0 0 940 290", label)
    holder = ET.SubElement(root, tag("g"), {"transform": "scale(0.72)"})
    holder.append(mark())
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
    color = icon_svg()
    small = icon_svg(small=True)
    mono = icon_svg(mono=True)
    save_svg(assets / "mark-color.svg", color)
    save_svg(assets / "mark-small.svg", small)
    save_svg(assets / "mark-mono.svg", mono)
    save_svg(assets / "favicon.svg", icon_svg(small=True, square=True))
    for size in (1024, 512, 256, 128, 64, 32):
        png(icon_svg(small=size <= 64, square=True), exports / f"mark-{size}.png", size, size)
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
