# Lane macro power grid: met1 rails + met4 straps, pins on met4.
# No met5 inside the macro; the top level drops met5 over it and connects
# met5 -> met4 with the stock sky130hs macro grid.
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
define_pdn_grid -name {grid} -voltage_domains {CORE} -pins {met4}
add_pdn_stripe -grid {grid} -layer {met1} -width {0.48} -pitch {6.66} -offset {0} -followpins
add_pdn_stripe -grid {grid} -layer {met4} -width {1.600} -pitch {27.140} -offset {13.570}
add_pdn_connect -grid {grid} -layers {met1 met4}
