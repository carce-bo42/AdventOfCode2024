# Voy a descomponer el problema en N iteraciones de M interaciones
# N < M
# Cada vez que hago 5 iteraciones, me guardo el resultado de un numero
# tras esas 5. Luego, hago lo mismo con los numeros que salen de esta.
# En unas cuantas iteraciones, no debería casi tener que estar calculando
# nada.

def do_weird_fibonacci(times, numbers):
    
    if times == 0:
        return numbers
    
    result = []
    for n in numbers:
        if n == '0':
            result.append('1')
        elif len(n)%2 == 0:
            result.append(n[0:len(n)//2])
            result.append(str(int(n[len(n)//2:len(n)])))
        else:
            result.append(str(int(n)*2024))

    return do_weird_fibonacci(times-1, result)

fname = "input.txt"
count = 0
numbers = []
with open(fname) as file:
    for line in file:
        numbers = line.strip().split()

memo = {}
rr = []

M = 9
N = 5
for x in range(0, M):
    rr = []
    for n in numbers:
        if n not in memo.keys():
            memo[n] = do_weird_fibonacci(N, [n])
        rr.extend(memo[n])
    numbers = rr

print(len(memo))

print(len(numbers))