
def dump_map():
    for i in range(0, len(_map)):
        print("".join(_map[i]))

# x and y start at 0.
def move_guard(x_origin, y_origin, direction):

    x = x_origin
    y = y_origin

    memory.setdefault(f"{x}|{y}", set())
    if direction in memory[f"{x}|{y}"]:
        # Estamos en un bucle !
        return 1
    memory[f"{x}|{y}"].add(direction)

    if direction == '^':
        while x >= 0:
            if _map[x][y] == '#':
                return move_guard(x+1, y, '>')
            _map[x][y] = 'X'
            x -= 1
    elif direction == '>':
        while y < len(_map[0]):
            if _map[x][y] == '#':
                return move_guard(x, y-1, 'v')
            _map[x][y] = 'X'
            y += 1
    elif direction == 'v':
        while x < len(_map):
            if _map[x][y] == '#':
                return move_guard(x-1, y, '<')
            _map[x][y] = 'X'
            x += 1
    elif direction == '<':
        while y >= 0:
            if _map[x][y] == '#':
                return move_guard(x, y+1, '^')
            _map[x][y] = 'X'
            y -= 1

    return 0

fname = "input.txt"
_map = []
count = 0
x_start = 0
y_start = 0
with open(fname) as file:
    for line in file:
        _map.append(list(line.strip()))
        tmp = line.find('^')
        if tmp != -1:
            x_start = count
            y_start = tmp
        count +=1

# _map[x] tiene la linea x desde arriba
# _map[x][y] linea x, columna y

# Encontramos las posiciones por las que el guardia se mueve.
memory = {}
move_guard(x_start, y_start, '^')

# Como solo podemos poner un obstaculo, tendremos que ponerlo por donde
# se mueve. De esta forma, se reduce el espacio de busqueda.

# Cada par es un candidato a nuevo obstaculo
candidates = []
for x in range(0, len(_map)):
    for y in range(0, len(_map[0])):
        if _map[x][y] == 'X':
            candidates.append([x,y])

valid_options = 0
for x, y in candidates:

    # Reseteamos la memoria
    memory = {}

    # Metemos el obstaculo
    _map[x][y] = '#'

    # Le hacemos iterar. Si es 1, sale porque va a repetir un movimiento
    # => Está en bucle
    valid_options += move_guard(x_start, y_start, '^')

    # Reseteamos la posicion del obstaculo
    _map[x][y] = '.'

print(valid_options)