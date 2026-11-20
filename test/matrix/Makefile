
SIM ?= icarus
TOPLEVEL_LANG = verilog

VERILOG_SOURCES = $(abspath ../../src/mac_unit.v) \
                  $(abspath ../../src/matrix_core.v)

TOPLEVEL = matrix_core
COCOTB_TEST_MODULES = test_matrix

include $(shell cocotb-config --makefiles)/Makefile.sim
