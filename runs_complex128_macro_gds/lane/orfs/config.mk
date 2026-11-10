export DESIGN_NAME = complex128_unit
export DESIGN_NICKNAME = complex128_unit
export PLATFORM = sky130hs
export VERILOG_FILES = ./designs/src/snn_core/snn_core.v
export SDC_FILE = ./designs/src/snn_core/snn_core.sdc
export CORE_UTILIZATION = 40
export CLOCK_PERIOD = 10.0
export CLOCK_PORT = clk
# Macro hardening: keep met5 free for the top-level power grid.
# `override`: platform config.mk later sets MAX_ROUTING_LAYER = met5 with
# a plain assignment, which silently replaced an ordinary setting here.
override export MAX_ROUTING_LAYER = met4
export PDN_TCL = /mnt/design/pdn.tcl
