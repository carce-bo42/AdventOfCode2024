from heapq import heapify, heappop, heappush
from colorama import Fore, Style

class _Map:

    X_LEN = 142
    Y_LEN = 142

    def __init__(self, x_len = X_LEN, y_len = Y_LEN):
        self.x_len = x_len
        self.y_len = y_len
        self._map = [['.'] * x_len for _ in range(y_len)]

    def __getitem__(self, indices):
        x, y = indices
        return self._map[y][x]

    def __setitem__(self, indices, value):
        x, y = indices
        self._map[y][x] = value

    def __repr__(self):
        # Generate rows as strings with ">" in a different color
        rows_as_strings = [
            " ".join(
                Fore.RED + str(cell) + Style.RESET_ALL if cell in ">^<v" else str(cell)
                for cell in row
            )
            for row in self._map
        ]
        return "\n".join(rows_as_strings)


ROUTING = {
    # current direction: tuple[(dx,dy), next direction, cost)]
    "^": ( ((0,-1), "^", 1   ), ((1, 0), ">", 1001), ((0,1), "v", 1002), ((-1,0), "<", 1001)),
    ">": ( ((0,-1), "^", 1001), ((1, 0), ">", 1   ), ((0,1), "v", 1001), ((-1,0), "<", 1002)),
    "v": ( ((0,-1), "^", 1002), ((1, 0), ">", 1001), ((0,1), "v", 1   ), ((-1,0), "<", 1001)),
    "<": ( ((0,-1), "^", 1001), ((1, 0), ">", 1002), ((0,1), "v", 1001), ((-1,0), "<", 1   ))
}


def dijkstra(points: set[(int,int)], source: tuple[int,int] ) -> dict[(int,int) : int]:

    distances = { source : 0 }
    pq = [(0, source, ">")]
    heapify(pq)

    while pq:

        current_cost, current_node, current_direction = heappop(pq)
        if distances[current_node] < current_cost:
            continue

        for vector, direction, cost in ROUTING[current_direction]:
            neighbor = (current_node[0] + vector[0], current_node[1] + vector[1])
            if neighbor in points:
                new_dist = current_cost + cost
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(pq, (new_dist, neighbor, direction))

    predecessors = {node: None for node in points}

    # Get list of predecessors
    for node, distance in distances.items():
        for vector, direction, cost in ROUTING[current_direction]:
            neighbor = (node[0] + vector[0], node[1] + vector[1])
            if neighbor in points:
                if distances[neighbor] == distance + cost:
                    predecessors[neighbor] = (node, direction)

    return distances, predecessors

def read_file(filename: str):

    points = set()
    _map = _Map()
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line):

                _map[x,y] = char
                if char == '#':
                    continue

                points.add((x,y))

                if char == 'S':
                    start = (x,y)

                if char == 'E':
                    end = (x,y)

    return _map, points, start, end

if __name__ == "__main__":
    _map, points, start, end = read_file("input.txt")
    distances, predecessors = dijkstra(points, start)
    print(distances[end])
    print(predecessors)

    # node = (end, ">")
    # while node[0] != start:
    #     _map[*node[0]] = node[1]
    #     node = predecessors[*node[0]]
