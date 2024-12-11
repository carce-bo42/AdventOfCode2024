import functools

def get_memo_key(a, b):
    return f"{a}|{b}"

def blink(n):
    
    result = []
    
    if n == '0':
        result.append('1')
    elif len(n)%2 == 0:
        mid_digits = len(n)//2
        result.append(n[:mid_digits])
        # str(int()) para quitar 0 a la izq.
        result.append(str(int(n[mid_digits:])))
    else:
        result.append(str(int(n)*2024))
    
    return result


def blink_n_times(times, n):

    # La busqueda de una llave en un diccionario es O(n), el acceso es O(log n)..
    # Esto me lo dijo Daniel Santo Tomas en una comida de empresa, God Bless
    
    key = get_memo_key(times, n)

    try:
        return memo[key]
    except KeyError:
        res = blink(n)
        if times == 1:
            memo[key] = len(res)
        else:
            total = blink_n_times(times-1, res[0])
            if len(res) > 1:
                total += blink_n_times(times-1, res[1])
            memo[key] = total
        return memo[key]
        
fname = "input.txt"
count = 0
numbers = []
with open(fname) as file:
    for line in file:
        numbers = line.strip().split()

# No hay que ir iterando el resultado de todas las piedras nivel por nivel.
# Hay que hacer el problema piedra por piedra.
count = 0
memo = {}
for nbr in numbers:
    count += blink_n_times(75, nbr)

print(count)