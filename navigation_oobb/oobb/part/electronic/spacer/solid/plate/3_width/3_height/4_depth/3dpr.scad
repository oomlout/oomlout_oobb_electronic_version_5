$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [-17.0, 17.0, 0]) {
				cylinder(h = 4, r = 5);
			}
			translate(v = [17.0, 17.0, 0]) {
				cylinder(h = 4, r = 5);
			}
			translate(v = [-17.0, -17.0, 0]) {
				cylinder(h = 4, r = 5);
			}
			translate(v = [17.0, -17.0, 0]) {
				cylinder(h = 4, r = 5);
			}
		}
	}
	union() {
		translate(v = [-15.0, -15.0, -98.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [15.0, -15.0, -98.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-15.0, 15.0, -98.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [15.0, 15.0, -98.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-15.0, 0, -98.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [15.0, 0, -98.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-7.5, 15.0, -98.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [7.5, 15.0, -98.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-15.0, -7.5, -98.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [15.0, -7.5, -98.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-15.0, 7.5, -98.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [15.0, 7.5, -98.0]) {
			cylinder(h = 200, r = 1.8);
		}
	}
}
