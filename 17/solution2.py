import re

class HistorianComputer:

    def __init__(self, rA: int, rB: int, rC: int):

        self.rA = rA
        self.rB = rB
        self.rC = rC
        self.opcodes = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv
        ]
        self.buf = ""

    def execute_program(self, instructions: list[int]):

        # instruction pointer.
        self.ip = 0
        self.save_rA = self.rA

        while self.ip < len(instructions):
            opcode = instructions[self.ip]
            operand = instructions[self.ip+1]
            self.opcodes[opcode](operand)

        return self.buf[:-1]

    def combo_operand(self, operand: int):
        return operand if operand < 4 else [self.rA, self.rB, self.rC][operand%4]

    def adv(self, operand: int):
        self.rA = int(self.rA / (2**self.combo_operand(operand)))
        self.ip += 2

    def bxl(self, operand: int):
        self.rB = self.rB ^ operand
        self.ip += 2

    def bst(self, operand: int):
        self.rB = self.combo_operand(operand)%8
        self.ip += 2

    def jnz(self, operand: int):
        if self.rA == 0:
            self.ip += 2
        else:
            self.ip = operand

    def bxc(self, operand: int):
        self.rB = self.rB ^ self.rC
        self.ip += 2

    def out(self, operand: int):
        self.buf += f"{self.combo_operand(operand)%8},"
        self.ip += 2

    def bdv(self, operand: int):
        self.rB = int(self.rA / (2**self.combo_operand(operand)))
        self.ip += 2

    def cdv(self, operand: int):
        self.rC = int(self.rA / (2**self.combo_operand(operand)))
        self.ip += 2


def read_file(filename: str):

    patterns = {
        r"Register A: (\d+)": lambda m: int(m.group(1)),
        r"Register B: (\d+)": lambda m: int(m.group(1)),
        r"Register C: (\d+)": lambda m: int(m.group(1)),
        r"Program: (.*)": lambda m: list(map(int, m.group(1).split(",")))
    }

    with open(filename) as file:
        results = []
        for line in file:
            sline = line.strip()
            for pattern, action in patterns.items():
                if m := re.match(pattern, sline):
                    results.append(action(m))

        return results


def nth_rightmost_bits(num, n=1, bits=3):
    mask = (1 << (bits*n)) - 1
    rightmost = num & mask
    return bin(rightmost)[2:].zfill(bits)


def get_magic_number(rA: list[int], instructions: list[int], digit: int = 0) -> list[int]:

    if len(instructions) == digit:
        return [v >> 3 for v in rA]

    solution = []
    # for bits in 000 001 010 011 100 101 110 111
    for base in rA:
        for bits in range(0,8):
            _rA = base + bits
            computer = HistorianComputer(_rA, 0, 0)
            buf = computer.execute_program(instructions)
            if int(buf[0]) == instructions[-(digit+1)]:
                solution.append(_rA << 3)

    return get_magic_number(solution, instructions, digit + 1)


if __name__ == "__main__":

    _, _, _, instructions = read_file("input.txt")
    solutions = get_magic_number([0], instructions)
    print(f"{solutions}, min = {min(solutions)}")
