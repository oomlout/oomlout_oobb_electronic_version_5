"""The electronic project owns the plate; OOBB owns the wire-holder void."""

import unittest
from unittest.mock import patch

import oobb
import working_scad


class WireIntegrationTests(unittest.TestCase):
    def test_all_plates_place_one_library_void(self):
        for wire_type in ("basic", "power", "motor", "motor_stepper", "i2c"):
            with self.subTest(wire_type=wire_type):
                thing = {"components": [], "components_objects": [], "components_string": []}
                working_scad.get_wire(thing, wire_type=wire_type)
                calls = thing["components_objects"]
                plates = [item for item in calls if item["shape"] == "oobb_plate"]
                holes = [item for item in calls if item["shape"] == "oobb_hole"]
                wires = [item for item in calls if item["shape"] == "oobb_wire"]
                self.assertEqual(len(plates), 1)
                self.assertEqual([plates[0][k] for k in ("width", "height", "depth")], [3, 3, 4])
                self.assertEqual(plates[0]["type"], "positive")
                self.assertEqual(len(holes), 12)
                self.assertEqual(sum(item["radius_name"] == "m6" for item in holes), 6)
                self.assertEqual(sum(item["radius_name"] == "m3" for item in holes), 6)
                self.assertEqual(len(wires), 1)
                self.assertEqual(wires[0]["wire_type"], wire_type)
                self.assertEqual(wires[0]["type"], "negative")
                self.assertFalse(wires[0]["plate"])
                self.assertTrue(wires[0]["polarizing_pin"])
                self.assertEqual(len(calls), 14)
                # Exercise real component discovery and OpenSCAD construction.
                scad = oobb.scad_render(oobb.opsc_get_object(thing["components"], mode="3dpr"))
                self.assertIn("difference()", scad)
                self.assertIn("cube", scad)

    def test_polarizing_toggle_and_position_reach_component(self):
        thing = {"components": [], "components_objects": [], "components_string": []}
        working_scad.get_wire(thing, wire_type="power", polarizing_pin=False, pos=[20, 30, 5])
        placed = thing["components_objects"][-1]
        self.assertFalse(placed["polarizing_pin"])
        self.assertEqual(placed["pos"], [20, 30, 5])
        group = thing["components"][-1][0]
        self.assertEqual(group["pos"], [20, 30, 5])
        self.assertTrue(all(item["shape"] == "cube" for item in group["objects"]))

    def test_print_preparation_stays_in_project(self):
        thing = {"components": [], "components_objects": [], "components_string": []}
        with patch.object(working_scad.scad_help, "prepare_base_for_print") as prepare:
            working_scad.get_wire(thing, prepare_print=True)
        prepare.assert_called_once_with(thing, [0, 0, 0], prepare_print=True)


if __name__ == "__main__":
    unittest.main()
