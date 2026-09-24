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

# plate is 4 mm tall, the wire channel pockets are cut 2.8 mm deep from
# the top face leaving a 1.2 mm floor, the wire pass through cuts and all
# holes go all the way through
WIRE_DEPTH_DEFAULT = 4
WIRE_CUTOUT_DEPTH = 2.8

# connector hardware (mm), sized for 2.54 mm header chunks
WIRE_KEY_RADIUS = 3.0            # circular key hole for the 2x2 header chunk (spacer plates)
WIRE_KEY_OFFSET_X = 1.27         # half a pitch off centre so it keys
WIRE_CUT_EXTRA = 2               # cutout overshoot so cuts go fully through
WIRE_HEADER_CLEARANCE = 0.54     # clearance for header pieces in their cutouts

# the pocket is the bar for the holder: it seats the header bar behind
# the exit opening, one pitch (2.54) + 0.54 clearance long, and two
# positions (2 x 2.54) wider than the exit centered on it -- which is
# also three positions wider than the run on the keyed types since their
# exit is the run + 2.54 (this reproduces the original 15.24 pocket)
WIRE_POCKET_LENGTH = 2.54 + WIRE_HEADER_CLEARANCE
WIRE_POCKET_EXTRA_WIDTH = 2 * 2.54

# rim between the pocket and the front edge, taken unscaled from the
# original 53 mm drawing (edge at 26.5, pocket bottom at 20.32); it also
# sets the exit slot length and pushes the holder back off the edge
WIRE_POCKET_FRONT_CLEARANCE = 6.18

# wire routing channels in absolute mm lifted from the old 53 mm (3 x 3 @
# 20 mm) drawings; the connectors are the same 2.54 mm hardware whatever
# the grid so NOTHING is scaled to the 15 mm grid and every position and
# length is a multiple of 2.54 (or the 1.27 half pitch where a keying
# offset is needed); widths are n x 2.54, or n x 2.54 + 0.54 clearance
# where the header piece seats in them
# each channel: (center_x, entry_width, entry_top, step_y, run_width)
#   entry - narrower tab the wire drops into at the back (the back wire
#           clearance box; shorten y_top towards y_step if a type ever
#           needs the room)
#   run   - main vertical run from step_y down to the pocket, widens at
#           step_y
# the front piece is derived: the exit slot is the run width (motor types)
# or run + 2.54 shifted half a pitch left (wire types), the pocket is the
# exit + 2 x 2.54 centered on it, and both sit WIRE_POCKET_FRONT_CLEARANCE
# back from the front edge so the run bottom follows the pocket position
# keyed wire types get a half cylinder notch in the front edge to show
# the keying side
WIRE_EXIT_NOTCH_TYPES = ["basic", "i2c", "power"]
WIRE_EXIT_NOTCH_RADIUS = 1.5
WIRE_EXIT_NOTCH_GAP = 3

WIRE_CHANNELS = {
    "basic": [
        (1.27, 5.62, 10.16, -3.81, 7.62),
    ],
    "power": [
        (0.00, 3.08, 2.54, -3.81, 5.08),
    ],
    "motor": [
        (0.00, 3.08, 10.16, 3.81, 5.08),
    ],
    "motor_stepper": [
        (0.00, 8.16, 10.16, 3.81, 10.16),
    ],
    "i2c": [
        (1.27, 8.16, 10.16, 3.81, 10.16),
    ],
}


def get_wire(thing, **kwargs):
    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    depth = kwargs.get("depth", WIRE_DEPTH_DEFAULT)
    wire_type = kwargs.get("wire_type", "basic")
    pos = kwargs.get("pos", [0, 0, 0])

    sp = oobb.gv("osp")
    grid_x = (width - 1) / 2 * sp      # connector column/row offsets
    grid_y = (height - 1) / 2 * sp
    half_slot = grid_x / 2             # pin hole offsets along an edge

    def add_through(**p3):
        p3["type"] = "negative"
        p3["pos"] = [p3["pos"][0] + pos[0], p3["pos"][1] + pos[1], p3["pos"][2] + pos[2]]
        oobb.append_full(thing, **p3)

    def add_pocket(**p3):
        # 2.8 mm deep pocket cut down from the top face
        p3["type"] = "negative"
        p3["pos"] = [p3["pos"][0] + pos[0], p3["pos"][1] + pos[1], depth - WIRE_CUTOUT_DEPTH + pos[2]]
        oobb.append_full(thing, **p3)

    def pocket_rect(x, y, size_x, size_y):
        # cube is corner anchored in opsc so shift by half size
        add_pocket(
            shape="cube",
            size=[size_x, size_y, WIRE_CUTOUT_DEPTH + 1],
            pos=[x - size_x / 2, y - size_y / 2, 0],
        )

    def through_rect(x, y, size_x, size_y):
        add_through(
            shape="cube",
            size=[size_x, size_y, depth + WIRE_CUT_EXTRA],
            pos=[x - size_x / 2, y - size_y / 2, -1],
        )

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

    #no key hole at the back any more: the full size channel needs the
    #space, the keying is the offset front exit (and the edge notch on
    #the wire types) so the plug only fits one way round

    #wire routing channel, 2.8 mm deep, exiting through the front edge
    if True:
        for channel in WIRE_CHANNELS.get(wire_type, []):
            (cx, w_entry, y_top, y_step, w_run) = channel

            #the holder sits WIRE_POCKET_FRONT_CLEARANCE back from the
            #front edge (as in the original, unscaled) and the run ends
            #at the top of the pocket, which is one pitch + clearance long
            plate_front_y = -(height * sp - oobb.gv("osp_minus")) / 2
            y_bottom = plate_front_y + WIRE_POCKET_FRONT_CLEARANCE
            y_run_bottom = y_bottom + WIRE_POCKET_LENGTH

            #entry tab and run go all the way through (the wires pass
            #through them), entry above the step, full width run below it
            through_rect(cx, (y_top + y_step) / 2, w_entry, y_top - y_step)
            through_rect(cx, (y_step + y_run_bottom) / 2, w_run, y_step - y_run_bottom)

            #front opening: motor and motor_stepper match the inside
            #channel exactly, the wire types keep the right side flush
            #with the run and open 2.54 mm wider on the left so the
            #plug only fits one way round
            if wire_type in ("motor", "motor_stepper"):
                exit_cx = cx
                w_exit = w_run
            else:
                exit_cx = cx - 1.27
                w_exit = w_run + 2.54
            #pocket is the bar for the holder: exit + 2 x 2.54 wide
            #centered on the exit opening, and the exit slot runs out
            #through the front plate edge from it
            w_pocket = w_exit + WIRE_POCKET_EXTRA_WIDTH
            pocket_rect(exit_cx, (y_run_bottom + y_bottom) / 2, w_pocket, y_run_bottom - y_bottom)
            pocket_rect(exit_cx, y_bottom - 10, w_exit, 20)

            #half cylinder notch in the front edge marking the keying
            #side, a gap of 3 mm left of the exit
            if wire_type in WIRE_EXIT_NOTCH_TYPES:
                notch_x = exit_cx - w_exit / 2 - WIRE_EXIT_NOTCH_GAP - WIRE_EXIT_NOTCH_RADIUS
                add_pocket(
                    shape="cylinder",
                    r=WIRE_EXIT_NOTCH_RADIUS,
                    h=WIRE_CUTOUT_DEPTH + 1,
                    pos=[notch_x, plate_front_y, 0],
                )

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
        add_through(
            shape="rounded_rectangle",
            size=[cutout[0], cutout[1], depth + WIRE_CUT_EXTRA],
            r=SPACER_CUTOUT_RADIUS,
            pos=[0, 0, -1],
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
