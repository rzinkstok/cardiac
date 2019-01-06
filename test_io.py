import pytest
from cardiac import IO


DECK = """002\n800\n010\n000\n011\n000\n900\n"""


@pytest.fixture()
def io():
    io = IO()
    return io


def test_io_init(io):
    assert len(io.input_stack) == 0
    assert len(io.output_stack) == 0


def test_io_input(io, tmp_path):
    f = tmp_path / "deck1.txt"
    f.write_text(DECK)
    io.read_deck(f)
    assert len(io.input_stack) == 7
    assert io.input_stack[4] == "010"


def test_io_get_input(io, tmp_path):
    f = tmp_path / "deck1.txt"
    f.write_text(DECK)
    io.read_deck(f)
    data = DECK.split()
    for d in data:
        assert d == io.get_input()
    assert len(io.input_stack) == 0


def test_io_put_output(io):
    data = ["001", "567", "-178"]
    for d in data:
        io.put_output(d)
    assert len(io.output_stack) == 3
    for d, o in zip(data, io.output_stack):
        assert d == o


def test_io_format_output(io, capsys):
    data = ["001", "567", "-178"]
    for d in data:
        io.put_output(d)
    io.format_output()
    out, err = capsys.readouterr()
    assert "\n".join(data) in out
