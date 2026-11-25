"""Blender worker for the OOBB basic wire holder and its header references."""
import json
import sys
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_catalogue import aim, material

MM = .001
WIRE_COLOURS = [(204, 58, 64), (201, 203, 197), (69, 86, 135), (62, 134, 87)]


def load(path, name, finish, xyz=(0, 0, 0), rotation=0):
    bpy.ops.wm.stl_import(filepath=str(path))
    obj = bpy.context.object
    obj.name = name
    obj.scale = (MM,) * 3
    obj.rotation_euler.z = rotation
    obj.location = Vector(xyz) * MM
    obj.data.materials.append(finish)
    return obj


def cable(name, points, finish):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 24
    curve.bevel_depth = .46 * MM
    curve.bevel_resolution = 5
    curve.use_fill_caps = True
    line = curve.splines.new("BEZIER")
    line.bezier_points.add(len(points) - 1)
    for point, xyz in zip(line.bezier_points, points):
        point.co = Vector(xyz) * MM
        point.handle_left_type = point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, curve)
    bpy.context.scene.collection.objects.link(obj)
    curve.materials.append(finish)
    return obj


def studio():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    prefs = bpy.context.preferences.addons["cycles"].preferences
    try:
        prefs.compute_device_type = "OPTIX"
        prefs.get_devices()
        for device in prefs.devices:
            device.use = device.type == "OPTIX"
        if any(d.use for d in prefs.devices):
            scene.cycles.device = "GPU"
    except (RuntimeError, TypeError):
        pass
    scene.render.resolution_x = 1440
    scene.render.resolution_y = 812
    scene.render.resolution_percentage = 100
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    scene.view_settings.view_transform = "AgX"
    scene.world = bpy.data.worlds.new("Studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (.8, .8, .8, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = .35
    return scene


def frame(scene, objects, direction):
    bpy.context.view_layer.update()
    corners = [obj.matrix_world @ Vector(v) for obj in objects for v in obj.bound_box]
    lo, hi = (Vector([f(p[i] for p in corners) for i in range(3)]) for f in (min, max))
    center = (lo + hi) / 2
    span = max(hi - lo)
    for name, pos, energy, radius in [
        ("Key", (-2, -3, 5), 22, 4), ("Fill", (3, -1, 3), 12, 3), ("Rim", (0, 4, 4), 18, 3),
    ]:
        lamp = bpy.data.lights.new(name, "AREA")
        lamp.energy = energy * .07 * (span / .1) ** 2
        lamp.shape = "DISK"
        lamp.size = span * radius
        light = bpy.data.objects.new(name, lamp)
        scene.collection.objects.link(light)
        light.location = center + Vector(pos) * span
        aim(light, center)
    camera = bpy.data.cameras.new("Orthographic studio")
    camera.type = "ORTHO"
    camera.clip_start = .0001
    cam = bpy.data.objects.new("Camera", camera)
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.location = center + Vector(direction).normalized() * span * 3
    aim(cam, center)
    bpy.context.view_layer.update()
    local = [cam.matrix_world.inverted() @ p for p in corners]
    a, b = ([f(p[i] for p in local) for i in (0, 1)] for f in (min, max))
    cam.location += cam.rotation_euler.to_matrix() @ Vector(((a[0]+b[0])/2, (a[1]+b[1])/2, 0))
    camera.ortho_scale = max(b[0]-a[0], (b[1]-a[1]) * 1440/812) * 1.14
    bpy.context.view_layer.update()
    return cam


def render(job, view):
    import math

    scene = studio()
    teal = material("Satin teal PLA", (0, 177, 183))
    black = material("Black connector insulator", (18, 18, 18), .33)
    gold = material("Gold-plated brass", (212, 168, 83), .25)
    gold.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = .8
    tin = material("Tin-plated contact", (186, 191, 195), .3)
    tin.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = .8
    objects, anchors = [], {}
    variant = job.get("variant", {})
    count = variant.get("contacts", 3)
    hx = variant.get("header_x", 0)
    cx = variant.get("housing_x", 1.27)
    if job.get("single"):
        objects.append(load(job["single"], "Socket housing", black))
        direction = (-.7, -1.55, 1.7)
    elif view in ("stock", "keyed"):
        bundle = job["stock" if view == "stock" else "header"]
        prefix = "model_3d_3_strip" if view == "keyed" and job.get("rows") else job.get("mesh_prefix", "model_3d")
        objects.append(load(Path(bundle) / f"{prefix}_body.stl", "Breakaway insulator", black))
        objects.append(load(Path(bundle) / f"{prefix}_pins.stl", "Header contacts", gold))
        direction = (-.7, -1.55, 1.7)
    elif job.get("rows"):
        rows, depth = job["rows"], job["depth"]
        exploded = view == "exploded"
        objects.append(load(job["plate"], "Production base", teal))
        cap_x = 50 if view == "plate" else 0
        cap_z = 0 if view == "plate" else depth + (35 if exploded else 0)
        if view != "seating":
            objects.append(load(job["cap"], "Included top retainer", teal, (cap_x, 0, cap_z)))
        anchors.update(pocket=(1.27, -14.4, 1.5), rear=(1.27, 9, depth),
                       cap=(cap_x-12, -12, cap_z+2.54))
        direction = (-1.1, -1.7, 1.8)
        if view != "plate":
            hz = 1.27 * (rows+2) + (8 if exploded else 0)
            header = Path(job["header"])
            for col, x in enumerate((-1.27, 1.27, 3.81)):
                objects.append(load(header / "model_3d_body.stl", f"Vertical insulator {col+1}", black, (x, -14.4, hz)))
                objects.append(load(header / "model_3d_pins.stl", f"Vertical contacts {col+1}", gold, (x, -14.4, hz)))
            for row in range(rows):
                z = 2.56 + row*2.54 + (17 if exploded else 0)
                y = -13.13 + (4 if exploded else 0)
                objects.append(load(job["housing"], f"Row {row+1} socket housing", black, (1.27, y, z)))
                for col, x in enumerate((-1.27, 1.27, 3.81)):
                    mid = 1.27 + (col-1)*1.45
                    entry_y = 2 + row*.9
                    wire_z = z+1.25
                    end_y = y+14
                    if exploded:
                        start = end_y+3
                        objects.append(load(job["contact"], f"Socket {row+1}.{col+1}", tin,
                                            (x, start, wire_z-1.3), math.pi/2))
                        start += 11.25
                        points = [(x, start, wire_z), (x, start+3, wire_z),
                                  (mid, 17+row*.7, wire_z-5), (mid, entry_y, depth+3)]
                    else:
                        points = [(x, end_y-.2, wire_z), (x, end_y+.6, wire_z),
                                  (mid, entry_y, wire_z-.25)]
                    points += [(mid, entry_y, -1.5), (mid, entry_y+2, -3.8),
                               (mid+(col-1), 26+row*.9, -5-row*.12)]
                    objects.append(cable(f"Wire {row+1}.{col+1}", points,
                                         material(f"Jacket {row+1}.{col+1}", WIRE_COLOURS[col], .48)))
            anchors["header"] = (-2.54, -15.82, hz)
            anchors["housing"] = (1.27, -7, z+2.5)
            anchors["crimp"] = (-1.27, end_y+7, 2.56+(17 if exploded else 0)+1.75)
            anchors["wires"] = (1.27, 10, -3)
            if exploded:
                direction = (-1.5, -.85, 1.1)
            elif view != "seating":
                anchors["header"] = (1.27, -14.4, depth+2.54)
                anchors["wires"] = (1.27, 3, depth-1)
    else:
        objects.append(load(job["plate"], "Production printed plate", teal))
        anchors["key"] = (-9.58, -21.6, 2.9)
        anchors["pocket"] = (-6.7, -14.5, 1.21)
        anchors["rear"] = (cx, 8, 4.01)
        direction = (-.65, -1.35, 2.45)
        if view != "plate":
            exploded = view == "exploded"
            lift = 7 if view == "seating" else 0
            header_z = 2.47 + (10 if exploded else lift)
            housing_y = -13.01 + (4 if exploded else 0)
            housing_z = 1.22 + (17 if exploded else lift)
            header = Path(job["header"])
            objects.append(load(header / "model_3d_body.stl", "Keyed header insulator", black, (hx, -14.28, header_z)))
            objects.append(load(header / "model_3d_pins.stl", "Retained contacts", gold, (hx, -14.28, header_z)))
            objects.append(load(job["housing"], f"{count}-way female crimp housing", black, (cx, housing_y, housing_z)))
            anchors["header"] = (-4.8, -15.45, header_z + 1.28)
            anchors["housing"] = (cx, housing_y + 6, housing_z + 2.51)
            for index in range(count):
                offset = index - (count-1)/2
                x = cx + offset * 2.54
                mid = cx + offset * 1.45
                exit_x = mid + offset * 1.15
                end_y = housing_y + 14
                wire_z = housing_z + 1.25
                if exploded:
                    # The socket row is pulled back along its insertion axis.
                    start_contact = end_y + 3
                    objects.append(load(job["contact"], f"Loose socket {index+1}", tin,
                                        (x, start_contact, wire_z - 1.3), math.pi / 2))
                    wire_start = start_contact + 11.25
                    points = [(x, wire_start, wire_z), (x, wire_start+3, wire_z),
                              (mid, 18, 10), (mid, 7.5, 5), (mid, 7.5, -1.3),
                              (mid, 10, -3.4), (exit_x, 24, -4.5), (exit_x, 29, -4.5)]
                    anchors["crimp"] = (cx + (count-1)*1.27, start_contact+6, wire_z+1.3)
                else:
                    points = [(x, end_y-.2, wire_z), (x, 2.15, wire_z),
                              (mid, 4.5, 2.15), (mid, 7, .4), (mid, 8.4, -2.9),
                              (mid, 11.7, -4), (exit_x, 24, -4.5), (exit_x, 29, -4.5)]
                objects.append(cable(f"Wire {index+1}", points, material(f"Wire jacket {index+1}", WIRE_COLOURS[index], .48)))
            anchors["wires"] = (-.18, 9.5, -2.8)
            if exploded:
                direction = (-1.25, -.72, 1.46)
                anchors["wires"] = (-.18, 13.5, 7)
    cam = frame(scene, objects, direction)
    out = Path(job["scratch"])
    scene.render.filepath = str(out / (view + ".png"))
    if not job.get("project_only"):
        bpy.ops.render.render(write_still=True)
    projected = {name: tuple(world_to_camera_view(scene, cam, Vector(point) * MM)[:2])
                 for name, point in anchors.items()}
    (out / (view + ".json")).write_text(json.dumps(projected), encoding="utf-8")


if __name__ == "__main__":
    jobs = json.loads(Path(sys.argv[sys.argv.index("--") + 1]).read_text(encoding="utf-8"))
    for job in jobs if isinstance(jobs, list) else [jobs]:
        for view in job["views"]:
            print(f"Rendering {job['scratch']} / {view}", flush=True)
            render(job, view)
