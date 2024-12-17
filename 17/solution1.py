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
            # print(f"ip={self.ip}, opcode={opcode}, operand={operand}")
            self.opcodes[opcode](operand)

        #print(f"output={self.buf[:-1]}    rA_ini={self.save_rA}")
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


def read_file(filename):

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


# What is the relation between whats printed and rA ?
# I would try to give a mathematical justification, but its just
# empirically that I checked this:
# This does never ever print a dictionary that is not 1 to 1 mapped.
# All bits correspond to a value, and that is it.
    # rA = 30886136
    # bits = rA & 0b111
    # results = {}
    # for i in range(0,6791627991):
    #     bits = (rA+i) & 0b111
    #     #print (f"bits={bits:03b}")
    #     computer = HistorianComputer(rA+i, rB, rC)
    #     buf = computer.execute_program(instructions)
    #     results.setdefault(bits, buf[0])
    #     print(results)
#
# The first 3 bits are for the first printed number
# The second 3 bits are for the second printed number
# Etc.
# (n >> 0) & 0b111 => 3 rightmost bits
# (n >> 1) & 0b111 => 3 second rightmost bits
# (n >> M) & 0b111 => 3 M+1'st rightmost bits

if __name__ == "__main__":

    rA, rB, rC, instructions = read_file("input.txt")
    digit = 0
    rA = 281474976710655
    # while digit < 2:

    #     for bits in range(0,8):

    #         bits = bits << (3*digit)

    #         computer = HistorianComputer(rA + bits, rB, rC)
    #         buf = computer.execute_program(instructions)
    #         print(buf)
    #         if (digit*2) < len(buf) and int(buf[digit*2]) == instructions[digit]:
    #             rA = bits

    #     digit += 1

    for bits in range(0,32):

        computer = HistorianComputer(rA - bits, rB, rC)
        buf = computer.execute_program(instructions)
        print(bits)
        print(buf)
        if (digit*2) < len(buf) and int(buf[digit*2]) == instructions[digit]:
            pass

