import re
import sys

sys.path.append("..")
from aoc import Logger

def slurp(filename) -> str:
    out = ""
    with open(filename, "r") as fh:
        for l in fh:
            out += l.rstrip()
    return out

PATTERN = re.compile(r"(mul|do|don't)\((?:(\d+),(\d+))?\)")

def part1(s, logger: Logger=Logger()):
    tot = 0
    for m in re.finditer(PATTERN, s):
        logger.debug(m.group(0))
        if m.group(1) == 'mul':
            x = int(m.group(2))
            y = int(m.group(3))
            tot += x * y
    return tot

def part2(s, logger: Logger=Logger()):
    tot = 0
    enabled = True
    for m in re.finditer(PATTERN, s):
        logger.debug(m.group(0))
        if m.group(1) == "mul":
            x = int(m.group(2))
            y = int(m.group(3))
            if enabled:
                tot += x * y
        elif m.group(1) == "do":
            enabled = True
        elif m.group(1) == "don't":
            enabled = False
    return tot


if __name__ == '__main__':
    testlogger=Logger("DEBUG")
    print("-- test --")
    test = slurp("test.txt")
    print(test)
    print("part1 =", part1(test, logger=testlogger))

    test2 = slurp("test2.txt")
    print("part2 =", part2(test2, logger=testlogger))

    print()
    print("-- input --")
    inp = slurp("input.txt")
    print("part1 =", part1(inp))
    print("part2 =", part2(inp))