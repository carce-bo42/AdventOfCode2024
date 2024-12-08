def dump_map():
    for i in range(0, len(_map)):
        print("".join(_map[i]))

def point_in_bounds(x, y):
    return x >= 0 and y >= 0 and y < len(_map[0]) and x < len(_map)

def try_candidate(lst):
    if point_in_bounds(*lst):
        if _map[lst[0]][lst[1]] == '.':
            _map[lst[0]][lst[1]] = '#'
        antinodes.add((lst[0], lst[1]))
        return True
    return False

fname = "input.test2.txt"
antennas = {}
_map = []
line_count = 0
with open(fname) as file:
    for line in file:
        _map.append(list(line.strip()))
        for idx, char in enumerate(_map[-1]):
            if char != '.':
                antennas.setdefault(char, [])
                antennas[char].append([line_count, idx])
        line_count += 1

antinodes = set()
for _, coordinates in antennas.items():
    # iterate over unique pairs
    for i, point_a in enumerate(coordinates):
        for _, point_b in enumerate(coordinates[i+1:]):
            x_dist = point_b[0] - point_a[0]
            # Diagonal A ... B
            if point_a[1] < point_b[1]:
                y_dist = point_b[1] - point_a[1]
                # We start at k = 0 because two antennas will always be antinodes of each other.
                k = 0
                while any([
                    try_candidate([ point_a[0] - x_dist*k, point_a[1] - y_dist*k]),
                    try_candidate([ point_b[0] + x_dist*k, point_b[1] + y_dist*k])
                ]):
                    k += 1
            # Diagonal B ... A
            else:
                y_dist = point_a[1] - point_b[1]
                k = 0
                while any([
                    try_candidate([ point_a[0] - x_dist*k, point_a[1] + y_dist*k]),
                    try_candidate([ point_b[0] + x_dist*k, point_b[1] - y_dist*k])
                ]):
                    k += 1
dump_map()
print(len(antinodes))