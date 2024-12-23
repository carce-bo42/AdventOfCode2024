import re
from itertools import combinations


from itertools import chain, repeat, count, islice
from collections import Counter


def repeat_chain(values, counts):
    return chain.from_iterable(map(repeat, values, counts))


def unique_combinations_from_value_counts(values, counts, r):
    n = len(counts)
    indices = list(islice(repeat_chain(count(), counts), r))
    if len(indices) < r:
        return
    while True:
        yield tuple(values[i] for i in indices)
        for i, j in zip(reversed(range(r)), repeat_chain(reversed(range(n)), reversed(counts))):
            if indices[i] != j:
                break
        else:
            return
        j = indices[i] + 1
        for i, j in zip(range(i, r), repeat_chain(count(j), counts[j:])):
            indices[i] = j


def unique_combinations(iterable, r):
    values, counts = zip(*Counter(iterable).items())
    return unique_combinations_from_value_counts(values, counts, r)

def read_file(filename: str) -> list[int]:

    connections = []
    with open(filename) as file:
        for line in file:
            m = re.match(r"(\w+)-(\w+)", line.strip())
            connections.append(frozenset((str(m.group(1)),str(m.group(2)))))

    return connections

if __name__ == "__main__":
    connections = read_file("input.txt")
    parties = set()
    asd = 0
    print(len(connections))
    for c1,c2,c3 in combinations(connections, 3):
        asd += 1 
        if len(c1|c2|c3) == 3:
            parties.add(c1|c2|c3)
    
    res = 0
    for party in parties:
        if any(s[0] == 't' for s in party):
            res += 1
    print(res)
    