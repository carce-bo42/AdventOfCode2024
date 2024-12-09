import copy

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

        idx_at_solution = find_index(disk_solved, pair)
        idx_space, space = search_space(disk_solved, idx_at_solution, pair[1])

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
