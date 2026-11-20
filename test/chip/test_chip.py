
import cocotb
from cocotb.triggers import Timer


async def tick(dut):
    dut.clk.value = 0
    await Timer(5, unit="ns")
    dut.clk.value = 1
    await Timer(5, unit="ns")
    dut.clk.value = 0
    await Timer(1, unit="ns")


async def load(dut, index, value):
    dut.ui_in.value = value
    dut.uio_in.value = (index << 2) | 1
    await tick(dut)


async def read_result(dut, index):
    dut.uio_in.value = index << 2
    await Timer(1, unit="ns")
    return int(dut.uo_out.value)


@cocotb.test()
async def test_complete_accelerator(dut):
    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await tick(dut)
    dut.rst_n.value = 1

    # A = [[1, 2], [3, 4]]
    # B = [[5, 6], [7, -2]]

    # Pack two INT4 values per input byte.
    operands = [
        0x31,  # A column 0: 1, 3
        0x65,  # B row 0: 5, 6
        0x42,  # A column 1: 2, 4
        0xE7,  # B row 1: 7, -2
    ]

    for index, value in enumerate(operands):
        await load(dut, index, value)

    # Issue start command.
    dut.uio_in.value = 2
    await tick(dut)

    # Return command lines to idle.
    dut.uio_in.value = 0

    # Run both MAC cycles.
    await tick(dut)
    await tick(dut)

    # Read status: bit 0 indicates DONE.
    dut.uio_in.value = 1 << 5
    await Timer(1, unit="ns")

    status = int(dut.uo_out.value)
    assert status & 1, "Accelerator did not finish"

    # Read four signed 12-bit results.
    actual = []

    for i in range(4):
        lo = await read_result(dut, 2 * i)
        hi = await read_result(dut, 2 * i + 1)

        value = lo | ((hi & 0xF) << 8)

        if value & 0x800:
            value -= 4096

        actual.append(value)

    expected = [19, 2, 43, 10]

    assert actual == expected, (
        f"Expected {expected}, got {actual}"
    )

    dut._log.info(f"TinyTensor output: {actual}")
    dut._log.info("Full chip interface test passed!")
