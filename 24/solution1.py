import re

def read_file(filename: str) -> tuple[dict[str, int], list[tuple[str,str,str,str]]]:

    wires = dict()
    gates = []
    with open(filename) as file:
        for line in file:
            if m := re.match(r"^(\w+): ([01])$", line.strip()):
                wires[m.group(1)] = int(m.group(2))
            elif m := re.match(r"^(\w+) ([A-Z]+) (\w+) -> (\w+)$", line.strip()):
                wires.setdefault(m.group(1), -1)
                wires.setdefault(m.group(3), -1)
                gates.append((m.group(1),m.group(2),m.group(3),m.group(4)))

    return wires, gates

def AND(wires: dict[str, int], lhs: str, rhs: str) -> int:
    return wires[lhs] & wires[rhs]

def OR(wires: dict[str, int], lhs: str, rhs: str) -> int:
    return wires[lhs] | wires[rhs]

def XOR(wires: dict[str, int], lhs: str, rhs: str) -> int:
    return wires[lhs] ^ wires[rhs]

operators = {
    'AND' : AND,
    'XOR' : XOR,
    'OR' : OR,
}

if __name__ == "__main__":

    wires, gates = read_file("input.txt")

    while len(gates) != 0:
        for gate in gates:
            if wires[gate[0]] == -1 or wires[gate[2]] == -1:
                continue
            else:
                wires[gate[3]] = operators[gate[1]](wires, gate[0], gate[2])
                gates.remove(gate)
                break
    zwires = []
    for wire, value, in wires.items():
        if wire[0] == 'z':
            zwires.append((wire,value))
    zwires.sort(reverse=True)
    result_str = "".join([str(s[1]) for s in zwires])
    result = int(result_str,base=2)
    print(result)

