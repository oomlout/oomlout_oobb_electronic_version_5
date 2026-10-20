import copy
import oobb
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    typ = scad_help.get_typ(**kwargs)
    oomp_mode = "project"
    #oomp_mode = "oobb"
    filt = ""
    build_variables = scad_help.get_build_variables(typ, filter=filt)
    if True:
        kwargs["filter"] = build_variables["filter"]
        kwargs["save_type"] = build_variables["save_type"]
        kwargs["navigation"] = build_variables["navigation"]
        kwargs["overwrite"] = build_variables["overwrite"]
        kwargs["modes"] = build_variables["modes"]
        kwargs["oomp_mode"] = oomp_mode
        kwargs["oomp_run"] = build_variables["oomp_run"]
    parts = get_parts(kwargs, oomp_mode)
    
    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    if kwargs["navigation"]:
        oobb_style = False  
        sort = scad_help.get_navigation_sort(oobb_style=oobb_style)
        scad_help.generate_navigation(sort=sort)

def get_parts(kwargs, oomp_mode):
    parts = []    

    #load parts from parts/folder/working.yaml
    parts_directory = os.path.join(os.path.dirname(__file__), "parts")
    if not os.path.isdir(parts_directory):
        return parts

    for folder in os.listdir(parts_directory):
        folder_path = os.path.join(parts_directory, folder)
        if not os.path.isdir(folder_path):
            continue

        working_yaml_path = os.path.join(folder_path, "working.yaml")
        if not os.path.isfile(working_yaml_path):
            continue

        with open(working_yaml_path, "r", encoding="utf-8") as infile:
            loaded_part = yaml.safe_load(infile)

        if not isinstance(loaded_part, dict):
            continue

        oobb_details = loaded_part.get("oobb_details")
        if not isinstance(oobb_details, dict):
            continue

        part = loaded_part

        part_kwargs = copy.deepcopy(kwargs)
        part_kwargs.update(copy.deepcopy(loaded_part.get("kwargs", {})))
        part_kwargs.update(copy.deepcopy(oobb_details))
        part["kwargs"] = part_kwargs
        part["oobb_name"] = part.get("oobb_name", oobb_details.get("oobb_name", "default"))

        if oomp_mode == "oobb":
            part["kwargs"]["oomp_size"] = part["oobb_name"]

        parts.append(part)


    return parts

def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    


    #add plate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"    
        p3["depth"] = depth
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)
    
    #add holes seperate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_holes"
        p3["both_holes"] = True  
        p3["depth"] = depth
        p3["holes"] = "perimeter"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)

    #add a test screw_countersunk
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"screw_countersunk"
        p3["depth"] = depth
        p3["radius_name"] = "m3"
        pos1 = copy.deepcopy(pos)         
        pos1[2] += depth
        p3["pos"] = pos1
        p3["m"] = "#"
        oobb.append_full(thing,**p3)

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)

###### wire connector plates (migrated from old OOEB WI-* parts)

# Shared plate/spacer dimensions. Standard wire-holder voids come from
# the OOBB library; the triple-header stack is drawn locally below.
WIRE_DEPTH_DEFAULT = 4
WIRE_KEY_RADIUS = 3.0
WIRE_KEY_OFFSET_X = 1.27
WIRE_CUT_EXTRA = 2

# Triple headers seat in a through-window in a 2.54 mm bottom layer.
# The upper recess keeps the basic connector's four-pitch keyed exit.
WIRE_TRIPLE_PITCH = 2.54
WIRE_TRIPLE_BOTTOM_DEPTH = 2.54
WIRE_TRIPLE_MULTIPLE_DEFAULT = 3
WIRE_TRIPLE_FIT_CLEARANCE = 0.4  # per side, versus 0.2 on the single style
WIRE_TRIPLE_ENTRY_EXTRA = 1.0   # total extra width for the larger wire bundle
WIRE_TRIPLE_FRONT_CLEARANCE = 6.18
WIRE_TRIPLE_HOUSING_LENGTH = 14.0


def get_wire_triple_pin_header_holes(thing, **kwargs):
    """Matching beam and rear wire holes for the bottom layer and top plate."""
    height = kwargs.get("height", 3)
    depth = kwargs["depth"]
    header_cut_depth = kwargs.get("header_cut_depth", WIRE_TRIPLE_BOTTOM_DEPTH)
    pos = kwargs.get("pos", [0, 0, 0])
    pitch = WIRE_TRIPLE_PITCH
    clearance = WIRE_TRIPLE_FIT_CLEARANCE
    front_y = -(height * oobb.gv("osp") - oobb.gv("osp_minus")) / 2
    header_front = front_y + WIRE_TRIPLE_FRONT_CLEARANCE
    entry_top, entry_bottom = 11.43, -2.54

    # A three-pin-wide, one-pitch-long beam hole, with fit allowance.
    oobb.append_full(
        thing, type="negative", shape="cube",
        size=[3 * pitch + 2 * clearance, pitch + 2 * clearance, header_cut_depth + 1],
        pos=[pos[0] + pitch / 2 - (3 * pitch + 2 * clearance) / 2,
             pos[1] + header_front - clearance, pos[2] - 1],
    )
    # Same enlarged wire entry on both pieces, open through their full depth.
    entry_width = 5.62 + WIRE_TRIPLE_ENTRY_EXTRA
    oobb.append_full(
        thing, type="negative", shape="cube",
        size=[entry_width, entry_top - entry_bottom, depth + WIRE_CUT_EXTRA],
        pos=[pos[0] + pitch / 2 - entry_width / 2,
             pos[1] + entry_bottom, pos[2] - 1],
    )


def get_wire_triple_pin_header_top_void(thing, **kwargs):
    """Retain the beams with a closed front and a hole matching the base seat."""
    params = copy.deepcopy(kwargs)
    params["header_cut_depth"] = params["depth"] + 1
    get_wire_triple_pin_header_holes(thing, **params)


def get_wire_triple_pin_header_void(thing, **kwargs):
    """Cut one three-pin seat, its keyed front, and the rear wire clearance."""
    height = kwargs.get("height", 3)
    multiple = kwargs.get("multiple", WIRE_TRIPLE_MULTIPLE_DEFAULT)
    required_depth = round(WIRE_TRIPLE_BOTTOM_DEPTH + multiple * WIRE_TRIPLE_PITCH, 2)
    depth = kwargs.get("depth", required_depth)
    pos = kwargs.get("pos", [0, 0, 0])
    if depth < required_depth - 1e-9:
        raise ValueError(f"triple_pin_header with {multiple} rows needs at least {required_depth} mm total depth")

    pitch = WIRE_TRIPLE_PITCH
    clearance = WIRE_TRIPLE_FIT_CLEARANCE
    front_y = -(height * oobb.gv("osp") - oobb.gv("osp_minus")) / 2
    header_front = front_y + WIRE_TRIPLE_FRONT_CLEARANCE
    header_back = header_front + pitch
    run_top = header_back + WIRE_TRIPLE_HOUSING_LENGTH
    entry_top = 11.43
    if run_top >= entry_top:
        raise ValueError("triple_pin_header needs a taller plate for the rear wire entry")

    def rect(x, y, size_x, size_y, z, size_z):
        oobb.append_full(
            thing, type="negative", shape="cube",
            size=[size_x, size_y, size_z],
            pos=[pos[0] + x - size_x / 2, pos[1] + y - size_y / 2, pos[2] + z],
        )

    get_wire_triple_pin_header_holes(thing, height=height, depth=depth, pos=pos)

    # Leave 2.54 mm below the housing and front recess. Their overlap with
    # the seat and rear entry makes a continuous path for the connector.
    recess_depth = depth - WIRE_TRIPLE_BOTTOM_DEPTH + 1
    rect(pitch / 2, (header_front + run_top) / 2,
         3 * pitch + 2 * clearance, run_top - header_front + 2 * clearance,
         WIRE_TRIPLE_BOTTOM_DEPTH, recess_depth)
    rect(0, (front_y - 1 + header_front) / 2,
         4 * pitch, header_front - front_y + 1,
         WIRE_TRIPLE_BOTTOM_DEPTH, recess_depth)

    if kwargs.get("polarizing_pin", True):
        oobb.append_full(
            thing, type="negative", shape="cylinder", r=1.5, h=recess_depth,
            pos=[pos[0] - 2 * pitch - 3 - 1.5,
                 pos[1] + front_y, pos[2] + WIRE_TRIPLE_BOTTOM_DEPTH],
        )


def get_wire(thing, **kwargs):
    prepare_print = kwargs.get("prepare_print", False)
    triple_pin_header = kwargs.get("wire_style", "") == "triple_pin_header"
    triple_pin_header_top = kwargs.get("wire_style", "") == "triple_pin_header_top"
    multiple = kwargs.get("multiple", WIRE_TRIPLE_MULTIPLE_DEFAULT) if triple_pin_header else 1
    if triple_pin_header:
        if type(multiple) is not int or not 2 <= multiple <= 10:
            raise ValueError("triple_pin_header multiple must be an integer from 2 to 10")
    if (triple_pin_header or triple_pin_header_top) and kwargs.get("wire_type", "basic") != "basic":
        raise ValueError("triple_pin_header and its top retainer are basic wire styles")
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    default_depth = round(WIRE_TRIPLE_BOTTOM_DEPTH + multiple * WIRE_TRIPLE_PITCH, 2) if triple_pin_header else WIRE_DEPTH_DEFAULT
    if triple_pin_header_top:
        default_depth = WIRE_TRIPLE_BOTTOM_DEPTH
    depth = kwargs.get("depth", default_depth)
    pos = kwargs.get("pos", [0, 0, 0])
    if (triple_pin_header or triple_pin_header_top) and width < 3:
        raise ValueError("triple_pin_header plate width must be at least 3")

    sp = oobb.gv("osp")
    grid_x = (width - 1) / 2 * sp      # connector column/row offsets
    grid_y = (height - 1) / 2 * sp
    half_slot = grid_x / 2             # pin hole offsets along an edge

    def add_through(**p3):
        p3["type"] = "negative"
        p3["pos"] = [p3["pos"][0] + pos[0], p3["pos"][1] + pos[1], p3["pos"][2] + pos[2]]
        oobb.append_full(thing, **p3)

    #plate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = "oobb_plate"
        p3["width"] = width
        p3["height"] = height
        p3["depth"] = depth
        p3["pos"] = copy.deepcopy(pos)
        oobb.append_full(thing, **p3)

    #normal oobb m6 mounting holes on the grid: the four corners plus the
    #side edge midpoints (the front midpoint area carries the wire exit)
    if True:
        hole_positions = [
            (-grid_x, -grid_y),
            (grid_x, -grid_y),
            (-grid_x, grid_y),
            (grid_x, grid_y),
            (-grid_x, 0),
            (grid_x, 0),
        ]
        for hx, hy in hole_positions:
            add_through(
                shape="oobb_hole",
                radius_name="m6",
                pos=[hx, hy, depth / 2],
            )

    #m3 pin holes where the old header slots used to be: two on the top
    #edge flanking the key and two down each side edge
    if True:
        pin_positions = [(-half_slot, grid_y), (half_slot, grid_y)]
        for sy in (-half_slot, half_slot):
            pin_positions.append((-grid_x, sy))
            pin_positions.append((grid_x, sy))
        for px, py in pin_positions:
            add_through(
                shape="oobb_hole",
                radius_name="m3",
                pos=[px, py, depth / 2],
            )

    if triple_pin_header_top:
        p3 = copy.deepcopy(kwargs)
        p3.update(height=height, depth=depth, pos=copy.deepcopy(pos))
        get_wire_triple_pin_header_top_void(thing, **p3)
    elif triple_pin_header:
        p3 = copy.deepcopy(kwargs)
        p3.update(height=height, depth=depth, multiple=multiple, pos=copy.deepcopy(pos))
        get_wire_triple_pin_header_void(thing, **p3)

        # Each version prints its matching top beside the base, with a 6 mm gap.
        # The internal top style shares the mounting pattern and beam holes.
        top_kwargs = copy.deepcopy(kwargs)
        top_kwargs.pop("multiple", None)
        top_kwargs.update(
            wire_style="triple_pin_header_top", width=width, height=height,
            depth=WIRE_TRIPLE_BOTTOM_DEPTH, prepare_print=False,
            pos=[pos[0] + width * sp - oobb.gv("osp_minus") + 6, pos[1], pos[2]],
        )
        get_wire(thing, **top_kwargs)
    else:
        # Reusable single-header void; triple-header geometry stays local.
        p3 = copy.deepcopy(kwargs)
        p3.update(
            shape="oobb_wire",
            type="negative",
            plate=False,
            wire_type=kwargs.get("wire_type", "basic"),
            polarizing_pin=kwargs.get("polarizing_pin", True),
            width=width,
            height=height,
            depth=depth,
            pos=copy.deepcopy(pos),
        )
        oobb.append_full(thing, **p3)

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)


def get_wire_barrel_jack(thing, **kwargs):
    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    overall_depth = kwargs.get("depth", 12)
    slice_depth = overall_depth / 2
    pos = kwargs.get("pos", [0, 0, 0])
    wire_style = kwargs.get("wire_style", "")
    slice_offsets_x = [-25, 25]
    plate_front_y = (height * oobb.gv("osp") - oobb.gv("osp_minus")) / 2
    spacer_front_y = SPACER_CUTOUT_LITTLE[1] / 2
    cylinder_depth = plate_front_y - spacer_front_y + 0.5

    # The slices print side by side; stack the second one on the first for the full depth.
    for slice_number, slice_offset_x in enumerate(slice_offsets_x):
        spacer_floor = 0
        if wire_style == "bottom_solid" and slice_number == 0:
            spacer_floor = 1.5

        slice_kwargs = {
            "width": width,
            "height": height,
            "depth": slice_depth,
            "spacer_type": "little",
            "spacer_floor": spacer_floor,
            "pos": [
                pos[0] + slice_offset_x,
                pos[1],
                pos[2],
            ],
        }
        get_spacer(thing, **slice_kwargs)

        # Both cuts share the assembled split-plane axis. The lower slice
        # keeps the cylinder's lower half; the upper slice keeps its upper half.
        kwargs_entry = {
            "shape": "cylinder",
            "type": "negative",
            "r": 7 / 2,
            "h": cylinder_depth,
            "rot": [-90, 0, 0],
            "pos": [
                pos[0] + slice_offset_x,
                pos[1] - plate_front_y,
                pos[2] + (slice_depth if slice_number == 0 else 0),
            ],
        }
        oobb.append_full(thing, **kwargs_entry)

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)


###### spacer plates (migrated from old OOEB HL-SPAC / HL-SPBC parts)

# spacers stack with the wire connector plates to hold the 2.54 mm header
# chunks at height; four types, big and little are frames whose centre
# cutouts are the old HL-SPBC (31 x 45) and HL-SPAC (27 x 27) windows
# scaled by 15/20 -- the bigger window is big:
#   big    - tall window, the front and back pin rows are dropped (the
#            window swallows them), keeps the side pins
#   little - square window, full pattern including the back holes (key
#            circle + top pins) so it nests under any wire plate
#   hole   - solid plate with a single m10 hole in the centre
#   solid  - plain plate, no centre feature
# hole and solid carry the full pin pattern (back row + sides) but no key
# pin styles, applied to the m3 pin holes and added after depth in the
# taxonomy (eg ..._4_depth_countersunk_style):
#   basic             - m3 clearance holes, no extra name
#   countersunk_style - m3 countersunk screw cutouts instead of the m3 holes
#   nut_style         - m3 nut traps (overhang true) instead of the m3 holes

# the big window keeps the drawing's 45 mm height but its width matches
# little's so both leave the same 1.6 mm wall to the m6 holes at +-15;
# the literal 31 x 15/20 = 23.25 wide would leave a 0.1 mm sliver there
# (the old part got away with it because its edge holes were slim m3
# slots, not m6 clearance holes)
SPACER_CUTOUT_BIG = [20.25, 33.75]     # old HL-SPBC 31x45 window (height x 15/20)
SPACER_CUTOUT_LITTLE = [20.25, 20.25]  # old HL-SPAC 27x27 window x 15/20
SPACER_CUTOUT_RADIUS = 3.75            # old r5 window corners x 15/20


def get_spacer(thing, **kwargs):
    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    depth = kwargs.get("depth", WIRE_DEPTH_DEFAULT)
    spacer_type = kwargs.get("spacer_type", "big")
    spacer_style = kwargs.get("spacer_style", "")
    spacer_floor = kwargs.get("spacer_floor", 0)
    pos = kwargs.get("pos", [0, 0, 0])

    #style arrives as "countersunk_style" / "nut_style" / ""
    style = spacer_style.replace("_style", "")

    sp = oobb.gv("osp")
    grid_x = (width - 1) / 2 * sp
    grid_y = (height - 1) / 2 * sp
    half_slot = grid_x / 2

    def add_through(**p3):
        p3["type"] = "negative"
        p3["pos"] = [p3["pos"][0] + pos[0], p3["pos"][1] + pos[1], p3["pos"][2] + pos[2]]
        oobb.append_full(thing, **p3)

    #plate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = "oobb_plate"
        p3["width"] = width
        p3["height"] = height
        p3["depth"] = depth
        p3["pos"] = copy.deepcopy(pos)
        oobb.append_full(thing, **p3)

    #normal oobb m6 mounting holes on the grid, same six positions as the
    #wire plates
    if True:
        hole_positions = [
            (-grid_x, -grid_y),
            (grid_x, -grid_y),
            (-grid_x, grid_y),
            (grid_x, grid_y),
            (-grid_x, 0),
            (grid_x, 0),
        ]
        for hx, hy in hole_positions:
            add_through(
                shape="oobb_hole",
                radius_name="m6",
                pos=[hx, hy, depth / 2],
            )

    #little carries the back holes (key circle and top pin row), hole and
    #solid carry the top pin row without the key, big drops the front and
    #back rows and keeps only the side pins
    if spacer_type == "little":
        add_through(
            shape="cylinder",
            r=WIRE_KEY_RADIUS,
            h=depth + WIRE_CUT_EXTRA,
            pos=[WIRE_KEY_OFFSET_X, grid_y, -1],
        )
        pin_positions = [(-half_slot, grid_y), (half_slot, grid_y)]
    elif spacer_type in ("hole", "solid"):
        pin_positions = [(-half_slot, grid_y), (half_slot, grid_y)]
    else:
        pin_positions = []
    for sy in (-half_slot, half_slot):
        pin_positions.append((-grid_x, sy))
        pin_positions.append((grid_x, sy))

    #pin positions: m3 hole, countersunk screw or nut trap depending on style
    for px, py in pin_positions:
        if style == "countersunk":
            add_through(
                shape="screw_countersunk",
                radius_name="m3",
                depth=depth,
                pos=[px, py, depth],
            )
        elif style == "nut":
            add_through(
                shape="oobb_nut",
                radius_name="m3",
                overhang=True,
                hole=True,
                zz="top",
                pos=[px, py, depth],
            )
        else:
            add_through(
                shape="oobb_hole",
                radius_name="m3",
                pos=[px, py, depth / 2],
            )

    #centre feature: window cutout for the frame types, m10 hole or nothing
    if spacer_type == "big":
        cutout = SPACER_CUTOUT_BIG
    elif spacer_type == "little":
        cutout = SPACER_CUTOUT_LITTLE
    if spacer_type in ("big", "little"):
        cutout_start = -1
        cutout_depth = depth + WIRE_CUT_EXTRA
        if spacer_floor:
            cutout_start = spacer_floor
            cutout_depth = depth - spacer_floor + WIRE_CUT_EXTRA
        add_through(
            shape="rounded_rectangle",
            size=[cutout[0], cutout[1], cutout_depth],
            r=SPACER_CUTOUT_RADIUS,
            pos=[0, 0, cutout_start],
        )
    elif spacer_type == "hole":
        add_through(
            shape="oobb_hole",
            radius_name="m10",
            pos=[0, 0, depth / 2],
        )

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)


def get_hole_cover(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    diameter = kwargs.get("diameter", 10)
    clearance = kwargs.get("clearance", 0.5)
    thickness_wall = 2
    depth_taper = 3
    depth_top = 2
    diameter_top_extra = 10
    radius_gap=6
    diameter_top_taper = 5

    #add cylinder
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_cylinder"    
    dep = depth - depth_taper 
    p3["depth"] = dep
    p3["radius"] = (diameter-clearance)/2
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += depth_taper + dep/2
    p3["pos"] = pos1
    oobb.append_full(thing,**p3)
    
    #add cylinder taper using radius_1 and radius_2
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_cylinder"
    p3["depth"] = depth_taper
    p3["radius_2"] = (diameter-clearance)/2
    p3["radius_1"] = (diameter+clearance-thickness_wall)/2    
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth_taper/2
    p3["pos"] = pos1
    oobb.append_full(thing,**p3)

    #add top cylinder
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_cylinder"
    p3["depth"] = depth_top
    dia = diameter+diameter_top_extra
    p3["radius_2"] = (dia-diameter_top_taper)/2
    p3["radius_1"] = (dia)/2
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth-depth_top/2
    p3["pos"] = pos1
    oobb.append_full(thing,**p3)

    

    #add hole
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cylinder"
    p3["depth"] = depth - depth_top/2
    p3["radius"] = (diameter+clearance-thickness_wall)/2    

    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2 - depth_top/2
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb.append_full(thing,**p3)

    
    #diameter_top 30
    #add hole_top
    diameter_top_hole = 30
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cylinder"
    p3["depth"] = depth_top
    p3["radius"] = (diameter_top_hole)/2
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth - depth_top/2

    p3["pos"] = pos1
    p3["m"] = "#"
    oobb.append_full(thing,**p3)

    pos1 = copy.deepcopy(pos)
    pos1[1] += 100



    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)

    
if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)
