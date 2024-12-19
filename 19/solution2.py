import functools

@functools.cache
def design_can_be_done(design: str, patterns: frozenset[str]) -> int:

    # If theres nothing else to keep parsing, weve succesfully
    # matched a pattern with all slices of the string
    if not design:
        return 1

    # Find all possible patterns that could match the beggining
    # of the design
    valid_patterns = set()
    for pattern in patterns:
        if design.startswith(pattern):
            valid_patterns.add(pattern)

    # Iterate for all valid_patterns found, see if any return True
    count = 0
    for pattern in valid_patterns:
        count += design_can_be_done(design[len(pattern):], patterns)

    return count

def read_file(filename: str) -> tuple[frozenset[str], frozenset[str]]:

    patterns_ended = False
    designs = set()
    with open(filename) as file:
        for line in file:
            sline = line.strip()
            if len(sline) == 0:
                patterns_ended = True
                continue
            if not patterns_ended:
                patterns = frozenset(p.strip() for p in sline.split(","))
            else:
                designs.add(sline)

    return patterns, frozenset(designs)

if __name__ == "__main__":

    patterns, designs = read_file("input.txt")
    possible_designs = 0
    for design in designs:
        if different_designs := design_can_be_done(design, patterns):
            possible_designs += different_designs
    print(possible_designs)
