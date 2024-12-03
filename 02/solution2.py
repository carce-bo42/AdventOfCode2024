
def sequence_is_ok(lst):
    if len(set(lst)) != len(lst):
        return False
    steps = set([ lst[i] - lst[i-1] for i in range(1,len(lst)) ])
    if len(steps) > 3 or min(steps) < -3 or max(steps) > 3:
        return False
    if all([ x > 0 for x in steps ]) or all([ x < 0 for x in steps ]):
        return True
    return False

def sequence_is_ok_after_reducing(lst):
    for i in range(0, len(lst)):
        if sequence_is_ok(reduced_list(lst, i)):
            return True

def reduced_list(lst, index):
    return [ lst[i] for i in range(0, len(lst)) if i != index ]

fname = "input.txt"
count = 0
with open(fname) as file:
    for line in file:
        nn = [ int(num) for num in line.strip().split() ]
        if sequence_is_ok(nn):
            count += 1
        elif sequence_is_ok_after_reducing(nn):
            count += 1
print(count)
