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
		translate(v = [-7.5, 15.0, 4]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.8);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
					}
					union();
				}
			}
		}
		translate(v = [7.5, 15.0, 4]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.8);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
					}
					union();
				}
			}
		}
		translate(v = [-15.0, -7.5, 4]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.8);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
					}
					union();
				}
			}
		}
		translate(v = [15.0, -7.5, 4]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.8);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
					}
					union();
				}
			}
		}
		translate(v = [-15.0, 7.5, 4]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.8);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
					}
					union();
				}
			}
		}
		translate(v = [15.0, 7.5, 4]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.8);
						}
						translate(v = [0, 0, -4.0]) {
							cylinder(h = 4, r = 1.5);
						}
					}
					union();
				}
			}
		}
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
	}
}
