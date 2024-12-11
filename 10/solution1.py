# x and y start at 0.
def search_hike(x, y, memory):
    
    height = int(_map[x][y])
    if height == 9:
        memory.add(f"{x}|{y}")
        return
    
    if x+1 < len(_map) and int(_map[x+1][y]) == height+1:
        search_hike(x+1, y, memory)
    if x-1 >= 0 and int(_map[x-1][y]) == height+1:
        search_hike(x-1, y, memory)
    if y+1 < len(_map[0]) and int(_map[x][y+1]) == height+1:
        search_hike(x, y+1, memory)
    if y-1 >= 0 and int(_map[x][y-1]) == height+1:
        search_hike(x, y-1, memory)
    return

fname = "input.txt"
_map = []
with open(fname) as file:
    for line in file:
        _map.append(list(line.strip()))

score = 0
for x in range(0, len(_map)):
    for y in range(0, len(_map[0])):
        if _map[x][y] == '0':
            hikes_reached = set()
            search_hike(x, y, hikes_reached)
            score += len(hikes_reached)

print(score)
