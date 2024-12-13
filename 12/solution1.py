import copy

# Quiero algo del estilo
# { "A" : [
#       set( (xa1_1,ya1_2), (xa1_3,ya1_4) ... ),
#       set( (xa2_1,ya2_2), (xa2_3,xa2_4) ... ]),
#       ...
#   ],
#   "B" : [
#       set( (xb1_1, xb1_2) ... ),
#       ...
#   ],
#   ...
# }

# El mapa puede tener 1 flag de tipo "visited". Si un punto ha sido "visited",
# el flood fill no continúa por ahí, para no estar añadiendo puntos dobles etc.

# Otra posibilidad es ir cogiendo cada uno de los puntos y meterlos en el diccionario.
# En plan, empezar con
# { "A" : set( todos los puntos que sean A )
#   "B"  : set( todos los puntos que sean B )
#   ...
# }
# Y de aqui luego cojer el A y ver qué puntos forman un grupo y cuales no.
# Así recorres el input 1 vez, y luego lo que haces son malabares.
# Makes sense. More sense almenos que recorrerse el mapa entero con un floodFill.
#
# Los malabares en cuestion sería cojer 1 punto del A, y ver si vecinos en el grupo.
# Cuadno ya ningun vecino tenga vecinos, habré encontrado el primer grupo de "A".
# Voy borrando del "pool" de puntos aquellos que vaya metiendo en grupos, y listos.

# para acceder a un elemento SIN BORRAR estamos obligados a iterar el set
# hacemos break al salir para que no de por culo.
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

    # Buscamos el resto de peers del grupo.
    garden = find_peers(set(), point, coordinates)

    # Añadimos el garden encontrado al tipo de plantas que pertenece
    gardens.setdefault(gtype, []).append(garden)


def count_fences(garden, point, fences):

    # If ive already been at this point.
    if point in memo:
        return 0

    fences = 0

    memo.add(point)
    x, y = point

    for candidate in (x+1,y), (x-1,y), (x,y+1), (x,y-1):
        if candidate not in garden:
            fences += 1
        else:
            fences += count_fences(garden, candidate, fences)

    return fences

def get_fencing_price():

    price = 0
    for plant in gardens.keys():
        for garden in gardens[plant]:
            # Para contar fences, tenemos que saber por qué lugares hemos pasado ya y por cuales no.
            global memo
            memo = set()
            #print(len(garden), count_fences(garden, get_one_element_from_set(garden), 0))
            price += len(garden) * count_fences(garden, get_one_element_from_set(garden), 0)
    return price

fname = "input.txt"
with open(fname) as file:
    _map = {}
    for x, line in enumerate(file):
        for y, char in enumerate(line.strip()):
            _map.setdefault(char, set()).add((x,y))

# Este es mi diccionario soñado en la parte de arriba. Aqui rellenaremos los grupos
gardens = {}

for plant, coordinates in _map.items():
    while len(coordinates) > 0:
        generate_gardens_of_same_plant(plant, coordinates)

# Esto estoy 100% seguro de que se puede hacer mientras generabamos los grupos antes.
# Pero esto es mas straightforward y me la pela optimizar llegados a este punto.
print(get_fencing_price())