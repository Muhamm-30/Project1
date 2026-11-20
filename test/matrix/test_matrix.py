
import cocotb
from cocotb.triggers import Timer


async def tick(dut):
    dut.clk.value = 0
    await Timer(5, unit="ns")
    dut.clk.value = 1
    await Timer(5, unit="ns")
    dut.clk.value = 0
    await Timer(1, unit="ns")


def signed12(value):
    value = int(value) & 0xFFF
    return value - 4096 if value & 0x800 else value


def write_int4(signal, value):
    signal.value = value & 0xF


@cocotb.test()
async def test_matrix(dut):
    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.clear.value = 0
    dut.enable.value = 0

    for name in ("a0", "a1", "b0", "b1"):
        getattr(dut, name).value = 0

    await tick(dut)
    dut.rst_n.value = 1

    dut.enable.value = 1

    # Cycle 1: first outer product
    write_int4(dut.a0, 1)
    write_int4(dut.a1, 3)
    write_int4(dut.b0, 5)
    write_int4(dut.b1, 6)
    await tick(dut)

    # Cycle 2: second outer product
    write_int4(dut.a0, 2)
    write_int4(dut.a1, 4)
    write_int4(dut.b0, 7)
    write_int4(dut.b1, -2)
    await tick(dut)

    dut.enable.value = 0

    results = [
        signed12(dut.c00.value),
        signed12(dut.c01.value),
        signed12(dut.c10.value),
        signed12(dut.c11.value),
    ]

    expected = [19, 2, 43, 10]

    assert results == expected, (
        f"Expected {expected}, got {results}"
    )

    dut._log.info(f"Matrix result: {results}")
    dut._log.info("2x2 matrix multiplication passed!")


import random


@cocotb.test()
async def test_random_matrices(dut):
    rng = random.Random(42)

    for trial in range(100):
        A = [[rng.randint(-8, 7) for _ in range(2)]
             for _ in range(2)]
        B = [[rng.randint(-8, 7) for _ in range(2)]
             for _ in range(2)]

        expected = [
            A[0][0]*B[0][0] + A[0][1]*B[1][0],
            A[0][0]*B[0][1] + A[0][1]*B[1][1],
            A[1][0]*B[0][0] + A[1][1]*B[1][0],
            A[1][0]*B[0][1] + A[1][1]*B[1][1]
        ]

        # Reset all accumulators
        dut.clk.value = 0
        dut.rst_n.value = 0
        dut.clear.value = 0
        dut.enable.value = 0

        for name in ("a0", "a1", "b0", "b1"):
            getattr(dut, name).value = 0

        await tick(dut)
        dut.rst_n.value = 1
        dut.enable.value = 1

        # Two outer-product cycles
        for k in range(2):
            write_int4(dut.a0, A[0][k])
            write_int4(dut.a1, A[1][k])
            write_int4(dut.b0, B[k][0])
            write_int4(dut.b1, B[k][1])
            await tick(dut)

        actual = [
            signed12(dut.c00.value),
            signed12(dut.c01.value),
            signed12(dut.c10.value),
            signed12(dut.c11.value)
        ]

        assert actual == expected, (
            f"Trial {trial}: expected {expected}, got {actual}"
        )

    dut._log.info("All 100 random matrices passed!")


