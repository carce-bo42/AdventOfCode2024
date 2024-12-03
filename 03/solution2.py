import re

fname = "input.txt"
count = 0
enabled = True
with open(fname) as file:
    for line in file:
        for match in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", line):
            if match == "don't()":
                enabled = False
            elif match == "do()":
                enabled = True
            elif enabled:
                m = re.match(r"mul\((\d+),(\d+)\)", match)
                count += int(m.group(1)) * int(m.group(2))
print(count)