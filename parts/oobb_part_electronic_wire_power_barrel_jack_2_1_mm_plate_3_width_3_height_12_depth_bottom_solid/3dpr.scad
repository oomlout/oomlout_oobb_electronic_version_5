$fn = 50;

difference() {
	union() {
		translate(v = [-25, 0, 0]) {
			hull() {
				translate(v = [-17.0, 17.0, 0]) {
					cylinder(h = 6.0, r = 5);
				}
				translate(v = [17.0, 17.0, 0]) {
					cylinder(h = 6.0, r = 5);
				}
				translate(v = [-17.0, -17.0, 0]) {
					cylinder(h = 6.0, r = 5);
				}
				translate(v = [17.0, -17.0, 0]) {
					cylinder(h = 6.0, r = 5);
				}
			}
		}
		translate(v = [25, 0, 0]) {
			hull() {
				translate(v = [-17.0, 17.0, 0]) {
					cylinder(h = 6.0, r = 5);
				}
				translate(v = [17.0, 17.0, 0]) {
					cylinder(h = 6.0, r = 5);
				}
				translate(v = [-17.0, -17.0, 0]) {
					cylinder(h = 6.0, r = 5);
				}
				translate(v = [17.0, -17.0, 0]) {
					cylinder(h = 6.0, r = 5);
				}
			}
		}
	}
	union() {
		translate(v = [-40.0, -15.0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-10.0, -15.0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-40.0, 15.0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-10.0, 15.0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-40.0, 0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-10.0, 0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [-23.73, 15.0, -1]) {
			cylinder(h = 8.0, r = 3.0);
		}
		translate(v = [-32.5, 15.0, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-17.5, 15.0, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-40.0, -7.5, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-10.0, -7.5, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-40.0, 7.5, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-10.0, 7.5, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [-25, 0, 1.5]) {
			hull() {
				translate(v = [-6.375, 6.375, 0]) {
					cylinder(h = 6.5, r = 3.75);
				}
				translate(v = [6.375, 6.375, 0]) {
					cylinder(h = 6.5, r = 3.75);
				}
				translate(v = [-6.375, -6.375, 0]) {
					cylinder(h = 6.5, r = 3.75);
				}
				translate(v = [6.375, -6.375, 0]) {
					cylinder(h = 6.5, r = 3.75);
				}
			}
		}
		translate(v = [-25, -22.0, 6.0]) {
			rotate(a = [-90, 0, 0]) {
				cylinder(h = 12.375, r = 3.5);
			}
		}
		translate(v = [10.0, -15.0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [40.0, -15.0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [10.0, 15.0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [40.0, 15.0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [10.0, 0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [40.0, 0, -97.0]) {
			cylinder(h = 200, r = 3.25);
		}
		translate(v = [26.27, 15.0, -1]) {
			cylinder(h = 8.0, r = 3.0);
		}
		translate(v = [17.5, 15.0, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [32.5, 15.0, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [10.0, -7.5, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [40.0, -7.5, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [10.0, 7.5, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [40.0, 7.5, -97.0]) {
			cylinder(h = 200, r = 1.8);
		}
		translate(v = [25, 0, -1]) {
			hull() {
				translate(v = [-6.375, 6.375, 0]) {
					cylinder(h = 8.0, r = 3.75);
				}
				translate(v = [6.375, 6.375, 0]) {
					cylinder(h = 8.0, r = 3.75);
				}
				translate(v = [-6.375, -6.375, 0]) {
					cylinder(h = 8.0, r = 3.75);
				}
				translate(v = [6.375, -6.375, 0]) {
					cylinder(h = 8.0, r = 3.75);
				}
			}
		}
		translate(v = [25, -22.0, 0]) {
			rotate(a = [-90, 0, 0]) {
				cylinder(h = 12.375, r = 3.5);
			}
		}
	}
}
