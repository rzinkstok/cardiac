import inspect
import re

# Exception classes
class MemoryOutOfRange(Exception):
    pass


class InvalidAddress(Exception):
    pass


class InvalidData(Exception):
    pass


class DataValueOverflow(Exception):
    pass


class InputExhausted(Exception):
    pass


class InvalidOperation(Exception):
    pass


# CARDIAC part classes
class Memory(object):
    """Simple memory object for decimal words. The words hold decimal numbers between -999 and 999.

    Args:
        size (int): the number of words (cells) the memory can hold.
    """

    def __init__(self, size=100):
        super(Memory, self).__init__()
        self.mem_size = size
        self.mem_cells = ["" for i in range(self.mem_size)]
        self.mem_set(0, "001")

    def _mem_check_address(self, address):
        """Check whether the argument is a valid memory address."""
        try:
            address = int(address)
        except ValueError:
            raise InvalidAddress(f"Invalid address: {address}")
        if address < 0 or address > self.mem_size:
            raise MemoryOutOfRange(f"Memory address {address} out of range")
        return address

    def mem_get(self, address):
        """Get the content of the memory cell with the given address."""
        address = self._mem_check_address(address)
        return self.mem_cells[address]

    def mem_get_int(self, address):
        """Get the content of the memory cell with the given address as an int."""
        return int(self.mem_get(address))

    def mem_set(self, address, data):
        """Set the content of the memory cell with the given address to the given data."""
        address = self._mem_check_address(address)
        data = self._mem_clean_data(data)
        self.mem_cells[address] = data

    def _mem_clean_data(self, data):
        """Process the data before insertion."""
        try:
            data = int(data)
        except ValueError:
            raise InvalidData("Invalid data: {data}")
        if data > 999:
            raise DataValueOverflow(f"Value overflow: {data}")

        return f"{'-'*int(data<0)}{abs(data):03}"


class IO(object):
    """Simple input/output class."""

    def __init__(self):
        super(IO, self).__init__()
        self.input_stack = []
        self.output_stack = []

    def read_deck(self, fn):
        """Read a card deck from file into the input stack."""
        self.input_stack = []
        with open(fn, "r") as fp:
            for l in fp.readlines():
                data = l.strip()
                if data:
                    self.input_stack.append(data)
        self.input_stack.reverse()

    def flush_output(self):
        """Flush the output stack to stdout."""
        # print()
        # print("OUTPUT:")
        # print("-" * 60)
        print("\n".join(self.output_stack))
        # print("-" * 60)

    def put_output(self, data):
        """Put the given data on the output stack."""
        self.output_stack.append(data)

    def get_input(self):
        """Retrieve the next item from the input stack."""
        try:
            return self.input_stack.pop()
        except IndexError:
            raise InputExhausted("End of input")


class CPU(object):
    """CPU implementation."""

    def __init__(self):
        super(CPU, self).__init__()
        self.reset()

    def gather_instructions(self):
        """Retrieves all methods that implement instructions and collects them in a dict.

        Any member functions whose name conforms to 'opcode_<opcode>_<alias>' are included.
        E.g. 'opcode_0_cla' will be included with opcode 0 and alias 'cla'.
        """
        self.opcodes = {}
        for x in inspect.getmembers(self):
            if re.search("opcode\_\d\_[a-z]+", x[0]):
                parts = x[0].split("_")
                self.opcodes[int(parts[1])] = parts[2]

    @property
    def instructions(self):
        """Return a tuple of all available instructions sorted by opcode."""
        return tuple(self.opcodes[x].upper() for x in sorted(self.opcodes.keys()))

    def reset(self):
        """Reset registers and program counter."""
        self.acc = 0
        self.pc = 0
        self.ir = 0
        self.running = False

    def fetch(self):
        """Fetch the next instruction into the instruction register and advance the program counter."""
        self.ir = self.mem_get_int(self.pc)
        self.pc += 1

    def process(self):
        """Fetch and process the next instruction."""
        self.fetch()
        opcode, arg = self.ir // 100, self.ir % 100
        if opcode not in self.opcodes:
            raise InvalidOperation(f"Opcode {opcode} not available")

        # Build the method name for the opcode
        opname = f"opcode_{opcode}"
        if self.opcodes[opcode]:
            opname += f"_{self.opcodes[opcode]}"
        op = getattr(self, opname)

        # Execute
        op(arg)


# Main CARDIAC class
class Cardiac(Memory, IO, CPU):
    """CARDIAC computer implementation.

    Args:
        verbose (bool): whether to print debugging info for each cycle.
    """

    def __init__(self, verbose=False):
        super(Cardiac, self).__init__()
        self.opcodes = {}
        self.gather_instructions()
        self.verbose = verbose

    def debug(func):
        """Decorator to be used for opcode methods. Will cause debug info to be printed."""
        opcode = int(func.__name__.split("_")[1])

        def debug_wrapper(self, arg):
            if self.verbose:
                print("=" * 60)
                print()
                print("-" * 10)
                print(f"{opcode} {self.opcodes[opcode].upper()} [{arg:02}]")
                print("-" * 10)

            res = func(self, arg)

            if self.verbose:
                print()
                print(f"ACC: {self.acc:04}")
                print(f"PC:  {self.pc:02}")
                print()
                print(f"MEM:")
                print("".join([f" {i:02}  " for i in range(self.mem_size)]))
                print("".join([f"{x}  " if x else "     " for x in self.mem_cells]))
                print()
                try:
                    print(f"NEXT IN: {self.input_stack[-1]}")
                except IndexError:
                    print("NEXT IN: None")
                print("OUT:")
                print(self.output_stack)
                print()

            return res

        return debug_wrapper

    @debug
    def opcode_0_inp(self, arg):
        inp = self.get_input()
        self.mem_set(arg, inp)

    @debug
    def opcode_1_cla(self, arg):
        self.acc = self.mem_get_int(arg)

    @debug
    def opcode_2_add(self, arg):
        self.acc += self.mem_get_int(arg)

    @debug
    def opcode_3_tac(self, arg):
        if self.acc < 0:
            self.pc = arg

    @debug
    def opcode_4_sft(self, arg):
        l, r = arg // 10, arg % 10
        self.acc = (self.acc * pow(10, l) / pow(10, r)) % 10000

    @debug
    def opcode_5_out(self, arg):
        self.put_output(self.mem_get(arg))

    @debug
    def opcode_6_sto(self, arg):
        self.mem_set(arg, self.acc)

    @debug
    def opcode_7_sub(self, arg):
        self.acc -= self.mem_get_int(arg)

    @debug
    def opcode_8_jmp(self, arg):
        self.mem_set(99, 800 + self.pc)
        self.pc = arg

    @debug
    def opcode_9_hrs(self, arg):
        self.reset()
        self.pc = arg

    def run(self):
        """Start the computer and run the program loaded, if any."""
        self.running = True
        while self.running:
            try:
                self.process()
            except InputExhausted:
                self.reset()
        self.flush_output()


if __name__ == "__main__":
    c = Cardiac()
    c.read_deck("data/count2.cdc")
    c.run()
