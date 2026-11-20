
SIM ?= icarus
TOPLEVEL_LANG = verilog

VERILOG_SOURCES = $(abspath ../../src/mac_unit.v)

TOPLEVEL = mac_unit
COCOTB_TEST_MODULES = test_mac

include $(shell cocotb-config --makefiles)/Makefile.sim
