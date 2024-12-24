import re

def read_file(filename: str) -> dict[str, list[str]]:

    graph = dict()
    with open(filename) as file:
        for line in file:
            m = re.match(r"(\w+)-(\w+)", line.strip())
            graph.setdefault(m.group(1), set()).add(m.group(2))
            graph.setdefault(m.group(2), set()).add(m.group(1))

    return graph

def bron_kerbosch(
        R: set[str],
        P: set[str],
        X: set[str],
        N: dict[str, set[str]]
    ):
    if not P and not X:
        yield R
    for v in P:
        # Add vertex v to R, and recurse
        yield from bron_kerbosch(
            R | {v},  # Add v to the current clique R
            P & N[v],  # Restrict P to the neighbors of v
            X & N[v],  # Restrict X to the neighbors of v
            N
        )
        # Move v from P to X
        P = P - {v}
        X = X | {v}

if __name__ == "__main__":

    graph = read_file("input.txt")
    max_len = 0
    for s in bron_kerbosch(set(), set(graph.keys()), set(), graph):
        if max_len < len(s):
            max_len = len(s)
            result = s
    lst = list(result)
    lst.sort()
    print(",".join(s for s in lst))