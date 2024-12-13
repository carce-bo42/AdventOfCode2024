import re

def vectors_are_linearly_dependent(vA, vB):

    return vA[0] / vB[0] == vA[1] / vB[1]

def division_is_ok(up_term, down_term):

    # Si no son enteros divisibles, no es una cantidad realista
    # de veces que hay que apretar un boton
    if up_term % down_term != 0:
        return False

    # Si alguno de los dos terminos es negativo
    if up_term * down_term < 0:
        return False

    return True

def solve_problem(vA, vB, P):

    if vectors_are_linearly_dependent(vA, vB):
        if P[0] % vB[0] == 0:
            return 0, int(P[0]/vB[0])
        else:
            return -1, -1

    up_term = vB[0]*P[1] - vB[1]*P[0]
    down_term = vB[0]*vA[1] - vB[1]*vA[0]

    if not division_is_ok(up_term, down_term):
        return -1, -1

    x_press = int(up_term / down_term)

    up_term = (P[0]-vA[0]*x_press)
    down_term = vB[0]

    if not division_is_ok(up_term, down_term):
        return -1, -1

    y_press = int(up_term/down_term)

    return x_press, y_press


fname = "input.txt"
tokens = 0
with open(fname) as file:
    vA = ()
    vB = ()
    P = ()
    for line in file:

        sline = line.strip()

        m = re.match(r"Button A: X\+(\d+), Y\+(\d+)", sline)
        if m is not None:
            vA = (int(m.group(1)), int(m.group(2)))
            continue

        m = re.match(r"Button B: X\+(\d+), Y\+(\d+)",sline)
        if m is not None:
            vB = (int(m.group(1)), int(m.group(2)))
            continue

        m = re.match(r"Prize: X=(\d+), Y=(\d+)", sline)
        if m is not None:
            P = (int(m.group(1))+10000000000000, int(m.group(2))+10000000000000)

        if len(vA) == len(vB) == len(P) == 2:
            a_button, b_button = solve_problem(vA, vB, P)
            if a_button != -1:
                tokens += a_button * 3 + b_button * 1
            vA = vB = P = ()

print(tokens)