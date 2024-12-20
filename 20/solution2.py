from heapq import heapify, heappop, heappush
from itertools import combinations

# I learned dijsktra with this program.
# sources: https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python
# https://rosettacode.org/wiki/Maze_solving#Python

DIRECTIONS = {
    (1, 0),
    (0, 1),
    (-1,0),
    (0,-1),
}

def dijkstra(points: set[(int,int)], source: tuple[int,int] ) -> dict[(int,int) : int]:

    distances = { source : 0 }
    pq = [(0, source)]
    heapify(pq)

    while pq:
        current_distance, current_node = heappop(pq)
        if distances[current_node] < current_distance:
            continue
        for dir in DIRECTIONS:
            neighbor = (current_node[0] + dir[0], current_node[1] + dir[1])
            if neighbor in points:
                new_dist = current_distance + 1
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(pq, (new_dist, neighbor))

    return distances


def get_cheats_generic(distances: dict[(int,int):int], jump_size: int):

    cheats = 0
    for src, dst in combinations(distances, 2):
        point_distance = abs(dst[0]-src[0]) + abs(dst[1]-src[1])
        physical_distance = distances[dst] - distances[src]
        if point_distance <= jump_size and (physical_distance - point_distance) >= 100:
            cheats += 1
    return cheats


def read_file(filename: str):

    points = set()
    walls = set()
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line):
                if char == '#':
                    walls.add((x,y))
                    continue

                points.add((x,y))

                if char == 'S':
                    start = (x,y)

                if char == 'E':
                    end = (x,y)

    return points, walls, start, end


if __name__ == "__main__":

    points, walls, start, end = read_file("input.txt")
    distances = dijkstra(points, start)

    print(get_cheats_generic(distances, 20))