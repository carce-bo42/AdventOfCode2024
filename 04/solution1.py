# There are 3668 X's on the file.
# Hay que escanear en 8 direcciones.

def scan_n(x,y):
    if arr[x-1][y] != 'M':
        return False
    if arr[x-2][y] != 'A':
        return False
    if arr[x-3][y] != 'S':
        return False
    return True

def scan_ne(x,y):
    if arr[x-1][y+1] != 'M':
        return False
    if arr[x-2][y+2] != 'A':
        return False
    if arr[x-3][y+3] != 'S':
        return False
    return True

def scan_e(x,y):
    if arr[x][y+1] != 'M':
        return False
    if arr[x][y+2] != 'A':
        return False
    if arr[x][y+3] != 'S':
        return False
    return True

def scan_se(x,y):
    if arr[x+1][y+1] != 'M':
        return False
    if arr[x+2][y+2] != 'A':
        return False
    if arr[x+3][y+3] != 'S':
        return False
    return True

def scan_s(x,y):
    if arr[x+1][y] != 'M':
        return False
    if arr[x+2][y] != 'A':
        return False
    if arr[x+3][y] != 'S':
        return False
    return True

def scan_sw(x,y):
    if arr[x+1][y-1] != 'M':
        return False
    if arr[x+2][y-2] != 'A':
        return False
    if arr[x+3][y-3] != 'S':
        return False
    return True

def scan_w(x,y):
    if arr[x][y-1] != 'M':
        return False
    if arr[x][y-2] != 'A':
        return False
    if arr[x][y-3] != 'S':
        return False
    return True

def scan_nw(x,y):
    if arr[x-1][y-1] != 'M':
        return False
    if arr[x-2][y-2] != 'A':
        return False
    if arr[x-3][y-3] != 'S':
        return False
    return True


def scan_xmas(x,y):
    return sum([
        scan_n(x,y) if x-3 >= 0 else False,
        scan_ne(x,y) if x-3 >= 0 and y+3 < len(arr[0]) else False,
        scan_e(x,y) if y+3 < len(arr[0]) else False,
        scan_se(x,y) if x+3 < len(arr) and y+3 < len(arr[0]) else False,
        scan_s(x,y) if x+3 < len(arr) else False,
        scan_sw(x,y) if x+3 < len(arr) and y-3 >= 0 else False,
        scan_w(x,y) if y-3 >= 0 else False,
        scan_nw(x,y) if x-3 >= 0 and y-3 >= 0 else False
    ])

fname = "input.txt"
arr = []
with open(fname) as file:
    for line in file:
        arr.append(list(line.strip()))

# arr[x][y] = letra en fila x columna y
count = 0

for x in range(0,len(arr)):
    for y in range(0,len(arr[0])):
        if (arr[x][y] == 'X'):
            count += scan_xmas(x,y)
            
print(count)