

def dump_map():
    for i in range(0, len(_map)):
        print("".join(_map[i]))

# x and y start at 0.
def move_guard(x_origin, y_origin, direction):

    x = x_origin
    y = y_origin

    memory.setdefault(f"{x}|{y}", set())
    if direction in memory[f"{x}|{y}"]:
        return
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
    return

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

memory = {}
move_guard(x_start, y_start, '^')
dump_map()

count = 0
for line in _map:
    count += line.count('X')

print(count)
# _map[x] tiene la linea x desde arriba
# _map[x][y] linea x, columna y

