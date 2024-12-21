from heapq import heapify, heappop, heappush
from itertools import product

PASSWORD_KEYBOARD = {
    '7' : (0,0), '8' : (1,0), '9' : (2,0),
    '4' : (0,1), '5' : (1,1), '6' : (2,1),
    '1' : (0,2), '2' : (1,2), '3' : (2,2),
                 '0' : (1,3), 'A' : (2,3),
}

CONTROL_KEYBOARD = {
                 '^' : (1,0), 'A' : (2,0),
    '<' : (0,1), 'v' : (1,1), '>' : (2,1)
}

DIRECTIONS = {
    (0,-1) : '^',
    (1,0) : '>',
    (0,1) : 'v',
    (-1,0) : '<',
}

# We dissasemble the moves from the end to the start
def get_moves_from_route(
        sequence: list[tuple[int,int]],
    ) -> str:

    moves = ""
    current = sequence[0]
    for next_tile in sequence[1:]:
        # if (0,1) -> (0,2).
        # previous = (0,1). current = (0,2).
        # v = (0, 1) => '>'.
        v = ((next_tile[0] - current[0]), next_tile[1] - current[1])
        moves += DIRECTIONS[v]
        current = next_tile

    return moves+"A"


def add_moves_to_sequence(
        src: tuple[int, int],
        delta: int,
        axis: str,
        sequence: list[tuple[int, int]]
    ) -> None:

    if delta != 0:
        step = 1 if delta > 0 else -1
        if axis == 'x':
            for x in range(src[0] + step, src[0] + delta + step, step):
                sequence.append((x, src[1]))
        elif axis == 'y':
            for y in range(src[1] + step, src[1] + delta + step, step):
                sequence.append((src[0], y))

# So, going up is very costly because we need to start the arm that
# controls the robot by going left to press the ^  button, and that
# apparently was a problem ?
# I started with the order in this function being switched, saw some cases,
# ended up leaving it like this and the examples worked.
def get_best_path(
        points: set[tuple[int,int]],
        src: tuple[int,int],
        dst: tuple[int,int],
    ) -> dict[tuple[int,int] : tuple[int,int]]:

    sequence = [src]
    dx, dy = (dst[0]-src[0], dst[1]-src[1])
    if (src[0]+dx, src[1]) in points:
        add_moves_to_sequence(src, dx, 'x', sequence)
        new_src = sequence[-1]
        add_moves_to_sequence(new_src, dy, 'y', sequence)
    else:
        add_moves_to_sequence(src, dy, 'y', sequence)
        new_src = sequence[-1]
        add_moves_to_sequence(new_src, dx, 'x', sequence)

    return sequence


def get_keyboard_moves(sequence: str, keyboard: dict[str : tuple[int,int]]) -> str:

    start = keyboard['A']
    points = keyboard.values()
    moves = ""
    for char in sequence:
        path = get_best_path(points, start, keyboard[char])
        moves += get_moves_from_route(path)
        start = keyboard[char]

    return moves


def read_file(filename: str) -> list[str]:

    password_codes = []
    with open(filename) as file:
        for line in file:
            password_codes.append(line.strip())

    return password_codes

# 029A: <A^A>^^AvvvA, <A^A^>^AvvvA, and <A^A^^>AvvvA.
# 029A 1: v<<A>>^A<A>AvA<^AA>A<vAAA>^A
if __name__ == "__main__":

    password_codes = read_file("input.txt")
    complexity = 0
    for pwd in password_codes:
        moves = get_keyboard_moves(pwd, PASSWORD_KEYBOARD)
        print(moves)
        moves = get_keyboard_moves(moves, CONTROL_KEYBOARD)
        print(moves)
        moves = get_keyboard_moves(moves, CONTROL_KEYBOARD)
        print(moves)
        print(len(moves),int(pwd[:-1]))
        complexity += len(moves)*int(pwd[:-1])

    print(complexity)