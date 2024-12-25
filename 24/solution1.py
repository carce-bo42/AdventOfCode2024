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
    xwires = []
    ywires = []
    for wire, value, in wires.items():
        if wire[0] == 'z':
            zwires.append((wire,value))
        elif wire[0] == 'x':
            xwires.append((wire,value))
        elif wire[0] == 'y':
            ywires.append((wire,value))

    zwires.sort(reverse=True)
    xwires.sort(reverse=True)
    ywires.sort(reverse=True)
    xbin = "0" + "".join([str(s[1]) for s in xwires])
    ybin = "0" + "".join([str(s[1]) for s in ywires])
    zbin = "".join([str(s[1]) for s in zwires])
    result = int(xbin, base=2) + int(ybin, base=2)
    result_str = bin(result)[2:]
    for pos, char in enumerate(result_str):
        if char != zbin[pos]:
            print(f"z{len(result_str)-(pos+1)} is wrong")

    print(f"zbin = {zbin}")
    print(f"res  = {result_str}")
