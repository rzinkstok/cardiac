import pytest
from cardiac import (
    Memory,
    MemoryOutOfRange,
    InvalidAddress,
    DataValueOverflow,
    InvalidData,
)


@pytest.fixture
def memory():
    m = Memory()
    m.init_mem()
    return m


def test_memory_init(memory):
    assert len(memory.mem_cells) == 100

    assert memory.mem_get(0) == "001"


def test_mem_set(memory):
    memory.mem_set(5, "739")
    assert memory.mem_get(5) == "739"

    memory.mem_set(83, 15)
    assert memory.mem_get(83) == "015"

    memory.mem_set(34, -12)
    assert memory.mem_get(34) == "-012"

    with pytest.raises(MemoryOutOfRange):
        memory.mem_set(300, "000")

    with pytest.raises(MemoryOutOfRange):
        memory.mem_set(-13, 43)

    with pytest.raises(InvalidAddress):
        memory.mem_set("aa", "123")

    with pytest.raises(DataValueOverflow):
        memory.mem_set(45, 1001)

    with pytest.raises(InvalidData):
        memory.mem_set(73, "a")


def test_mem_get(memory):
    memory.mem_set(10, 1)
    memory.mem_set(12, -75)

    assert memory.mem_get(10) == "001"
    assert memory.mem_get_int(10) == 1
    assert memory.mem_get(12) == "-075"
    assert memory.mem_get_int(12) == -75
