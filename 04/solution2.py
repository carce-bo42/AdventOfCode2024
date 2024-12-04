def scan_xmas2(x,y):
    if x-1 >= 0 and x+1 < len(arr) and y-1 >= 0 and y+1 < len(arr[0]):
        if {arr[x-1][y-1],arr[x-1][y+1],
            arr[x+1][y-1],arr[x+1][y+1]} != {'S','M'}:
            return False
        if arr[x-1][y-1] == arr[x+1][y+1]:
            return False
        if arr[x+1][y-1] == arr[x-1][y+1]:
            return False
    else:
        return False
    return True

fname = "input.txt"
arr = []
with open(fname) as file:
    for line in file:
        arr.append(list(line.strip()))

# arr[x][y] = letra en fila x columna y
count = 0

for x in range(0,len(arr)):
    for y in range(0,len(arr[0])):
        if (arr[x][y] == 'A'):
            count += scan_xmas2(x,y)
            
print(count)