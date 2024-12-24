import re

def read_file(filename: str) -> tuple[dict[str, int], list[tuple[str,str,str,str]]]:

    wires = dict()
    gates = []
    with open(filename) as file:
        for line in file:
            if m := re.match(r"^(\w+): ([01])$", line.strip()):
                wires[m.group(1)] = int(m.group(2))
            elif m := re.match(r"^(\w+) ([A-Z]+) (\w+) -> (\w+)$", line.strip()):
                wires.setdefault(m.group(1), None)
                wires.setdefault(m.group(3), None)
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
            if wires[gate[0]] is None or wires[gate[2]] is None:
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
    print(int("".join([str(s[1]) for s in zwires]),base=2))

