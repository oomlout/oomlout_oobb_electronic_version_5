import copy

from oomp_populate_helper import build_oomp_id, write_extras

# OOEB (OOBB Electronic) wire connector plates.
#
# Migrated from old_version/part/WI/* (20 mm OOEB grid) to the OOBB version 5
# 15 mm grid.  Each part is a 4 mm plate that holds 2.54 mm header chunks
# (with pins removed for holding and keying) in m3 holes, with m6 mounting
# holes on the OOBB grid and a 2.8 mm deep wire routing channel exiting
# through the front edge.  One part per wire connector type, old type codes
# map to the more verbose new names:
#
#   baw              -> basic           (replaces baw outright)
#   hv / bahv        -> power
#   mot              -> motor           (2 wire)
#   stm              -> motor_stepper   (4 wire)
#   i2c              -> i2c             (4 wire grove)
#
# removed because they did not fit the new system: ba2, bamt, bast
# (the old WI-ATXF/WI-ATXM/WI-I01 sheets are multi panel composites and are
#  not migrated either)
#
# taxonomy: oobb, part, electronic, wire, <type>, plate, <width>_width,
#           <height>_height, <depth>_depth
# barrel-jack plates use <jack>, plate, then the same three dimensions.
# A barrel-jack plate style follows the dimensions when one is set.
# spacers add the pin style after depth when set:
#           oobb, part, electronic, spacer, <type>, plate, <width>_width,
#           <height>_height, <depth>_depth, <style>

WIRE_WIDTH_DEFAULT = 3
WIRE_HEIGHT_DEFAULT = 3
WIRE_DEPTH_DEFAULT = 4
WIRE_HEADER_PITCH = 2.54
WIRE_TRIPLE_PIN_HEADER_MULTIPLES = [3, 2, *range(4, 11)]

WIRE_CONNECTOR_TYPES = [
    "basic",
    "power",
    "motor",
    "motor_stepper",
    "i2c",
]

# spacers stack with the wire plates to hold 2.54 mm header chunks at
# height; big and little are frames (the old HL-SPBC 31x45 window, the
# bigger one, is big; the old HL-SPAC 27x27 one is little), hole is solid
# with a single m10 hole and solid is plain; each comes in the three pin
# styles that replace the m3 pin holes
SPACER_TYPES = ["big", "little", "hole", "solid"]
SPACER_STYLES = ["", "countersunk_style", "nut_style"]


def apply_taxonomy(option):
    part_type = option["part_type"]
    part_style = option.get("part_style", "")
    taxonomy_6 = option.get("taxonomy_6", "plate")
    taxonomy_7 = option.get("taxonomy_7", "")
    oobb_name = option.pop("oobb_name", option["part_category"])
    width = option["width"]
    height = option["height"]
    depth = option["depth"]

    if taxonomy_6 == "plate":
        width_taxonomy_slot = 7
    else:
        taxonomy_7 = taxonomy_7 or "plate"
        width_taxonomy_slot = 8

    option["taxonomy_1"] = "oobb"
    option["taxonomy_2"] = "part"
    option["taxonomy_3"] = "electronic"
    option["taxonomy_4"] = option["part_category"]
    option["taxonomy_5"] = part_type
    option["taxonomy_6"] = taxonomy_6
    if taxonomy_7:
        option["taxonomy_7"] = taxonomy_7
    option[f"taxonomy_{width_taxonomy_slot}"] = f"{width}_width"
    option[f"taxonomy_{width_taxonomy_slot + 1}"] = f"{height}_height"
    option[f"taxonomy_{width_taxonomy_slot + 2}"] = f"{depth}_depth".replace(".", "_")
    if part_style:
        option[f"taxonomy_{width_taxonomy_slot + 3}"] = part_style
    if "multiple" in option:
        option[f"taxonomy_{width_taxonomy_slot + 4}"] = f"{option['multiple']}_multiple"

    option["oobb_details"] = {
        "oobb_name": oobb_name,
        f"{option['part_category']}_type": part_type,
        f"{option['part_category']}_style": part_style,
        "width": width,
        "height": height,
        "depth": depth,
    }
    if "multiple" in option:
        option["oobb_details"]["multiple"] = option["multiple"]


def main(**kwargs):
    options = []

    for wire_type in WIRE_CONNECTOR_TYPES:
        options.append(
            {
                "part_category": "wire",
                "part_type": wire_type,
                "width": WIRE_WIDTH_DEFAULT,
                "height": WIRE_HEIGHT_DEFAULT,
                "depth": WIRE_DEPTH_DEFAULT,
            }
        )

    # Make the three-row stack first; multiple counts rows vertically.
    # The bottom layer adds one pitch below the 2-10 header rows.
    for multiple in WIRE_TRIPLE_PIN_HEADER_MULTIPLES:
        options.append(
            {
                "part_category": "wire",
                "part_type": "basic",
                "part_style": "triple_pin_header",
                "multiple": multiple,
                "width": WIRE_WIDTH_DEFAULT,
                "height": WIRE_HEIGHT_DEFAULT,
                "depth": round(WIRE_HEADER_PITCH * (multiple + 1), 2),
            }
        )

    options.append(
        {
            "part_category": "wire",
            "part_type": "power",
            "part_style": "",
            "taxonomy_6": "barrel_jack_2_1_mm",
            "taxonomy_7": "plate",
            "oobb_name": "wire_barrel_jack",
            "width": 3,
            "height": 3,
            "depth": 12,
        }
    )

    options.append(
        {
            "part_category": "wire",
            "part_type": "power",
            "part_style": "bottom_solid",
            "taxonomy_6": "barrel_jack_2_1_mm",
            "taxonomy_7": "plate",
            "oobb_name": "wire_barrel_jack",
            "width": 3,
            "height": 3,
            "depth": 12,
        }
    )

    for spacer_type in SPACER_TYPES:
        for spacer_style in SPACER_STYLES:
            options.append(
                {
                    "part_category": "spacer",
                    "part_type": spacer_type,
                    "part_style": spacer_style,
                    "width": WIRE_WIDTH_DEFAULT,
                    "height": WIRE_HEIGHT_DEFAULT,
                    "depth": WIRE_DEPTH_DEFAULT,
                }
            )

    #load from working_manual.yaml
    if False:
        with open("working_manual.yaml", "r", encoding="utf-8") as file:
            import yaml

            data = yaml.safe_load(file)
            for option_yaml in data.get("options", []):
                options.append(option_yaml)

    for option in options:
        apply_taxonomy(option)

    extras = [copy.deepcopy(option) for option in options]

    import working_oomp_populate_extra_detail

    working_oomp_populate_extra_detail.main(extras=extras)
    write_extras(extras)


if __name__ == "__main__":
    main()
