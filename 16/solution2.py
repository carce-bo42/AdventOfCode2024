from collections import deque
from heapq import heapify, heappop, heappush

ROUTING = {
    # current direction: tuple[(dx,dy), next direction, cost)]
    "^": ( ((0,-1), "^", 1   ), ((1,0), ">", 1001), ((-1,0), "<", 1001)),
    ">": ( ((0,-1), "^", 1001), ((1,0), ">", 1   ), (( 0,1), "v", 1001)),
    "v": ( ((1, 0), ">", 1001), ((0,1), "v", 1   ), ((-1,0), "<", 1001)),
    "<": ( ((0,-1), "^", 1001), ((0,1), "v", 1001), ((-1,0), "<", 1   ))
}

DIRECTIONS = {
    ">" : (1,0),
    "v" : (0,1),
    ">" : (-1,0),
    "^" : (0,-1)
}

def backwards_bfs(end: tuple[int,int], distances: dict[tuple[int,int], int]):
    queue = deque()
    res = 1
    start = (*end, distances[end][0], "<")  # x, y, score, direction
    queue.append(start)
    visited = set()

    while queue:
        cur_x, cur_y, cur_score, cur_dir = queue.popleft()

        allowed_directions_n_score = []
        for vec, dir, score in ROUTING[cur_dir]:
            allowed_directions_n_score.append((vec, dir, cur_score - score))

        for new_vec, new_dir, new_score in allowed_directions_n_score:
            neighbor = (cur_x + new_vec[0], cur_y + new_vec[1])
            if neighbor in distances \
                and (distances[neighbor][0] in [new_score, new_score - 1000]) \
                    and neighbor not in visited:
                res += 1
                queue.append((*neighbor, new_score, new_dir))
                visited.add(neighbor)

    return res

def dijkstra(points: set[(int,int)], source: tuple[int,int] ) -> dict[(int,int) : int]:

    distances = { source : (0, ">") }

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
                    heappush(pq, (new_dist, neighbor))

    return distances


def read_file(filename: str):

    points = set()
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line):

                if char == '#':
                    continue

                points.add((x,y))

                if char == 'S':
                    start = (x,y)

                if char == 'E':
                    end = (x,y)

    return points, start, end


if __name__ == "__main__":
    points, start, end = read_file("input.txt")
    distances = dijkstra(points, start)
    print(backwards_bfs(end, distances))
