# Count top-level met4 power/ground straps that cross into a lane macro
# (bbox shrunk by the 2 um PDN halo). Any hit means top-level met4 overlaps
# the lane's own met4 wiring in the merged GDS.
read_db /mnt/results/complex128_gpu_128/base/2_4_floorplan_pdn.odb
set block [ord::get_db_block]
set dbu [[ord::get_db_tech] getDbUnitsPerMicron]
set halo [expr {round(2.0 * $dbu)}]
set boxes {}
foreach inst [$block getInsts] {
    if {[[$inst getMaster] isBlock]} {
        set b [$inst getBBox]
        lappend boxes [list [expr {[$b xMin] + $halo}] [expr {[$b yMin] + $halo}] \
                            [expr {[$b xMax] - $halo}] [expr {[$b yMax] - $halo}]]
    }
}
set hits 0
set total 0
foreach net [$block getNets] {
    if {[$net getSigType] ni {POWER GROUND}} continue
    foreach sw [$net getSWires] {
        foreach w [$sw getWires] {
            if {[$w isVia]} continue
            if {[[$w getTechLayer] getName] ne "met4"} continue
            incr total
            set x0 [$w xMin]; set y0 [$w yMin]; set x1 [$w xMax]; set y1 [$w yMax]
            foreach m $boxes {
                lassign $m mx0 my0 mx1 my1
                if {$x0 < $mx1 && $x1 > $mx0 && $y0 < $my1 && $y1 > $my0} {
                    incr hits
                    break
                }
            }
        }
    }
}
puts "MACROS=[llength $boxes] MET4_PG_SHAPES=$total MET4_PG_INSIDE_LANES=$hits"
