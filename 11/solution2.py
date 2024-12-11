import functools

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

# Esto hace que se cacheen las llamadas con argumentos iguales.
@functools.cache
def blink_n_times(times, n):
    
    res = blink(n)
    
    if times == 1:
        return len(res)
    else:
        total = blink_n_times(times-1, res[0])
        if len(res) > 1:
            total += blink_n_times(times-1, res[1])
        return total

fname = "input.txt"
count = 0
numbers = []
with open(fname) as file:
    for line in file:
        numbers = line.strip().split()

# No hay que ir iterando el resultado de todas las piedras nivel por nivel.
# Hay que hacer el problema piedra por piedra.
count = 0
for nbr in numbers:
    count += blink_n_times(75, nbr)

print(count)