"""Render every header-based wire holder and the reusable OOMP header library.

Run the OOMP header_oobb_3d generator first. --reuse rebuilds captions and docs.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw
import yaml

from render_basic_wire import sheet
from render_parts import find_blender, sha, write_json, font

ROOT = Path(__file__).resolve().parent
OOMP = Path(os.environ.get("OOMP_ELECTRONIC_ROOT", ROOT.parent / "oomp_electronic_version_5")).resolve()
sys.path.insert(0, str(OOMP))
from kicad_agents.header_oobb_3d import (VARIANTS, CONTACT_ID, long_id as stock_id, variant_id,
                                      housing_id, read_step, write_stl, LONG_PRODUCT_URL, LONG_DATASHEET_URL, LONG_MPN)


def hardware_link(identity):
    if not (OOMP / "parts" / identity / "working.yaml").exists():
        raise ValueError(f"Missing hardware record: {identity}")
    return "https://github.com/oomlout/oomp_electronic_version_5/tree/main/parts/" + identity


def prepare(part, detail, scratch):
    rows = detail.get("multiple", 0) if detail.get("wire_style") == "triple_pin_header" else 0
    kind = f"vertical_{rows}_row" if rows else detail["wire_type"]
    v = VARIANTS[kind]
    contacts = 3 if rows else v["contacts"]
    label = f"Triple header · {rows} rows" if rows else f"{kind.replace('_', ' ').title()} wire holder"
    scratch.mkdir(parents=True, exist_ok=True)
    assets = {"housing": housing_id(contacts), "contact": CONTACT_ID}
    for key, identity in assets.items():
        target = scratch / f"{key}.stl"
        write_stl(read_step(OOMP / "parts" / identity / "data/model_3d.step"), target)
    job = dict(scratch=str(scratch), plate=str(part / "3dpr.stl"),
               header=str(OOMP / "parts" / variant_id(kind) / "data"),
               housing=str(scratch / "housing.stl"), contact=str(scratch / "contact.stl"),
               views=["plate", "assembled", "exploded", "keyed", "seating"], variant=v, rows=rows, depth=detail["depth"])
    if rows:
        import trimesh
        mesh = trimesh.load_mesh(part / "3dpr.stl")
        groups = mesh.split(only_watertight=False)
        base = [m for m in groups if m.bounds[1][0] < 25]
        cap = [m for m in groups if m.bounds[0][0] > 25]
        if len(base) != 1 or len(cap) != 1 or len(groups) != 2:
            raise ValueError(f"Expected a base and included top retainer: {part.name}")
        base[0].export(scratch / "base.stl")
        cap[0].apply_translation([-50, 0, 0])
        cap[0].export(scratch / "cap.stl")
        job.update(plate=str(scratch / "base.stl"), cap=str(scratch / "cap.stl"))
    specs = {
        "plate": (f"{label} · printed parts", f"3 × 3 OOBB  /  {detail['depth']:g} mm base" + ("  /  included 2.54 mm top retainer" if rows else ""),
                  [("pocket", "Header seat"), ("rear", "Rear wire opening")] + ([("cap", "Top retainer")] if rows else [])),
        "assembled": (f"{label} · assembled", f"{contacts * (rows or 1)} contacts  /  2.54 mm pitch",
                      [("header", "Retained end cells" if rows else "Prepared header"), (("cap", "Top retainer") if rows else ("housing", f"{contacts}-way housing")), ("wires", "Wires through base")]),
        "exploded": (f"{label} · exploded", "Feed wires through the base, crimp sockets, insert into housings, then fit headers.",
                     [("header", "3 vertical strips" if rows else "Prepared header"), ("housing", f"{rows} socket housings" if rows else f"{contacts}-way housing"),
                      ("crimp", f"{contacts*(rows or 1)} crimp sockets")] + ([("cap", "Top retainer")] if rows else [("rear", "Rear wire opening")])),
    }
    removed = ", ".join(map(str, v["removed"]))
    specs["keyed"] = (f"{label} · prepare the header",
                      f"{'Three strips' if rows else 'One strip'}  /  {v['count']} positions per strip  /  remove pins {removed}", [])
    specs["seating"] = (f"{label} · seat the connector",
                        "Locate the empty bottom cells in the base before fitting the top retainer." if rows else
                        "Lower the mated housing and header together into the printed seat.",
                        [("header", "Prepared header"), ("housing", "Socket housing")])
    stock, header = stock_id(v["count"]), variant_id(kind)
    quantity = 3 if rows else 1
    hardware = [dict(id=stock, name=f"{v['count']}-position header_long section (equal ends)", quantity=quantity),
                dict(id=header, name="Prepared vertical strip" if rows else "Prepared OOBB header", quantity=quantity, state="after modification"),
                dict(id=assets["housing"], name=f"{contacts}-way socket housing", quantity=rows or 1),
                dict(id=CONTACT_ID, name="Female crimp socket, 22–30 AWG", quantity=contacts*(rows or 1))]
    for item in hardware:
        item["url"] = hardware_link(item["id"])
    if rows:
        first = f"Cut three {v['count']}-position sections of header_long (6.25 mm exposed at both ends). Push out pins {removed} from each strip; keep both end cells intact. Stand the strips vertically, counting from the bottom."
        fit = "Place the three vertical strips into the bottom beam window, with one set of pin ends facing the keyed front opening. Mate one three-way housing with each active row."
        last = "Fit the included top retainer over the three empty top cells. It is printed beside the base in the same part file. Keep the rear wire opening clear."
    else:
        first = f"Cut one {v['count']}-position section of header_long (6.25 mm exposed at both ends). Count from the key side (negative X in the model) and push out pins {removed}; keep the full plastic strip."
        if kind in ("motor", "motor_stepper"):
            first = f"Cut one {v['count']}-position header_long section, with equal 6.25 mm ends, and push out the two end pins ({removed}); keep the full plastic strip."
        fit = "Mate the housing with the rear 6.25 mm pin ends, then lower the header and housing into their seats. The equal front ends face the front opening."
        last = "Check that the wires move freely through the rear opening and the contacts remain recessed inside the front edge."
    steps = [first, f"Pass {contacts*(rows or 1)} wires up through the rear opening before crimping. Crimp one socket per wire and insert the sockets into the backs of the housings until latched.", fit, last]
    description = (f"A {rows}-row, three-contact-wide connector using three vertical header_long strips with equal pin ends and an included top retainer. "
                   f"The base is 2.54 mm plus {rows} × 2.54 mm; the top adds 2.54 mm when fitted." if rows else
                   f"A printed {kind.replace('_', ' ')} wire holder converts a {v['count']}-position header_long with equal pin ends into a {contacts}-contact connector. Empty plastic cells locate the header in the plate.")
    manifest = dict(part_id=part.name, description=description, hardware=hardware, steps=steps,
                    step_views=["keyed", "exploded", "seating", "assembled"],
                    header_reference=dict(mpn=LONG_MPN, lcsc="C343639", product_url=LONG_PRODUCT_URL, datasheet_url=LONG_DATASHEET_URL),
                    wire_count=contacts*(rows or 1), removed_pin_positions=list(v["removed"]),
                    note="The stock and prepared header rows describe the same item before and after modification. Use 15 mm overall header_long stock (6.25 mm exposed on each side of a 2.5 mm insulator); LCSC C343639 is a 40-position strip cut to the required lengths. Wire colours identify conductors, not a pinout. Housing and uncrimped socket geometry use nominal Harwin M20 references; wire bends are illustrative.",
                    images={view: f"basic_wire_{view}.png" for view in specs},
                    source_sha256={"production_stl": sha(part / "3dpr.stl"), "header_step": sha(Path(job["header"]) / "model_3d.step"),
                                   **{k: sha(OOMP / "parts" / i / "data/model_3d.step") for k, i in assets.items()}})
    return job, specs, manifest


def header_jobs(scratch):
    result = []
    entries = [(stock_id(n), n, (), False, f"Long equal-pin header · {n} positions") for n in range(1, 41)]
    entries += [(variant_id(k), v["count"], v["removed"], v.get("vertical", False),
                 f"OOBB {k.replace('_', ' ')} header") for k, v in VARIANTS.items()]
    for identity, count, removed, vertical, title in entries:
        folder = scratch / identity
        folder.mkdir(parents=True, exist_ok=True)
        data = OOMP / "parts" / identity / "data"
        job = dict(scratch=str(folder), stock=str(data), views=["stock"])
        subtitle = f"6.25 mm each end  /  15 mm overall  /  {count-len(removed)} contacts"
        if removed:
            subtitle += "  /  remove pins " + ", ".join(map(str, removed))
        if vertical:
            subtitle += "  /  count bottom to top"
        result.append((job, (title, subtitle, []), identity))
        if vertical:
            arrangement = scratch / (identity + "_3_strip")
            arrangement.mkdir(parents=True, exist_ok=True)
            result.append((dict(job, scratch=str(arrangement), mesh_prefix="model_3d_3_strip", output_name="model_3d_arrangement.png"),
                           (f"Vertical header set · {count-2} rows", f"Three {count}-position long strips  /  {3*(count-2)} contacts  /  equal pin ends", []), identity))
    identity = housing_id(2)
    folder = scratch / identity
    folder.mkdir(parents=True, exist_ok=True)
    write_stl(read_step(OOMP / "parts" / identity / "data/model_3d.step"), folder / "housing.stl")
    result.append((dict(scratch=str(folder), single=str(folder / "housing.stl"), views=["stock"]),
                   ("Two-way socket housing", "Harwin M20-1060200  /  2.54 mm pitch  /  nominal reference geometry", []), identity))
    return result


def contact_sheet(assemblies):
    """Keep the overview tied to the current published assembly images."""
    items = sorted(assemblies, key=lambda a: ("triple_pin_header" in a["part_id"], a["wire_count"], a["part_id"]))
    height = 170 + 300*((len(items)+3)//4)
    canvas = Image.new("RGB", (1600, height), "#f6f4ef")
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 16), "OOBB wire connectors · equal-ended headers", font=font(34), fill="#243a3b")
    for i, assembly in enumerate(items):
        x, y = (i%4)*400, 80+(i//4)*300
        with Image.open(ROOT / "parts" / assembly["part_id"] / assembly["images"]["exploded"]) as source:
            frame = source.crop((80, 137, 1520, 949))
            frame.thumbnail((390, 260))
            canvas.paste(frame, (x, y+30))
        name = assembly["part_id"].split("wire_")[1].split("_plate")[0].replace("_", " ")
        if "triple_pin_header" in assembly["part_id"]:
            name = f"Triple header · {assembly['wire_count']//3} rows"
        draw.text((x+12, y), name, font=font(22), fill="#243a3b")
    draw.text((24, height-43), "AI-generated CAD illustrations. Errors possible.  /  Teal: printed PLA", font=font(22), fill="#4f6160")
    canvas.save(ROOT / "presentation/wire_catalogue_preview.png")


def main(reuse=False, part_filter="", include_headers=True):
    scratch = ROOT / "build/presentation/wire_catalogue"
    scratch.mkdir(parents=True, exist_ok=True)
    assemblies = []
    for part in sorted((ROOT / "parts").glob("*wire*")):
        if part_filter not in part.name:
            continue
        detail = yaml.safe_load((part / "working.yaml").read_text(encoding="utf-8")).get("oobb_details", {})
        if detail.get("oobb_name") != "wire" or detail.get("wire_type") not in VARIANTS or detail.get("wire_style") not in ("", "triple_pin_header", None):
            continue
        job, specs, manifest = prepare(part, detail, scratch / part.name)
        assemblies.append((part, job, specs, manifest))
    headers = header_jobs(scratch) if include_headers else []
    jobs = [a[1] for a in assemblies] + [h[0] for h in headers]
    write_json(scratch / "jobs.json", jobs)
    if not reuse:
        with (scratch / "blender.log").open("w", encoding="utf-8") as handle:
            subprocess.run([find_blender(None), "--background", "--python-exit-code", "1", "--python",
                            str(ROOT / "presentation/scripts/render_basic_wire_scene.py"), "--", str(scratch / "jobs.json")],
                           stdout=handle, stderr=subprocess.STDOUT, check=True)
    for part, job, specs, manifest in assemblies:
        for view, specification in specs.items():
            output = part / manifest["images"][view]
            sheet(view, Path(job["scratch"]), output, specification)
            with Image.open(output) as image:
                image.thumbnail((480, 480))
                image.save(part / f"basic_wire_{view}_thumb.png")
        write_json(part / "assembly.json", manifest)
        from wire_booklet import publish
        detail = yaml.safe_load((part / "working.yaml").read_text(encoding="utf-8"))["oobb_details"]
        publish(part, Path(job["scratch"]), manifest, detail, OOMP)
        if part.name == "oobb_part_electronic_wire_basic_plate_3_width_3_height_4_depth":
            write_json(ROOT / "presentation/basic_wire.json", manifest)
    for job, spec, identity in headers:
        destination = OOMP / "parts" / identity / "data" / job.get("output_name", "model_3d_render.png")
        sheet("stock", Path(job["scratch"]), destination, spec)
        shutil.copyfile(destination, OOMP / "parts_source" / identity / destination.name)
    if headers:
        from kicad_agents.wire_housing_3d import refresh_metadata
        refresh_metadata()
    manifest_path = ROOT / "presentation/wire_catalogue.json"
    previous = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    assembly_records = {a["part_id"]: a for a in previous.get("assemblies", [])} if part_filter else {}
    assembly_records.update({a[3]["part_id"]: a[3] for a in assemblies})
    write_json(manifest_path, dict(
        assemblies=list(assembly_records.values()),
        header_models=sorted({h[2] for h in headers}) if include_headers else previous.get("header_models", []),
        hardware_renders=[dict(id=h[2], file=h[0].get("output_name", "model_3d_render.png")) for h in headers]
        if include_headers else previous.get("hardware_renders", [])))
    contact_sheet(list(assembly_records.values()))
    print(f"Rendered {len(assemblies)} assemblies and {len(headers)} hardware models.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse", action="store_true")
    parser.add_argument("--filter", default="")
    parser.add_argument("--no-headers", action="store_true")
    args = parser.parse_args()
    main(args.reuse, args.filter, not args.no_headers)
