
import cocotb
from cocotb.triggers import Timer


async def tick(dut):
    """Generate one clock cycle."""
    dut.clk.value = 0
    await Timer(5, unit="ns")
    dut.clk.value = 1
    await Timer(5, unit="ns")
    dut.clk.value = 0
    await Timer(1, unit="ns")


def signed12(value):
    """Interpret a 12-bit output as signed."""
    value = int(value) & 0xFFF
    return value - 4096 if value & 0x800 else value


@cocotb.test()
async def test_mac(dut):
    # Initialize inputs
    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.clear.value = 0
    dut.enable.value = 0
    dut.a.value = 0
    dut.b.value = 0

    await tick(dut)
    assert signed12(dut.acc.value) == 0

    # Release reset and test signed products
    dut.rst_n.value = 1
    dut.enable.value = 1

    expected = 0
    cases = [
        (3, 2),       # +6
        (3, -2),      # -6
        (-4, -3),     # +12
        (-8, 7),      # -56
        (-8, -8),     # +64
    ]

    for a, b in cases:
        dut.a.value = a & 0xF
        dut.b.value = b & 0xF

        await tick(dut)

        expected += a * b
        actual = signed12(dut.acc.value)

        assert actual == expected, (
            f"MAC failed: {a} * {b}, "
            f"expected {expected}, got {actual}"
        )

        dut._log.info(
            f"a={a}, b={b}, accumulator={actual}"
        )

    # Disable accumulation
    dut.enable.value = 0
    dut.a.value = 7
    dut.b.value = 7

    await tick(dut)
    assert signed12(dut.acc.value) == expected

    # Clear accumulator
    dut.clear.value = 1
    await tick(dut)
    assert signed12(dut.acc.value) == 0

    # Accumulate again after clearing
    dut.clear.value = 0
    dut.enable.value = 1
    dut.a.value = 2
    dut.b.value = 3

    await tick(dut)
    assert signed12(dut.acc.value) == 6

    # Test asynchronous reset
    dut.rst_n.value = 0
    await Timer(1, unit="ns")
    assert signed12(dut.acc.value) == 0

    dut._log.info("All MAC tests passed!")
