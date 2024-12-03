
# No se repiten
# Las diffs no pueden tener mas de 3 valores (-1,-2,-3) o (1,2,3)
# Ni pueden haber diffs de distinto signo
def sequence_is_ok(lst):
    if len(set(lst)) != len(lst):
        return False
    steps = set([ lst[i] - lst[i-1] for i in range(1,len(lst)) ])
    if len(steps) > 3 or min(steps) < -3 or max(steps) > 3:
        return False
    if all([ x > 0 for x in steps ]):
        return True
    if all([ x < 0 for x in steps ]):
        return True
    return False

fname = "input.txt"
count = 0
with open(fname) as file:
    for line in file:
        nn = [ int(num) for num in line.strip().split() ]
        if sequence_is_ok(nn):
            count += 1

print(count)
