import re

def read_file(filename: str) -> dict[str, list[str]]:

    graph = dict()
    with open(filename) as file:
        for line in file:
            m = re.match(r"(\w+)-(\w+)", line.strip())
            graph.setdefault(m.group(1), []).append(m.group(2))
            graph.setdefault(m.group(2), []).append(m.group(1))

    return graph

if __name__ == "__main__":
    graph = read_file("input.txt")

    cliques3 = set()
    for c1, neighbours in graph.items():
        for c2 in neighbours:
            for c3 in graph[c2]:
                if c1 in graph[c3]:
                    if any(s[0] == 't' for s in (c1,c2,c3)):
                        cliques3.add(frozenset((c1,c2,c3)))
    print(len(cliques3))