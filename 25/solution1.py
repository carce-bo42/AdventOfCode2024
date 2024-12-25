# Son de 5 x 7
# Top row filled # -> lock
# Bottom row filled # -> key

(
    IDLE,
    KEY,
    LOCK
) = range(3)

def read_line(line, tmp):
    for pos, char in enumerate(line):
        if char == '#':
            tmp[pos] += 1
    return tmp

def read_file(filename: str) -> tuple[list[list[int]], list[list[int]]]:

    keys = []
    locks = []
    with open(filename) as file:
        tmp = []
        state = IDLE
        for line in file:
            sline = line.strip()
            if not sline:
                if state == LOCK:
                    locks.append(tmp)
                elif state == KEY:
                    keys.append(tmp)
                state = IDLE
                continue

            if state == IDLE:
                if sline[0] == '#':
                    state = LOCK
                    tmp = [1,1,1,1,1]
                elif sline[0] == '.':
                    state = KEY
                    tmp = [0,0,0,0,0]
            else:
                tmp = read_line(sline, tmp)

        if state == LOCK:
            locks.append(tmp)
        elif state == KEY:
            keys.append(tmp)

    return keys, locks

def find_lock_key_pairs(keys, locks):
    fits = 0
    for key in keys:
        for lock in locks:
            if not any([a + b > 7 for a, b in zip(key, lock)]):
                fits += 1
    return fits

if __name__ == "__main__":
    keys, locks = read_file("input.txt")
    print(find_lock_key_pairs(keys, locks))