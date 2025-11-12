"""
Tests for memory classes.

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import pytest

from constants import STACK_BASE
from memory import DataMemory, InstructionMemory, Memory


def test_write_out_of_range():
    m = Memory()
    m.write_enable(True)
    with pytest.raises(ValueError):
        m.write(0x10000, 0xABCD)  # beyond 16-bit range


def test_read_default_from_unwritten_cell():
    m = Memory()
    assert m.read(0x1234) == 0


def test_mem_write_when_enabled():
    m = Memory()
    m.write_enable(True)
    m.write(0x0000, 0xABCD)
    m.write_enable(True)
    m.write(0x0001, 0x1234)
    m.write_enable(True)
    m.write(0x0002, 0x1111)
    assert m.read(0) == 0xABCD
    assert m.read(1) == 0x1234
    assert m.read(2) == 0x1111


def test_mem_write_when_disabled():
    m = Memory()
    with pytest.raises(RuntimeError):
        m.write(0, 0xABCD)


def test_write_enable_clears_after_write():
    m = Memory()
    m.write_enable(True)
    m.write(0x0000, 0xABCD)
    assert not m._write_enable


@pytest.mark.parametrize("addr,val", [(0x0000, 0xABCD), (0x0000, 0x1234)])
def test_mem_hexdump(addr, val):
    # This is a feeble test---should revise.
    m = Memory()
    m.write_enable(True)
    m.write(addr, val)
    for line in m.hexdump(0, 1):
        addr_str = f"{addr:04X}"
        val_str = f"{val:04X}"
        assert line == f"{addr_str}: {val_str}"


def test_hexdump_multiple_lines_and_range():
    m = Memory()
    for i in range(10):
        m.write_enable(True)
        m.write(i, i)
    lines = list(m.hexdump(0, 10, width=4))
    assert len(lines) == 3  # restricted to width


def test_load_program():
    p = [0x0DFF, 0xC002, 0xE000, 0x9206, 0x5288, 0xA003, 0xD000]
    im = InstructionMemory()
    im.load_program(p)
    for addr, inst in enumerate(p):
        assert im.read(addr) == inst


def test_load_program_disables_write():
    im = InstructionMemory()
    im.load_program([0x1234])
    assert not im._write_enable


def test_instruction_memory_write_protected():
    """
    Direct write should fail
    """
    im = InstructionMemory()
    with pytest.raises(RuntimeError):
        im.write_enable(True)
        im.write(0x0000, 0xBEEF)


def test_instruction_memory_load_program_allowed():
    im = InstructionMemory()
    program = [0xAAAA, 0xBBBB]
    im.load_program(program)
    for addr, word in enumerate(program):
        assert im.read(addr) == word


def test_data_memory_blocks_nonstack_write():
    """
    Ensure writes at or beyond STACK_BASE raise an error.
    """
    dm = DataMemory()
    dm.write_enable(True)
    with pytest.raises(RuntimeError, match="stack region"):
        dm.write(STACK_BASE, 0xABCD)

    dm.write_enable(True)
    with pytest.raises(RuntimeError):
        dm.write(STACK_BASE + 1, 0xBEEF)


def test_data_memory_allows_stack_write_when_flag_set():
    """
    Verify that writes with from_stack=True succeed in stack region.
    """
    dm = DataMemory()
    dm.write_enable(True)
    dm.write(STACK_BASE, 0xABCD, from_stack=True)

    # confirm value is stored
    assert dm.read(STACK_BASE) == 0xABCD


def test_data_memory_normal_region_writable():
    """
    Writes below STACK_BASE should always succeed.
    """
    dm = DataMemory()
    dm.write_enable(True)
    dm.write(0x0100, 0x1234)
    assert dm.read(0x0100) == 0x1234


def test_memory_len_and_contains():
    m = Memory()
    assert len(m) == 0
    m.write_enable(True)
    m.write(0, 0xABCD)
    assert len(m) == 1
    assert 0 in m
    assert 1 not in m
