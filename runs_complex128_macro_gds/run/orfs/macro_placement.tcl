# 128 lanes on a 12 x 11 grid centred in the 18.8 mm core (4 slots empty).
# Pitch 1560 x 1700 um around a ~938 um macro leaves 622 / 762 um channels
# for the 49,152 top-level operand and result nets.
for {set i 0} {$i < 128} {incr i} {
    set col [expr {$i % 12}]
    set row [expr {$i / 12}]
    set x [expr {451.0 + $col * 1560.0}]
    set y [expr {531.0 + $row * 1700.0}]
    set name [format {lanes\[%d\].lane} $i]
    place_macro -macro_name $name -location [list $x $y] -orientation R0 -exact
}
