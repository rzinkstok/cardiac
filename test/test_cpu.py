import pytest
from cardiac import CPU
import types


INSTRUCTION = 147


@pytest.fixture
def cpu():
    cpu = CPU()
    return cpu


def bla(self, arg):
    self.acc = arg


def mem_get_int(self, address):
    return INSTRUCTION


def test_cpu_init(cpu):
    assert cpu.acc == 0
    assert cpu.pc == 0
    assert cpu.ir == 0


def test_cpu_instructions(cpu):
    cpu.opcode_1_cla = types.MethodType(bla, cpu)
    cpu.gather_instructions()
    assert len(cpu.opcodes) == 1
    assert 1 in cpu.opcodes
    assert cpu.opcodes[1] == "cla"


def test_cpu_fetch(cpu):
    cpu.opcode_1_cla = types.MethodType(bla, cpu)
    cpu.mem_get_int = types.MethodType(mem_get_int, cpu)
    cpu.gather_instructions()
    cpu.fetch()
    assert cpu.ir == 147
    assert cpu.pc == 1


def test_cpu_process(cpu):
    cpu.opcode_1_cla = types.MethodType(bla, cpu)
    cpu.mem_get_int = types.MethodType(mem_get_int, cpu)
    cpu.gather_instructions()
    cpu.process()
    assert cpu.acc == 47
