import itertools

def read_file(filename):
    out = []
    with open(filename, "r") as fh:
        for l in fh:
            out.append([int(x) for x in l.strip().split()])
    return out

def isvalid(xs):
    dxs = [b-a for a, b in itertools.pairwise(xs)]
    if all(1 <= dx <= 3 for dx in dxs) or all(-3 <= dx <= -1 for dx in dxs):
        return 1
    else:
        return 0

def part1(xs, debug=0):
    nvalid = 0
    for x in xs:
        valid = isvalid(x)
        if debug >= 2:
            print(x, valid)
        nvalid += valid
    return nvalid

def part2(xs, debug=0):
    nvalid = 0
    for x in xs:
        valid = 0
        if isvalid(x):
            valid = 1
        else:
            for i in range(len(x)):
                if isvalid([xi for j, xi in enumerate(x) if j != i]):
                    valid = 1
                    break
        if debug >= 2:
            print(x, valid)
        nvalid += valid
    return nvalid


if __name__ == '__main__':
    test = read_file("test.txt")
    for l in test:
        print(l)
    print(part1(test))
    print(part2(test, debug=2))

    print()
    print("-- input --")
    inp = read_file("input.txt")
    print(part1(inp))
    print(part2(inp, debug=0))