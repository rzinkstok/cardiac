import inspect


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


class Memory(object):
    def init_mem(self, size=100):
        self.mem_size = size
        self.mem_cells = ["" for i in range(self.mem_size)]
        self.mem_set(0, "001")

    def _mem_check_address(self, address):
        try:
            address = int(address)
        except ValueError:
            raise InvalidAddress(f"Invalid address: {address}")
        if address < 0 or address > self.mem_size:
            raise MemoryOutOfRange(f"Memory address {address} out of range")
        return address

    def mem_get(self, address):
        address = self._mem_check_address(address)
        return self.mem_cells[address]

    def mem_get_int(self, address):
        return int(self.mem_get(address))

    def mem_set(self, address, data):
        address = self._mem_check_address(address)
        data = self._mem_clean_data(data)
        self.mem_cells[address] = data

    def _mem_clean_data(self, data):
        try:
            data = int(data)
        except ValueError:
            raise InvalidData("Invalid data: {data}")
        if data > 999:
            raise DataValueOverflow(f"Value overflow: {data}")

        return f"{'-'*int(data<0)}{abs(data):03}"


class CPU(object):
    def __init__(self):
        print("Init CPU")
        self.init_io()
        self.init_mem()
        self.reset()
        self.opcodes = [
            int(x[0][7:])
            for x in inspect.getmembers(self.__class__)
            if x[0].startswith("opcode_")
        ]

    def reset(self):
        self.acc = 0
        self.pc = 0
        self.ir = 0
        self.running = False

    def fetch(self):
        self.ir = self.mem_get_int(self.pc)
        self.pc += 1

    def process(self):
        self.fetch()
        opcode, arg = self.ir // 100, self.ir % 100
        if opcode not in self.opcodes:
            raise InvalidOperation(f"Opcode {opcode} not available")
        op = getattr(self, f"opcode_{opcode}")
        op(arg)

    def run(self):
        self.running = True
        while self.running:
            self.process()
            # input()


class IO(object):
    def init_io(self):
        self.input_stack = []
        self.output_stack = []

    def read_deck(self, fn):
        self.input_stack = []
        with open(fn, "r") as fp:
            for l in fp.readlines():
                data = l.strip()
                if data:
                    self.input_stack.append(data)
        self.input_stack.reverse()

    def format_output(self):
        print()
        print("OUTPUT:")
        print("-" * 60)
        print("\n".join(self.output_stack))
        print("-" * 60)

    def put_output(self, data):
        self.output_stack.append(data)

    def get_input(self):
        try:
            return self.input_stack.pop()
        except IndexError:
            raise InputExhausted("End of input")


class Cardiac(Memory, IO, CPU):
    def debug(self, opcode, arg):
        opcodes = {
            0: "INP",
            1: "CLA",
            2: "ADD",
            3: "TAC",
            4: "SFT",
            5: "OUT",
            6: "STO",
            7: "SUB",
            8: "JMP",
            9: "HRS",
        }
        print()
        print("-" * 60)
        print(f"{opcode} {opcodes[opcode]} [{arg:02}]")
        print("-" * 60)

    def debug_mem(self, display=100):
        print()
        print(f"ACC: {self.acc:04}")
        print(f"PC:  {self.pc:02}")
        print()
        print(f"MEM:")
        print("".join([f"{i:02}  " for i in range(display)]))
        print("".join([f"{x} " if x else "    " for x in self.mem_cells[:display]]))
        print()
        try:
            print(f"IN: {self.input_stack[-1]}")
        except IndexError:
            print("IN: None")
        print("OUT:")
        print(self.output_stack)

    def opcode_0(self, arg):
        self.debug(0, arg)
        inp = self.get_input()
        self.mem_set(arg, inp)
        self.debug_mem()

    def opcode_1(self, arg):
        self.debug(1, arg)
        self.acc = self.mem_get_int(arg)
        self.debug_mem()

    def opcode_2(self, arg):
        self.debug(2, arg)
        self.acc += self.mem_get_int(arg)
        self.debug_mem()

    def opcode_3(self, arg):
        self.debug(3, arg)
        if self.acc < 0:
            self.pc = arg
        self.debug_mem()

    def opcode_4(self, arg):
        self.debug(4, arg)
        l, r = arg // 10, arg % 10
        self.acc = (self.acc * pow(10, l) / pow(10, r)) % 10000

    def opcode_5(self, arg):
        self.debug(5, arg)
        self.put_output(self.mem_get(arg))
        self.debug_mem()

    def opcode_6(self, arg):
        self.debug(6, arg)
        self.mem_set(arg, self.acc)
        self.debug_mem()

    def opcode_7(self, arg):
        self.debug(7, arg)
        self.acc -= self.mem_get_int(arg)
        self.debug_mem()

    def opcode_8(self, arg):
        self.debug(8, arg)
        self.mem_set(99, 800 + self.pc)
        self.pc = arg
        self.debug_mem()

    def opcode_9(self, arg):
        self.debug(9, arg)
        self.reset()
        self.pc = arg
        self.debug_mem()


if __name__ == "__main__":
    c = Cardiac()
    c.read_deck("deck5.txt")
    c.debug_mem()
    c.run()
    c.format_output()
