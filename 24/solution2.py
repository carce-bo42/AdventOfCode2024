import re
import copy

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

def solve_gates(wires, gates):

    while len(gates) != 0:
        for gate in gates:
            if wires[gate[0]] is None or wires[gate[2]] is None:
                continue
            else:
                wires[gate[3]] = operators[gate[1]](wires, gate[0], gate[2])
                gates.remove(gate)
                break

    return wires, gates

def get_desired_result(wires):

    xwires = []
    ywires = []
    for wire, value, in wires.items():
        if wire[0] == 'x':
            xwires.append((wire,value))
        elif wire[0] == 'y':
            ywires.append((wire,value))

    xwires.sort(reverse=True)
    ywires.sort(reverse=True)
    return bin(int("".join([str(s[1]) for s in xwires]), base=2) + int("".join([str(s[1]) for s in ywires]), base=2))[2:]


def get_actual_result(wires):
    zwires = []
    for wire, value, in wires.items():
        if wire[0] == 'z':
            zwires.append((wire,value))
    zwires.sort(reverse=True)
    return "".join([str(s[1]) for s in zwires])


def compute_errors(actual_result, desired_result):
    errors = []
    for pos, char in enumerate(desired_result):
        if char != actual_result[pos]:
            errors.append(f"z{len(desired_result)-pos-1}")
    return errors

def get_candidates(wires_dict):
    candidates = []
    if "z00" in wires_dict.keys():
        del wires_dict["z00"]
    for res, op in wires_dict.items():
        if res[0] == 'z' and res[1:] != "45":
            # If zK does not come from an XOR
            if op[1] != 'XOR':
                candidates.append(res)
                continue

        # If operands in an OR dont come from an AND
        if op[1] == 'OR':
            rhs = op[0]
            lhs = op[2]
            if wires_dict[rhs][1] != 'AND':
                candidates.append(rhs)
            if wires_dict[lhs][1] != 'AND':
                candidates.append(lhs)

    print(candidates)


def get_errors(wires,gates):
    _wires, _ = solve_gates(copy.deepcopy(wires), copy.deepcopy(gates))
    desired_result = get_desired_result(_wires)
    actual_result = get_actual_result(_wires)
    print(desired_result)
    print(actual_result)
    return compute_errors(actual_result, desired_result)


def swap_wires(gates, w1, w2):
    for idx, gate in enumerate(gates):
        if gate[3] == w1:
            gates[idx] = (gate[0], gate[1], gate[2], w2)
        elif gate[3] == w2:
            gates[idx] = (gate[0], gate[1], gate[2], w1)


if __name__ == "__main__":

    wires, gates = read_file("input.txt")
    errors = get_errors(wires, gates)
    wires_dict = {gate[3] : (gate[0],gate[1],gate[2]) for gate in gates}
    # z11, z24, z38 MUST be swapped.
    # ... where ?

    # do swaps
    swap_wires(gates, "z11", "vkq")
    swap_wires(gates, "z38", "hqh")

    # These are a matter of trial and error. In the end, after swapping this
    # I get a candidate but the result coincides, so ...
    # but qdq still is weird
    # So z28 and qdq were swapped, and it worked, but it still gave a candidate
    # So I realized that qdq had to be a product of x28 and y28, because otherwise
    # qdq OR jnk -> ftq
    # Has no operands that come from an and between x28 and y28. Searched for the
    # x28 AND y28 -> pvb then swapped the definition of qdq with pvb and it worked.
    swap_wires(gates, "pvb", "qdq")
    swap_wires(gates, "z24", "mmk")
    wires_dict = {gate[3] : (gate[0],gate[1],gate[2]) for gate in gates}
    errors = get_errors(wires, gates)
    print(errors)
    lst = ["z11", "vkq", "z38", "hqh", "pvb", "qdq", "z24", "mmk"]
    lst.sort()
    print(",".join(lst))

    # svb is ok
    # jss, qwb is ok
    #

