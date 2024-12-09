import copy


def get_last_nonempty_element(disk):

    for idx, pair in enumerate(reversed(disk)):
        if pair[0] != -1:
            return (len(disk) -1) - idx

# Solo busco por la ixquierda
def search_space(disk, idx_max, amount):

    for idx, pair in enumerate(disk):

        # Dont search beyond the position
        if idx >= idx_max:
            break

        if pair[0] == -1 and pair[1] >= amount:
            return idx, pair[1]

    return -1, -1

def find_index(disk, unique_pair):

    for idx, pair in enumerate(disk):
        if pair == unique_pair:
            return idx

# Esto seguramente no haga falta.
# Pero cuando hemos copiado un nodo a otro lugar, deberíamos
# limpiar la procedencia:
# [ -1, 2 ], [ -1, 3 ] == [ -1, 5 ]

def print_solution(disk):
    for id, value in disk:
        if id != -1:
            print(f"{str(id)*value}", end="")
        else:
            print("."*value, end="")
    print("")

disk_original = []

fname = "input.txt"
max_id = 0
with open(fname) as file:
    for line in file:
        for idx, char in enumerate(line):
            if idx % 2 == 0:
                disk_original.append([int(idx/2), int(char)])
            else:
                disk_original.append([-1, int(char)])

disk_solved = copy.deepcopy(disk_original)

count = 0
for idx, pair in enumerate(reversed(disk_original)):

    if pair[0] != -1:

        # El index original es el inverso, pero teniendo en cuenta cuando
        # partimos [-1, 5] -> [3, 4], [-1, 1]. Aqui aparece una nueva entrada.
        # Si esta entrada esta antes o despues del numero siguiente que conseguiremos
        # mover, no lo sabemos. Asi que buscamos el indice y listos.
        idx_at_solution = find_index(disk_solved, pair)

        # Busco el indice (en la solucion) tal que el "file" cabe
        # i.e. disk_solved[idx2] = [ -1, <valor >= pair[1] ].
        idx_space, space = search_space(disk_solved, idx_at_solution, pair[1])

        # Si no cabe el file en ningun hueco, vamos al siguiente par.
        if idx_space == -1:
            continue

        disk_solved[idx_space] = [ pair[0], pair[1] ]
        disk_solved[idx_at_solution][0] = -1
        if space > pair[1]:
            disk_solved.insert(idx_space+1, [ -1, space - pair[1] ])

count = 0
pos = 0
for id, value in disk_solved:

    if id == -1:
        pos += value
        continue

    while value > 0:
        count += id * pos
        pos += 1
        value -= 1

print(count)
