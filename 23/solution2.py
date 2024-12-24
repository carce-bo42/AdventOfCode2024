import re

def read_file(filename: str) -> tuple[dict[str, list[str]], list[frozenset[str]]]:

    graph = dict()
    connections = []
    with open(filename) as file:
        for line in file:
            m = re.match(r"(\w+)-(\w+)", line.strip())
            graph.setdefault(m.group(1), []).append(m.group(2))
            graph.setdefault(m.group(2), []).append(m.group(1))
            connections.append(frozenset((m.group(1),m.group(2))))

    return graph, connections

def bron_kerbosch(R, P, X):



if __name__ == "__main__":

    graph, _ = read_file("input.txt")
