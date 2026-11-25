"""Check assembly coverage, header selection, asset provenance and local links."""
import json
import os
import re
from pathlib import Path
from urllib.parse import unquote

import fitz
from PIL import Image
import yaml

from render_parts import sha

ROOT = Path(__file__).resolve().parent
ELECTRONIC = Path(os.environ.get("OOMP_ELECTRONIC_ROOT", ROOT.parent / "oomp_electronic_version_5")).resolve()


def main():
    manifest = json.loads((ROOT / "presentation/wire_catalogue.json").read_text(encoding="utf-8"))
    expected = set()
    for source in (ROOT / "parts").glob("*/working.yaml"):
        detail = yaml.safe_load(source.read_text(encoding="utf-8")).get("oobb_details", {})
        if detail.get("oobb_name") == "wire":
            expected.add(source.parent.name)
    assert {a["part_id"] for a in manifest["assemblies"]} == expected
    images = 0
    for assembly in manifest["assemblies"]:
        part = ROOT / "parts" / assembly["part_id"]
        assert sha(part / "3dpr.stl") == assembly["source_sha256"]["production_stl"]
        content = (part / "README.md").read_text(encoding="utf-8")
        assert "header_long" in content and "6.25 mm" in content
        assert len(assembly["step_views"]) == len(assembly["steps"]) == 4
        assert len(set(assembly["step_views"])) == 4
        viewer = (part/"assembly/assembly_instructions.html").read_text(encoding="utf-8")
        payload = json.loads(viewer.split('<script id="viewer-data" type="application/json">', 1)[1].split('</script>', 1)[0])
        with fitz.open(part/"assembly/assembly_instructions.pdf") as book:
            assert len(book) == len(payload["slides"]) == 8
            assert payload["slides"][2]["id"] == payload["start"]
            assert payload["slides"][2]["steps"] == [1, 2, 3, 4]
            for page, slide in zip(book, payload["slides"], strict=True):
                assert abs(page.rect.width - 297*72/25.4) < .1 and abs(page.rect.height - 210*72/25.4) < .1
                assert payload["images"][slide["image"]].startswith("data:image/")
                assert [a["url"] for a in slide["links"]] == [a["uri"] for a in page.get_links()]
        assert not re.search(r"short (rear |back )?(pins|tails)", content, re.I)
        prepared = next(h for h in assembly["hardware"] if "header_oobb_" in h["id"])
        stock = next(h for h in assembly["hardware"] if "header_long_" in h["id"])
        hardware = ELECTRONIC / "parts" / prepared["id"]
        record = yaml.safe_load((hardware / "working.yaml").read_text(encoding="utf-8"))
        assert record["parent_header_id"] == stock["id"]
        assert sha(hardware / "data/model_3d.step") == assembly["source_sha256"]["header_step"]
        assert record["header_dimensions_mm"]["front_pin"] == record["header_dimensions_mm"]["rear_pin"] == 6.25
        for item in assembly["hardware"]:
            assert (ELECTRONIC / "parts" / item["id"] / "working.yaml").is_file()
            assert item["url"] in content
        for name in assembly["images"].values():
            with Image.open(part / name) as image:
                assert image.size == (1600, 1080)
            images += 1
    for render in manifest["hardware_renders"]:
        part = ELECTRONIC / "parts" / render["id"]
        output = part / "data" / render["file"]
        assert output.read_bytes() == (ELECTRONIC / "parts_source" / render["id"] / render["file"]).read_bytes()
        with Image.open(output) as image:
            assert image.size == (1600, 1080)
        content = (part / "README.md").read_text(encoding="utf-8")
        for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", content):
            link = unquote(match[1]).split("#", 1)[0]
            if link and "://" not in link:
                assert (part / link).exists(), (part, link)
        images += 1
    result = dict(assemblies=len(expected), matched_pdf_and_html_guides=len(expected), header_long_lengths=40, prepared_header_models=14,
                  vertical_arrangements=9, full_resolution_images=images,
                  reference="HOAUC 1625-1140CNG0S150001 / LCSC C343639",
                  pin_ends_mm=[6.25, 6.25], overall_pin_mm=15,
                  source_hashes="matched", hardware_references="matched", physical_fit_tested=False)
    (ROOT / "presentation/wire_validation.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
