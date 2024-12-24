import itertools
import sys

sys.path.append("..")
from aoc import Logger

PRUNE = 16777216

def calc_next(x):
    x = ((x * 64) ^ x) % PRUNE
    x = ((x // 32) ^ x) % PRUNE
    return ((x * 2048) ^ x) % PRUNE


def calc_next_n(x0, n=2000):
    x = x0
    for _ in range(n):
        x = calc_next(x)
    return x

def calc_iter(x0, n=2000):
    x = x0
    for _ in range(n+1):
        yield x
        x = calc_next(x)

def part1(filename, logger=Logger("WARN")):
    sum = 0
    with open(filename, "r") as fh:
        for l in fh:
            x = int(l.strip())
            x2k = calc_next_n(x, 2000)
            logger.debug(f"{x}: {x2k}")
            sum += x2k
    return sum

def get_prices(x0, n=2000):
    return list(x % 10 for x in calc_iter(x0, n=n))

def get_patterns(prices):
    dprices = [0]
    dprices.extend(b-a for a, b in itertools.pairwise(prices))
    #print(prices)
    #print(dprices)
    pattern = dict()
    for i in range(4, len(prices)):
        d4 = tuple(dprices[i-3:i+1])
        if d4 not in pattern:
            pattern[d4] = prices[i]
    return pattern

def part2(filename):
    patterns = dict()
    with open(filename, "r") as fh:
        for l in fh:
            x = int(l.strip())
            prices = get_prices(x, n=2000)
            patterns[x] = get_patterns(prices)
    aggregate = dict()
    for x, ps in patterns.items():
        for p, price in ps.items():
            if p not in aggregate:
                aggregate[p] = 0
            aggregate[p] += price
    top = list(sorted(aggregate.items(), key=lambda x: x[1], reverse=True))[:10]
    for t in top:
        print(t)
    return(top[0][1])


if __name__ == '__main__':
    print("-- test0 --")
    test0 = 123
    print(test0)
    for _ in range(10):
        test0 = calc_next(test0)
        print(test0)

    print()
    print("-- test --")
    print("part 1")
    print(part1("test.txt", logger=Logger("DEBUG")))

    print("-- test2 --")
    print("part 2")
    print(part2("test2.txt"))

    print()
    print("-- input --")
    print("part 1")
    print(part1("input.txt"))
    print("part 2")
    print(part2("input.txt"))
