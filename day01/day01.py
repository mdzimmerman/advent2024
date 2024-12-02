def dist(x, y):
    return abs(x - y)

def get_lists(filename):
    ls, rs = [], []
    with open(filename, 'r') as fh:
        for l in fh:
            xs = l.split()
            ls.append(int(xs[0]))
            rs.append(int(xs[1]))
    return ls, rs

def part1(ls, rs):
    return sum(dist(l, r) for l, r in zip(sorted(ls), sorted(rs)))


def part2(ls, rs):
    rindex = dict()
    for r in rs:
        if r not in rindex:
            rindex[r] = 0
        rindex[r] += 1
    out = 0
    for l in ls:
        if l in rindex:
            out += l * rindex[l]
    return out


if __name__ == '__main__':
    print("-- test --")
    ls, rs = get_lists("test.txt")
    print(part1(ls, rs))
    print(part2(ls, rs))

    print("-- input --")
    ls, rs = get_lists("input.txt")
    print(part1(ls, rs))
    print(part2(ls, rs))