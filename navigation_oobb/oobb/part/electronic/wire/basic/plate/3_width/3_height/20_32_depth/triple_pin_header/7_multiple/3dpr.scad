$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [-17.0, 17.0, 0]) {
				cylinder(h = 20.32, r = 5);
			}
			translate(v = [17.0, 17.0, 0]) {
				cylinder(h = 20.32, r = 5);
			}
			translate(v = [-17.0, -17.0, 0]) {
				cylinder(h = 20.32, r = 5);
			}
			translate(v = [17.0, -17.0, 0]) {
				cylinder(h = 20.32, r = 5);
			}
		}
		translate(v = [50, 0, 0]) {
			hull() {
				translate(v = [-17.0, 17.0, 0]) {
					cylinder(h = 2.54, r = 5);
				}
				translate(v = [17.0, 17.0, 0]) {
					cylinder(h = 2.54, r = 5);
				}
				translate(v = [-17.0, -17.0, 0]) {
					cylinder(h = 2.54, r = 5);
				}
				translate(v = [17.0, -17.0, 0]) {
					cylinder(h = 2.54, r = 5);
				}
			}
		}
	}
	union() {
		translate(v = [-15.0, -15.0, -89.84]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [15.0, -15.0, -89.84]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-15.0, 15.0, -89.84]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [15.0, 15.0, -89.84]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-15.0, 0, -89.84]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [15.0, 0, -89.84]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-7.5, 15.0, -89.84]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [7.5, 15.0, -89.84]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-15.0, -7.5, -89.84]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [15.0, -7.5, -89.84]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-15.0, 7.5, -89.84]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [15.0, 7.5, -89.84]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-2.94, -16.22, -1]) {
			cube(size = [8.42, 3.34, 3.54]);
		}
		translate(v = [-2.04, -2.54, -1]) {
			cube(size = [6.62, 13.969999999999999, 22.32]);
		}
		translate(v = [-2.94, -16.22, 2.54]) {
			cube(size = [8.42, 17.34, 18.78]);
		}
		translate(v = [-5.08, -23.0, 2.54]) {
			cube(size = [10.16, 7.18, 18.78]);
		}
		translate(v = [-9.58, -22.0, 2.54]) {
			cylinder(h = 18.78, r = 1.5);
		}
		translate(v = [35.0, -15.0, -98.73]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [65.0, -15.0, -98.73]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [35.0, 15.0, -98.73]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [65.0, 15.0, -98.73]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [35.0, 0, -98.73]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [65.0, 0, -98.73]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [42.5, 15.0, -98.73]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [57.5, 15.0, -98.73]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [35.0, -7.5, -98.73]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [65.0, -7.5, -98.73]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [35.0, 7.5, -98.73]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [65.0, 7.5, -98.73]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [47.06, -16.22, -1]) {
			cube(size = [8.42, 3.34, 4.54]);
		}
		translate(v = [47.96, -2.54, -1]) {
			cube(size = [6.62, 13.969999999999999, 4.54]);
		}
	}
}
