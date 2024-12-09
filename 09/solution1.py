import copy


def get_last_nonempty_element(disk):

    for idx, pair in enumerate(reversed(disk)):
        if pair[0] != -1:
            return (len(disk) -1) - idx

# Necesito una estructura de datos que tenga pares [id, cantidad]
disk_original = []
disk_solved = []

fname = "input.txt"
max_id = 0
with open(fname) as file:
    for line in file:
        for idx, char in enumerate(line):
            if idx % 2 == 0:
                disk_original.append([int(idx/2), int(char)])
            else:
                disk_original.append([-1, int(char)])

count = 0
for idx1, pair in enumerate(disk_original):
    if pair[0] != -1:
        disk_solved.append(pair)
    else:
        space = pair[1]
        while space > 0:
            idx2 = get_last_nonempty_element(disk_original)
            if idx2 <= idx1:
                break
            id, amount = disk_original[idx2]
            fill = amount if space >= amount else space
            disk_solved.append([id, fill])
            if fill == amount:
                disk_original[idx2][0] = -1
            else:
                disk_original[idx2][1] = amount - fill
            space -= fill

count = 0
pos = 0
for id, value in disk_solved:
    if id == -1:
        break
    while value > 0:
        count += id * pos
        pos += 1
        value -= 1

print(count)