import re
from heapq import heapify, heappop, heappush
from colorama import Fore, Style

# I learned dijsktra with this program.
# sources: https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python
# https://rosettacode.org/wiki/Maze_solving#Python

DIRECTIONS = {
    (1, 0),
    (0, 1),
    (-1,0),
    (0,-1),
}

def read_file(filename, max_len):

    falling_bytes = []

    with open(filename) as file:
        results = []
        for line in file:
            if m := re.match(r"(\d+),(\d+)", line.strip()):
                falling_bytes.append((int(m.group(1)),int(m.group(2))))

    grid_points = ((x, y) for x in range(0,max_len+1) for y in range(0,max_len+1))
    points = {(x,y) for x, y in grid_points if (x,y) not in falling_bytes[:1024]}

    return points, falling_bytes

def dijkstra(points: set[(int,int)], source: tuple[(int,int)] ):

    # Unknown distance function from source to any != source
    distances = {node: float("inf") for node in points}

    # Set the source value to 0
    distances[source] = 0

    # Create the priority queue.
    pq = [(0, source)]
    heapify(pq)

    # Previously visited nodes.
    visited = set()

    while pq:

        # Get the node with the min distance
        current_distance, current_node = heappop(pq)

        # If a node has been visited, do not compute again the distances
        # with respect its neighbours.
        if current_node in visited:
            continue
        visited.add(current_node)

        for dir in DIRECTIONS:
            neighbor = (current_node[0] + dir[0], current_node[1] + dir[1])
            if neighbor in points:
                # For each neighbour, compute the acumulated distance.
                # the weight is 1 for all points.
                new_dist = current_distance + 1
                # push it to the heap to check in case it is
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(pq, (new_dist, neighbor))

    predecessors = {node: None for node in points}

    # Get list of predecessors
    for node, distance in distances.items():
        for dir in DIRECTIONS:
            neighbor = (node[0] + dir[0], node[1] + dir[1])
            if neighbor in points:
                if distances[neighbor] == distance + 1:
                    predecessors[neighbor] = node

    return distances, predecessors

class _Map:

    X_LEN = 71
    Y_LEN = 71

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
        # Generate rows as strings with "#" in a different color
        rows_as_strings = [
            " ".join(
                Fore.RED + str(cell) + Style.RESET_ALL if cell == "#" else str(cell)
                for cell in row
            )
            for row in self._map
        ]
        return "\n".join(rows_as_strings)

if __name__ == "__main__":

    points, falling_bytes = read_file("input.txt", 70)
    assert len(points) == 71*71 - 1024

    distances, predecessors = dijkstra(points, (0,0))
    print(distances[(70,70)])

    _map = _Map()
    for (x,y) in falling_bytes[:1024]:
        _map[x,y] = 'O'

    node = (70,70)
    while node != (0,0):
        _map[*node] = '#'
        node = predecessors[node]

    # Show solution
    print(_map)

