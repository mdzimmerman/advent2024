import sys

sys.path.append("..")
from aoc import Logger, CharArray

cw = {"N": "E", "E": "S", "S": "W", "W": "N"}

def part1(array):
    poscurr = [p for p in array.find("^")][0]
    dircurr = "N"

    seen = set()
    while array.in_bounds(poscurr):
        seen.add(poscurr)
        pn = poscurr.move(dircurr)
        if array.get(pn) == "#":
            dircurr = cw[dircurr]
            pn = poscurr.move(dircurr)
        poscurr = pn
    return(len(seen))

def part2(array, loglevel: str = ""):
    logger = Logger(loglevel)
    p0 = [p for p in array.find("^")][0]
    d0 = "N"

    print(f"width={array.width}, height={array.height}, total={array.width * array.height}")

    nobs = 0
    i = 0
    for pobs, c in array.enumerate():
        if c != ".":
            continue
        i += 1
        if (i % 10) == 0:
            print(i)

        p = p0
        d = d0
        seen = set()
        inloop = False
        while not inloop and array.in_bounds(p):
            if (p, d) in seen:
                inloop = True
            seen.add((p, d))
            pn = p.move(d)
            if array.get(pn) == "#" or pn == pobs:
                d = cw[d]
                pn = p.move(d)
            p = pn
        if inloop:
            nobs += 1
    return nobs

if __name__ == '__main__':
    test = CharArray.from_file("test.txt")
    print(test)
    test.print()
    print([p for p in test.find("#")])
    print(part1(test))
    print(part2(test))

    inp = CharArray.from_file("input.txt")
    print(part1(inp))
    print(part2(inp), loglevel="DEBUG")