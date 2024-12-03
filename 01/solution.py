fname = "input.txt"
l1 = []
l2 = []
with open(fname) as f:
    for line in f:
        lst = line.strip().split()
        l1.append(int(lst[0]))
        l2.append(int(lst[1]))

l1.sort()
l2.sort()
distance = 0

for vv in range(0,len(l1)):
    distance += abs(l1[vv] - l2[vv])

print(distance)

