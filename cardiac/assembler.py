import os
from cardiac import Cardiac

INSTRUCTIONS = Cardiac().instructions


# Exception classes
class UndefinedVariable(Exception):
    pass


class DuplicateVariable(Exception):
    pass


class InvalidInstruction(Exception):
    pass


class Instruction(object):
    """Class containing all info for a single instruction line."""

    def __init__(self, address, opcode, operand):
        self.address = address
        self.opcode = opcode
        self.operand = operand

    def card(self, variables):
        """Create the addres/data card pair to store the instruction in memory.

        Args:
            variables (dict): a dict containing all variables that are defined
        """
        if self.opcode == "DATA":
            card = f"{int(self.operand):03}"
        else:
            opcode = INSTRUCTIONS.index(self.opcode)
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
    """A simple assembler for CARDIAC assembly code.

    Args:
        filename (str): the path to an assembly code file to process
    """

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
        """Loop over all lines in the file and hand them to the parse_line method."""
        with open(fn, "r") as fp:
            lines = fp.readlines()
        for l in lines:
            self.parse_line(l)

    def parse_line(self, l):
        """Parse a single line into the atomic tokens, and hand them to the process_instruction method."""
        tokens = l.rstrip("\n").split()

        if not tokens:
            return

        if tokens[0] in INSTRUCTIONS:
            tokens = [""] + tokens
        tokens = tokens[:3]

        if len(tokens) != 3:
            raise InvalidInstruction(f"Too few elements in {l}")

        if tokens[1] not in list(INSTRUCTIONS) + ["DATA"]:
            raise InvalidInstruction(f"Opcode not valid in {l}")

        self.process_instruction(tokens)

    def process_instruction(self, tokens):
        """Create a full instruction from the tokens."""
        label = tokens[0]
        opcode = tokens[1]
        operand = tokens[2]

        # Save the first non-data instruction as the start program counter
        if not self.start_address and opcode != "DATA":
            self.start_address = self.current_address

        if label:
            if label in self.variables:
                raise DuplicateVariable(f"Variable name {label} is already defined")
            self.variables[label] = self.current_address

        self.instructions.append(Instruction(self.current_address, opcode, operand))
        self.current_address += 1

    def assemble(self):
        """Build the bytecode string of the program."""
        self.cards = []
        for i in self.instructions:
            self.cards.append(i.card(self.variables))

        self.output = ""
        self.output += "002\n800\n"
        self.output += "".join(self.cards)
        self.output += f"002\n8{self.start_address:02}"

    def write_bytecode(self):
        """Write the output to a deck file that can be read by CARDIAC."""
        with open(self.output_filepath, "w") as fp:
            fp.write(self.output)


if __name__ == "__main__":
    a = Assembler("data/count.asm")
    c = Cardiac()
    c.read_deck(a.output_filepath)
    c.run()
