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
		translate(v = [-1.54, -3.8100000000000005, -1]) {
			cube(size = [5.62, 13.97, 6]);
		}
		translate(v = [-2.54, -12.74, -1]) {
			cube(size = [7.62, 8.93, 6]);
		}
		translate(v = [-7.62, -15.82, 1.2000000000000002]) {
			cube(size = [15.24, 3.08, 3.8]);
		}
		translate(v = [-5.08, -35.82, 1.2000000000000002]) {
			cube(size = [10.16, 20, 3.8]);
		}
		translate(v = [-9.58, -22.0, 1.2000000000000002]) {
			cylinder(h = 3.8, r = 1.5);
		}
	}
}
