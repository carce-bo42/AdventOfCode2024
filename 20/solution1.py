from heapq import heapify, heappop, heappush

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

    distances = {node: float("inf") for node in points}
    distances[source] = 0
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
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(pq, (new_dist, neighbor))

    return distances


# Walls that, if taken out, would potentially make a difference are those that
# 1. Are not on the edges.
# 2. Are surrounded by 2 walls and are not a corner.
# 3. If they are on a corner, there is a special case in which taking it out
#    could bring improvements to the path:
#              .#..        .#..
#            ...###       ...##
#            ###...   => ###..
#              #..         #..
# 4. Theres an argument about how a wall only surrounded by another wall is
#    useless to take out in order to save 100 seconds.
def filter_walls(walls: set[(int,int)]) -> set[(int,int)]:

    x_edge, y_edge = max(walls)
    candidates = set()

    for x, y in walls:
        if x == 0 or x == x_edge or y == 0 or y == y_edge:
            continue

        walls_around = []
        for dx, dy in DIRECTIONS:
            if (x+dx,y+dy) in walls:
                walls_around.append((dx,dy))

        if len(walls_around) > 2:
            continue

        if len(walls_around) == 1:
            candidates.add((x,y))
            continue

        # dx1 == dx2 ---> dx == 0 ---> aligned
        if walls_around[0][0] == walls_around[1][0]:
            candidates.add((x,y))
        # dy1 == dy2 ---> dy == 0 ---> aligned
        elif walls_around[0][1] == walls_around[1][1]:
            candidates.add((x,y))
        # The corner case. Theres math here.
        else:
            dx = walls_around[0][0] + walls_around[1][0]
            dy = walls_around[0][1] + walls_around[1][1]
            if (-dx,-dy) in walls:
                candidates.add((x,y))

    return candidates


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
    min_time = distances[end]

    walls = filter_walls(walls)
    cheats = {}
    count = 0
    for wall in walls:
        points.add(wall)
        distances = dijkstra(points, start)
        if min_time - distances[end] >= 100:
            count += 1
        points.remove(wall)
    print(count)

