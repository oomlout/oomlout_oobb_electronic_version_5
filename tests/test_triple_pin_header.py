"""Check the stepped header seat and vertically stacked connector rows."""

import unittest
from unittest.mock import patch

import oobb
import oomp
import working_oomp_populate as populate
import working_scad


def empty_thing():
    return {"components": [], "components_objects": [], "components_string": []}


class TriplePinHeaderTests(unittest.TestCase):
    def test_population_keeps_count_in_id_and_drawing_parameters(self):
        with patch.object(populate, "write_extras") as write:
            populate.main()
        options = write.call_args.args[0]
        triples = [p for p in options if p.get("part_style") == "triple_pin_header"]
        self.assertEqual(triples[0]["multiple"], 3)
        self.assertEqual(sorted(p["multiple"] for p in triples), list(range(2, 11)))
        ids = [populate.build_oomp_id(p) for p in triples]
        self.assertEqual(len(set(ids)), 9)
        for option in triples:
            details = option["oobb_details"]
            self.assertEqual(details["multiple"], option["multiple"])
            self.assertEqual(details["wire_style"], "triple_pin_header")
            self.assertEqual(details["wire_type"], "basic")
            self.assertEqual(details["height"], 3)
            self.assertAlmostEqual(details["depth"], 2.54 * (option["multiple"] + 1))
            self.assertEqual(details["width"], 3)
            self.assertTrue(populate.build_oomp_id(option).endswith(f"_{option['multiple']}_multiple"))
            self.assertEqual(populate.build_oomp_id(option), oomp.get_id(**option))

    def test_floor_window_keyed_front_and_larger_rear_clearances(self):
        thing = empty_thing()
        working_scad.get_wire(thing, wire_style="triple_pin_header", pos=[20, 30, 5])
        calls = thing["components_objects"]
        seat, rear, housing, front = [p for p in calls if p["shape"] == "cube"][:4]
        # The smaller seat opens the bottom layer and meets the upper recess.
        self.assertAlmostEqual(seat["size"][0], 3 * 2.54 + 0.8)
        self.assertAlmostEqual(seat["size"][1], 2.54 + 0.8)
        self.assertAlmostEqual(seat["pos"][2] + seat["size"][2], 5 + 2.54)
        self.assertAlmostEqual(housing["pos"][2], 5 + 2.54)
        self.assertAlmostEqual(front["pos"][2], 5 + 2.54)
        self.assertAlmostEqual(front["size"][0], 4 * 2.54)
        self.assertGreater(housing["size"][0], 7.62 + 0.4)
        self.assertGreater(rear["size"][0], 5.62)
        self.assertLessEqual(rear["pos"][2], 5)
        self.assertGreaterEqual(rear["pos"][2] + rear["size"][2], 5 + 10.16)
        # A six-pitch-wide header pocket must not be reintroduced.
        self.assertTrue(all(p["size"][0] < 6 * 2.54 for p in (seat, rear, housing, front)))
        self.assertFalse(any(p["shape"] == "oobb_wire" for p in calls))
        scad = oobb.scad_render(oobb.opsc_get_object(thing["components"], mode="3dpr"))
        self.assertIn("difference()", scad)

    def test_population_does_not_create_a_standalone_top_part(self):
        with patch.object(populate, "write_extras") as write:
            populate.main()
        tops = [p for p in write.call_args.args[0] if p.get("part_style") == "triple_pin_header_top"]
        self.assertEqual(tops, [])

    def test_top_holes_align_with_each_base_and_keep_the_front_closed(self):
        for multiple in range(2, 11):
            base = empty_thing()
            working_scad.get_wire(base, wire_style="triple_pin_header", multiple=multiple, pos=[20, 30, 5])
            calls = base["components_objects"]
            plates = [p for p in calls if p["shape"] == "oobb_plate"]
            self.assertEqual(len(plates), 2)
            self.assertEqual(plates[1]["depth"], 2.54)
            self.assertEqual(plates[1]["pos"], [70, 30, 5])
            cuts_base = [p for p in calls if p["shape"] == "cube"][:4]
            cuts_top = [p for p in calls if p["shape"] == "cube"][4:]
            self.assertEqual(len(cuts_top), 2)
            for cut in cuts_top:
                self.assertLess(cut["pos"][2], 5)
                self.assertGreater(cut["pos"][2] + cut["size"][2], 5 + 2.54)
                self.assertGreater(cut["pos"][1], 30 - 22)  # bridge across the front
            for top_cut, base_cut in zip(cuts_top, cuts_base[:2]):
                self.assertEqual(top_cut["size"][:2], base_cut["size"][:2])
                self.assertAlmostEqual(top_cut["pos"][0] - base_cut["pos"][0], 50)
                self.assertEqual(top_cut["pos"][1], base_cut["pos"][1])
            holes = [p for p in calls if p["shape"] == "oobb_hole"]
            self.assertEqual(len(holes), 24)
            for top_hole, base_hole in zip(holes[12:], holes[:12]):
                self.assertEqual(top_hole["radius_name"], base_hole["radius_name"])
                self.assertAlmostEqual(top_hole["pos"][0] - base_hole["pos"][0], 50)
                self.assertEqual(top_hole["pos"][1], base_hole["pos"][1])
        scad = oobb.scad_render(oobb.opsc_get_object(base["components"], mode="3dpr"))
        self.assertIn("difference()", scad)

    def test_stacks_change_depth_without_repeating_the_footprint(self):
        for multiple in range(2, 11):
            with self.subTest(multiple=multiple):
                thing = empty_thing()
                working_scad.get_wire(thing, wire_style="triple_pin_header",
                                      multiple=multiple, polarizing_pin=False)
                calls = thing["components_objects"]
                cubes = [p for p in calls if p["shape"] == "cube"]
                self.assertEqual(len(cubes), 6)
                self.assertFalse(any(p["shape"] == "cylinder" for p in calls))
                plate = next(p for p in calls if p["shape"] == "oobb_plate")
                self.assertEqual((plate["width"], plate["height"]), (3, 3))
                self.assertAlmostEqual(plate["depth"], (multiple + 1) * 2.54)
                housing, front = cubes[2:4]
                self.assertAlmostEqual(housing["size"][2] - 1, multiple * 2.54)
                self.assertAlmostEqual(front["size"][2] - 1, multiple * 2.54)

    def test_invalid_counts_and_insufficient_host_dimensions_are_rejected(self):
        for multiple in (0, 1, 11, 2.5, True):
            with self.subTest(multiple=multiple), self.assertRaises(ValueError):
                working_scad.get_wire(empty_thing(), wire_style="triple_pin_header", multiple=multiple)
        for params in ({"depth": 4}, {"multiple": 2, "width": 2}, {"height": 1}, {"wire_type": "motor"}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                working_scad.get_wire(empty_thing(), wire_style="triple_pin_header", **params)


if __name__ == "__main__":
    unittest.main()
