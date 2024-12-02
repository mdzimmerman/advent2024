import itertools

def read_file(filename):
    out = []
    with open(filename, "r") as fh:
        for l in fh:
            out.append([int(x) for x in l.strip().split()])
    return out

def part1(xs, debug=0):
    nvalid = 0
    for x in xs:
        dxs = [b-a for a, b in itertools.pairwise(x)]
        valid = 0
        if all(1 <= dx <= 3 for dx in dxs) or all(-3 <= dx <= -1 for dx in dxs):
            valid = 1
        if debug >= 2:
            print(x, valid)
        nvalid += valid
    return nvalid

def part2(xs, debug=0):
    pass

if __name__ == '__main__':
    test = read_file("test.txt")
    for l in test:
        print(l)
    print(part1(test))

    print()
    print("-- input --")
    inp = read_file("input.txt")
    print(part1(inp))