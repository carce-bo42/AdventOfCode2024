import re

fname = "input.txt"
count = 0
with open(fname) as file:
    for line in file:
        for match in re.findall(r"mul\(\d+,\d+\)", line):
            m = re.match(r"mul\((\d+),(\d+)\)", match)
            count += int(m.group(1)) * int(m.group(2))

print(count)