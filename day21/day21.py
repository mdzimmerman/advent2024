import functools
import itertools
import sys

import aoc

sys.path.append("..")
from aoc import Logger, Point

class Pad:
    layout: str
    position: dict[str, Point]
    keyname: dict[Point, str]

    def __init__(self, layout: str):
        self.layout = layout
        self.position = dict()
        self.keyname = dict()

        j = 0
        for line in layout.split("\n"):
            if not line:
                continue
            for i, c in enumerate(line):
                p = Point(i, j)
                self.position[c] = p
                self.keyname[p] = c
            j += 1

    def is_blocked(self, start: Point, dir: str, nsteps: int):
        space = self.position[" "]
        xrange = [start.x, start.x]
        yrange = [start.y, start.y]
        if dir == '<':
            xrange[0] = start.x-nsteps
        elif dir == '>':
            xrange[1] = start.x+nsteps
        elif dir == '^':
            yrange[0] = start.y-nsteps
        elif dir == "v":
            yrange[1] = start.y+nsteps

        return xrange[0] <= space.x <= xrange[1] and yrange[0] <= space.y <= yrange[1]

NUMERIC_PAD = Pad("""
789
456
123
 0A
""")

DIRECTIONAL_PAD = Pad("""
 ^A
<v>
""")

def part1(codes: list[str], logger: Logger=Logger.WARN):
    total = 0
    for c in codes:
        pat = move(c)
        val = int(c[:-1])
        score = val * len(pat)
        logger.debug(c, pat, val, len(pat), score)
        total += score
    return total

def move(ks, logger: Logger=Logger.WARN):
    d1 = move_numeric(ks)
    d2 = move_directional(d1)
    d3 = move_directional(d2)
    logger.debug(d3, len(d3))
    logger.debug(d2, len(d2))
    logger.debug(d1, len(d1))
    logger.debug(ks, len(ks))
    return d3

def move_numeric(ks):
    out = "".join(move_press_numeric(k1, k2) for k1, k2 in itertools.pairwise("A"+ks))
    return out

def move_directional(ks):
    out = "".join(move_press_directional(k1, k2) for k1, k2 in itertools.pairwise("A"+ks))
    return out

@functools.cache
def move_press_numeric(k1, k2):
    return move_press(k1, k2, NUMERIC_PAD)

@functools.cache
def move_press_directional(k1, k2):
    return move_press(k1, k2, DIRECTIONAL_PAD)

def move_press(k1, k2, destpad):
    p1 = destpad.position[k1]
    p2 = destpad.position[k2]
    diff = p2 - p1

    pathx = ""
    ewfirst = True
    if diff.x < 0:
        if destpad.is_blocked(p1, "<", abs(diff.x)):
            ewfirst = False
        pathx = "<" * abs(diff.x)
    elif diff.x > 0:
        if destpad.is_blocked(p1, ">", abs(diff.x)):
            ewfirst = False
        pathx = ">" * diff.x
    pathy = ""
    if diff.y < 0:
        pathy = "^" * abs(diff.y)
    elif diff.y > 0:
        pathy = "v" * diff.y
    if ewfirst:
        return pathx+pathy+"A"
    else:
        return pathy+pathx+"A"


if __name__ == '__main__':
    print(NUMERIC_PAD.layout)
    print(NUMERIC_PAD.keyname)

    test = aoc.read_lines("test.txt")
    move(test[0], logger=Logger.DEBUG)
    move(test[2], logger=Logger.DEBUG)
    print(part1(test, logger=Logger.DEBUG))

    inp = aoc.read_lines("input.txt")
    print(part1(inp, logger=Logger.DEBUG))
