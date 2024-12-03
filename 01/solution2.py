fname = "input.txt"
l1 = []
l2 = []
with open(fname) as f:
    for line in f:
        x, y = map(int, line.strip().split())
        l1.append(x)
        l2.append(y)

s1 = set(l1)
similarity = 0
for num in s1:
    similarity += num * l1.count(num) * l2.count(num)

print(similarity)
