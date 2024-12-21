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

def dijkstra(
        points: set[ tuple[int,int] ],
        source: tuple[int,int]
    ) -> tuple[ dict[tuple[int,int] : int], dict[tuple[int,int] : list[tuple[int,int]]]]:

    distances = { source : 0 }
    pq = [(0, source)]
    heapify(pq)

    while pq:
        current_distance, current_node = heappop(pq)
        if distances[current_node] < current_distance:
            continue
        for dir in [(1,0), (0,1), (-1,0), (0,-1)]:
            neighbor = (current_node[0] + dir[0], current_node[1] + dir[1])
            if neighbor in points:
                new_dist = current_distance + 1
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(pq, (new_dist, neighbor))

    predecessors = {node: [] for node in points}
    for node, distance in distances.items():
        for dir in [(1,0), (0,1), (-1,0), (0,-1)]:
            neighbor = (node[0] + dir[0], node[1] + dir[1])
            if neighbor in points:
                if distances[neighbor] == distance + 1:
                    predecessors[neighbor].append(node)

    return distances, predecessors


def build_possible_paths(
        predecessors: dict[tuple[int,int] : list[tuple[int,int]]],
    ) -> list[dict[tuple[int,int] : tuple[int,int]]]:

    result = []
    print([[(key, value) for value in values] for key, values in predecessors.items()])
    for combination in product(*[[(key, value) for value in values] for key, values in predecessors.items()]):
        result.append({key: value for key, value in combination})
    return result

# We dissasemble the moves from the end to the start
def get_moves_from_route(
        predecessors: dict[tuple[int,int] : tuple[int,int]],
        src: tuple[int, int],
        dst: tuple[int,int]
    ) -> str:

    current = dst
    moves = ""
    while current != src:
        previous = predecessors[current]
        # if (0,1) -> (0,2).
        # previous = (0,1). current = (0,2).
        # v = (0, 1) => '>'.
        v = ((current[0] - previous[0]), current[1] - previous[1])
        moves += DIRECTIONS[v]
        current = previous

    return moves[::-1]+"A"

def get_keyboard_moves(sequence: str, keyboard: dict[str : tuple[int,int]]) -> str:

    start = keyboard['A']
    points = keyboard.values()
    moves = ""
    #for char in sequence:
    _, predecessors = dijkstra(points, start)
    print(build_possible_paths(predecessors))
        #moves += get_moves_from_route(predecessors, start, keyboard[char])
        #start = keyboard[char]

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

    password_codes = read_file("input.test.txt")
    moves = get_keyboard_moves(password_codes[0], PASSWORD_KEYBOARD)
    # moves = get_keyboard_moves(moves, CONTROL_KEYBOARD)