
SIM ?= icarus
TOPLEVEL_LANG = verilog

VERILOG_SOURCES = $(abspath ../../src/mac_unit.v) \
                  $(abspath ../../src/matrix_core.v) \
                  $(abspath ../../src/tensortop.v) \
                  $(abspath ../../src/project.v)

TOPLEVEL = tt_um_muhamm30_tinytensor
COCOTB_TEST_MODULES = test_chip

include $(shell cocotb-config --makefiles)/Makefile.sim
