import os
from cardiac import Cardiac

OPCODES = ("INP", "CLA", "ADD", "TAC", "SFT", "OUT", "STO", "SUB", "JMP", "HRS")


class UndefinedVariable(Exception):
    pass


class DuplicateVariable(Exception):
    pass


class InvalidInstruction(Exception):
    pass


class Instruction(object):
    def __init__(self, address, opcode, operand):
        self.address = address
        self.opcode = opcode
        self.operand = operand

    def card(self, variables):
        if self.opcode == "DATA":
            card = f"{int(self.operand):03}"
        else:
            opcode = OPCODES.index(self.opcode)
            if self.operand in variables:
                operand = variables[self.operand]
            else:
                try:
                    operand = int(self.operand)
                except ValueError:
                    raise UndefinedVariable(f"Variable {self.operand} is undefined")
            card = f"{opcode}{operand:02}"
        return f"0{self.address:02}\n{card}\n"


class Assembler(object):
    def __init__(self, filename=None):
        self.variables = {}
        self.instructions = []
        self.start_address = None
        self.current_address = 3
        self.output = ""
        self.output_filepath = None

        if filename:
            output_folder = os.path.abspath(os.path.dirname(filename))
            self.output_filepath = os.path.join(
                output_folder, os.path.splitext(os.path.split(filename)[1])[0] + ".cdc"
            )
            self.parse_file(filename)
            self.assemble()
            self.write_bytecode()

    def parse_file(self, fn):
        with open(fn, "r") as fp:
            lines = fp.readlines()
        for l in lines:
            self.parse_line(l)

    def parse_line(self, l):
        parts = l.rstrip("\n").split()

        if not parts:
            return

        if parts[0] in OPCODES:
            parts = [""] + parts
        parts = parts[:3]

        if len(parts) != 3:
            raise InvalidInstruction(f"Too few elements in {l}")

        if parts[1] not in list(OPCODES) + ["DATA"]:
            raise InvalidInstruction(f"Opcode not valid in {l}")

        if parts[0]:
            self.process_variable(parts)

        self.process_instruction(parts)

    def process_variable(self, x):
        self.variables[x[1]] = x[0]

    def process_instruction(self, x):
        label = x[0]
        opcode = x[1]
        operand = x[2]

        if not self.start_address and opcode != "DATA":
            self.start_address = self.current_address

        if label:
            if label in self.variables:
                raise DuplicateVariable(f"Variable name {label} is already defined")
            self.variables[label] = self.current_address

        self.instructions.append(Instruction(self.current_address, opcode, operand))
        self.current_address += 1

    def assemble(self):
        self.cards = []
        for i in self.instructions:
            self.cards.append(i.card(self.variables))

        self.output = ""
        self.output += "002\n800\n"
        self.output += "".join(self.cards)
        self.output += f"002\n8{self.start_address:02}"

    def write_bytecode(self):
        with open(self.output_filepath, "w") as fp:
            fp.write(self.output)


if __name__ == "__main__":
    a = Assembler("data/count.asm")
    c = Cardiac(verbose=True)
    c.read_deck(a.output_filepath)
    c.run()
