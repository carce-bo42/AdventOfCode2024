from heapq import heapify, heappop, heappush
from colorama import Fore, Style
from collections import deque

class _Map:

    # X_LEN = 18
    # Y_LEN = 18
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
                Fore.RED + str(cell) + Style.RESET_ALL if cell in "O" else str(cell)
                for cell in row
            )
            for row in self._map
        ]
        return "\n".join(rows_as_strings)

ROUTING = {
    # current direction: tuple[(dx,dy), next direction, cost)]
    "^": ( ((0,-1), "^", 1   ), ((1, 0), ">", 1001), ((-1,0), "<", 1001)),
    ">": ( ((0,-1), "^", 1001), ((1, 0), ">", 1   ), ((0,1), "v", 1001)),
    "v": ( ((1, 0), ">", 1001), ((0,1), "v", 1   ), ((-1,0), "<", 1001)),
    "<": ( ((0,-1), "^", 1001), ((0,1), "v", 1001), ((-1,0), "<", 1   ))
}

DIRECTIONS = {
    (0,1),
    (0,-1),
    (1,0),
    (-1,0)
}

def dijkstra(points: set[(int,int)], source: tuple[int,int] ) -> dict[(int,int) : int]:

    distances = { source : (0, ">") }
    predecessors = {source: None}

    pq = [(0, source)]
    heapify(pq)

    while pq:

        current_cost, current_node = heappop(pq)
        if distances[current_node][0] < current_cost:
            continue

        _, current_direction = distances[current_node]

        for vector, direction, cost in ROUTING[current_direction]:
            neighbor = (current_node[0] + vector[0], current_node[1] + vector[1])
            if neighbor in points:
                new_dist = current_cost + cost
                if neighbor not in distances or new_dist < distances[neighbor][0]:
                    distances[neighbor] = (new_dist, direction)
                    predecessors[neighbor] = (current_node, direction)
                    heappush(pq, (new_dist, neighbor))

    return distances, predecessors

# Esto te encuentra el camino optimo recorrido.
# Hay que buscar aqui, que bifurcaciones tienen un coste equivalente.
# como se hace esto ? ... who the fuck knows
def find_optimal_path(
        distances: dict[tuple[int,int] : int],
        end: tuple[int,int],
        _map
    ) -> int:

    queue = deque()
    visited = set()

    max_distance_allowed = distances[end]
    current_min_score = 1000000000

    sits = 1
    queue.append(end)

    while queue:
        node = queue.popleft()
        x, y = node
        current_score = distances[node]

        for dx,dy in DIRECTIONS:
            neighbor = (x+dx,y+dy)
            if neighbor in visited or neighbor not in distances:
                continue

            score = distances[neighbor]
            if score > max_distance_allowed:
                continue

            score_diff = current_score - score
            if score_diff in [1, 1001]:
                sits += 1
                visited.add(neighbor)
                queue.append(neighbor)
                _map[*node] = 'O'
                if current_min_score > score:
                    current_min_score = score

    return sits, visited


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
    sits, visited = find_optimal_path({point : distances[point][0] for point in distances.keys()}, end, _map)
    print(sits)
    #print(_map)
    # for y in range(0,_map.y_len-1):
    #     for x in range(0, _map.x_len-1):
    #         if (x,y) in distances:
    #             print(f"{distances[(x,y)][0]:5}", end=" ")
    #         else:
    #             print("    #",end=" ")
    #     print()