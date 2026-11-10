read_db /mnt/results/complex128_gpu_128/base/2_1_floorplan.odb
source /mnt/design/macro_placement.tcl
set count 0
foreach inst [[ord::get_db_block] getInsts] {
    if {[$inst isPlaced]} {
        incr count
    }
}
puts "FIXED_MACROS=$count"
if {$count != 128} {
    exit 1
}
