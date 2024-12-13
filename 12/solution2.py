import copy

def get_one_element_from_set(_set):
    for x in _set:
        return x

def get_memo_key(a, b):
    return f"{a}|{b}"

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

# La gracia esta en generar un nuevo grupo con los puntos que NO pertenecen
# al grupo. Luego, con este grupo, se puede trabajar somehow para saber
# cuantos lados tiene:
#
#
#                        11111
# EEEEE      EEEEE      1EEEEE1
# EXXXX      E          1E3222
# EEEEE  =>  EEEEE  =>  1EEEEE1  => max(cada grupo contiguo) = 1 + 1 + 1 + 1 + 1 +1 + 3 + 3 = 12
# EXXXX      E          1E3222
# EEEEE      EEEEE      1EEEEE1
#                        11111
#
#                        11111
# AAAAA      AAAAA      1AAAAA1
# AXAXA      A A A      1A4A4A1
# AAAAA  =>  AAAAA  =>  1AAAAA1  => max(cada grupo contiguo) = 1 + 1 + 1 + 1 + 4 + 4 + 4 + 4 = 20
# AXAXA      A A A      1A4A4A1
# AAAAA      AAAAA      1AAAAA1
#                        11111
#
#
#                          111111
# AAAAAA       AAAAAA     1AAAAAA1
# AAABBA       AAA  A     1AAA22A1
# AAABBA       AAA  A     1AAA22A1
# ABBAAA   =>  A  AAA     1A22AAA1
# ABBAAA       A  AAA     1A22AAA1
# AAAAAA       AAAAAA     1AAAAAA1
#                          111111
#

# Esto NO aplica para los grupos interiores.
#
#                          111111         000000
# AAAAAA       AAAAAA     1AAAAAA1       0AAAAAA0
# AAABBA       A    A     1A2112A1       0A1001A0
# AAABBA       A    A     1A1  1A1       0A0  0A0
# ABBAAA       A    A     1A1  1A1       0A0  0A0 ==> suma de todos
# ABBAAA       A    A     1A2112A1       0A1001A0
# AAAAAA       AAAAAA     1AAAAAA1       0AAAAAA0
#                          111111         000000
#

# AAAAA       AAAAA       AAAAA
# A   A       A312A       A201A   3 0 0
# AA  A   =>  AA11A       AA00A     1 0
# A   A       A2 1A       A1 0A   2   0
# A   A       A212A       A101A   0 0 2
# AAAAA       AAAAA       AAAAA

# Itero para los 3's

# Si soy un 3 -> cojo todos los numeros que hay en la unica direccion que puedo ir,
# y les resto 2. El minimo es 0.

# Itero para los 2's

# Si soy un 2, cojo la direccion en la que tengo compañeros y resto 2. A todos.

# Si soy un 1 depues de este juego, lo sumo.

#
# AAAAAAA      AAAAAAA     AAAAAAA    AAAAAAA
# AAAXAAA      AAA AAA     AAA3AAA    AAA2AAA
# AAAXAAA      AAA AAA     AAA2AAA    AAA1AAA
# AXXXXXA      A     A     A32 23A    A21012A ==> suma de todos
# AAAXAAA      AAA AAA     AAA2AAA    AAA1AAA
# AAAXAAA      AAA AAA     AAA3AAA    AAA2AAA
# AAAAAAA      AAAAAAA     AAAAAAA    AAAAAAA
#
#                 1 1 1  1
#  A A A  A      2A3A3A22A1
# AAAAAAAAA  => 1AAAAAAAAA1
#  A A A A       2A3A3A3A2
#                 1 1 1 1


# Si un grupo es interno, para buscar su numero de lados, tenemos que retroceder y hacer
# el calculo raro este pero haciendolo desde fuera. Un puto follon, pero si se hace así debería
# fnucionar.
# Si un grupo es interno, por definicion es englobable.

# Para calcular un grupo contiguo, basta con empezar en un numero e iterar con memoria.
# Cuando la memoria tenga todos los puntos, calculamos el max, quitamos esos puntos de los
# "grupos externos", y seguimos.

(
    NORTH,
    EAST,
    SOUTH,
    WEST
) = range(4)

# Each orientation differs in 90º
directions = {
    (-1,0): NORTH,
    (0,1): EAST,
    (1,0): SOUTH,
    (0,-1): WEST
}

#
#                          (x-1,y)
#           (x-0.5,y-0.5)           (x-0.5,y+0.5)
# (x,y-1)                   (x,y)                     (x,y+1)
#           (x+0.5,y-0.5)           (x+0.5,y+0.5)
#                          (x+1,y)
#


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
            print(len(garden), sides)
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