def get_one_element_from_set(_set):
    for x in _set:
        return x

def find_peers(garden, point, coordinates):
    coordinates.remove(point)
    garden.add(point)
    x, y = point
    for candidate in (x+1,y), (x-1,y), (x,y+1), (x,y-1):
        if candidate in coordinates:
            find_peers(garden, candidate, coordinates)
    return garden

def generate_gardens_of_same_plant(gtype, coordinates):
    point = get_one_element_from_set(coordinates)
    garden = find_peers(set(), point, coordinates)
    gardens.setdefault(gtype, []).append(garden)

(
    NORTH,
    EAST,
    SOUTH,
    WEST
) = range(4)

directions = {
    (-1,0): NORTH,
    (0,1): EAST,
    (1,0): SOUTH,
    (0,-1): WEST
}

def generate_groups(values, point):

    values.remove(point)
    x, y = point

    for candidate in (x+1,y), (x-1,y), (x,y+1), (x,y-1):
        if candidate in values:
            generate_groups(values, candidate)

    return 1

# Todos los valores tienen la misma orientacion aqui.
def compute_groups(values):

    groups = 0
    while len(values) > 0:
        point = get_one_element_from_set(values)
        groups += generate_groups(values, point)

    return groups


def compute_sides(garden, plant):

    sides = 0
    lattice = {}
    for point in garden:
        x, y = point
        for dx, dy in directions:
            if (x + dx, y + dy) not in garden:
                if dx == 1:
                    orientation = SOUTH
                if dx == -1:
                    orientation = NORTH
                if dy == 1:
                    orientation = EAST
                if dy == -1:
                    orientation = WEST

                lattice.setdefault(orientation, set()).add((x+dx,y+dy))

    # Now we find disjoint groups on each orientation:
    for orientation in directions.values():
        sides += compute_groups(lattice[orientation])

    return sides

def get_new_fencing_price():

    price = 0
    for plant in gardens.keys():
        for garden in gardens[plant]:
            sides = compute_sides(garden, plant)
            price += len(garden) * sides
    return price

fname = "input.txt"
with open(fname) as file:
    _map = {}
    for x, line in enumerate(file):
        for y, char in enumerate(line.strip()):
            _map.setdefault(char, set()).add((x,y))

gardens = {}

for plant, coordinates in _map.items():
    while len(coordinates) > 0:
        generate_gardens_of_same_plant(plant, coordinates)


print(get_new_fencing_price())