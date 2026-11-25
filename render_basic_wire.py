"""Build OOBB basic wire holder illustrations."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

from render_parts import font

ROOT = Path(__file__).resolve().parent
PART_ID = "oobb_part_electronic_wire_basic_plate_3_width_3_height_4_depth"
VIEWS = {
    "plate": ("Basic wire holder · bare plate", "3 × 3 OOBB footprint  /  4 mm plate",
              [("key", "Key-side notch"), ("pocket", "Header seat"), ("rear", "Rear wire opening")]),
    "assembled": ("Basic wire holder · assembled", "Three contacts in a keyed 2.54 mm connector",
                  [("header", "Keyed header"), ("housing", "3-way socket housing"), ("wires", "Wires through base")]),
    "exploded": ("Basic wire holder · exploded", "Feed the wires up, crimp the sockets, then seat the linked header and housing.",
                 [("header", "Keyed header"), ("housing", "3-way housing"), ("crimp", "3 crimp sockets"),
                  ("rear", "Rear wire opening")]),
    "stock": ("2.54 mm long equal-pin header", "6 positions  /  6.25 mm each end  /  15 mm overall", []),
    "keyed": ("OOBB basic keyed header", "6 positions  /  remove 1, 2 and 6  /  key side at left", []),
}
OFFSETS = {"key": (-75, 55), "pocket": (-90, -70), "rear": (80, 38),
           "cap": (80, -40), "header": (-96, 45), "housing": (100, -48), "crimp": (95, -18), "wires": (95, 35)}


def sheet(view, scratch, destination, specification=None):
    title, subtitle, labels = specification or VIEWS[view]
    paper, ink, muted, teal = "#f6f4ef", "#243a3b", "#4f6160", "#276d70"
    canvas = Image.new("RGB", (1600, 1080), paper)
    with Image.open(scratch / f"{view}.png") as source:
        frame = source.convert("RGBA")
    x0, y0 = 80, 137
    canvas.paste(frame, (x0, y0), frame)
    draw = ImageDraw.Draw(canvas)
    draw.text((56, 33), title, font=font(48), fill=ink)
    draw.text((58, 94), subtitle, font=font(27), fill=muted)
    points = json.loads((scratch / f"{view}.json").read_text(encoding="utf-8"))
    for n, (name, label) in enumerate(labels, 1):
        u, v = points[name]
        x, y = x0 + frame.width * u, y0 + frame.height * (1-v)
        dx, dy = OFFSETS[name]
        a, b = x + dx, y + dy
        draw.line((x, y, a, b), fill=teal, width=2)
        draw.ellipse((x-4, y-4, x+4, y+4), fill=teal, outline=paper, width=1)
        draw.ellipse((a-16, b-16, a+16, b+16), fill=paper, outline=teal, width=2)
        draw.text((a, b), str(n), anchor="mm", font=font(22), fill=ink)
        legend_x = 58 + (n-1) * 380
        draw.text((legend_x, 966), f"{n}  {label}", font=font(26), fill=ink)
    draw.line((58, 1014, 1542, 1014), fill="#bdc7bf", width=2)
    draw.text((58, 1031), "AI-generated CAD illustration. Errors possible.", font=font(22), fill=muted)
    palette = {"plate": "Teal: printed PLA", "stock": "Black: insulator  /  Gold: contacts",
               "keyed": "Black: insulator  /  Gold: contacts"}.get(view, "Teal: printed PLA  /  Black: connector")
    draw.text((1542, 1031), palette, anchor="ra", font=font(22), fill=muted)
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, optimize=True)


def main(oomp_root, blender=None, reuse=False):
    import os
    os.environ["OOMP_ELECTRONIC_ROOT"] = str(oomp_root)
    if blender:
        os.environ["BLENDER_EXE"] = blender
    from render_wire_catalogue import main as render
    render(reuse=reuse, part_filter=PART_ID, include_headers=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--oomp-root", type=Path, default=ROOT.parent / "oomp_electronic_version_5")
    parser.add_argument("--blender")
    parser.add_argument("--reuse", action="store_true", help="Redo captions using the last raw images")
    args = parser.parse_args()
    main(args.oomp_root.resolve(), args.blender, args.reuse)
