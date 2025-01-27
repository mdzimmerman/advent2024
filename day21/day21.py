import itertools
import sys

sys.path.append("..")
from aoc import Logger, Point

class Pad:
    position: dict[str, Point]
    keyname: dict[Point, str]

    def __init__(self, layout: str):
        self.position = dict()
        self.keyname = dict()

        j = 0
        for line in layout.split("\n"):
            if not line:
                continue
            for i, c in enumerate(line):
                p = Point(i, j)
                if c != " ":
                    self.position[c] = p
                    self.keyname[p] = c
            j += 1

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

def move(ks):
    d1 = "".join(move_and_press(k1, k2, NUMERIC_PAD) for k1, k2 in itertools.pairwise("A"+ks))
    d2 = "".join(move_and_press(k1, k2, DIRECTIONAL_PAD) for k1, k2 in itertools.pairwise("A"+d1))
    d3 = "".join(move_and_press(k1, k2, DIRECTIONAL_PAD) for k1, k2 in itertools.pairwise("A"+d2))
    print(d3)
    print(d2)
    print(d1)
    print(ks)

def move_and_press(k1, k2, destpad):
    p1 = destpad.position[k1]
    p2 = destpad.position[k2]
    diff = p2 - p1

    pathx = ""
    ewfirst = True
    if diff.x < 0:
        for x in range(p1.x, p1.x-1, -1):
            p = Point(x, p1.y)
            if p not in destpad.keyname:
                ewfirst = False
                break
        pathx = "<" * abs(diff.x)
    elif diff.x > 0:
        pathx = ">" * diff.x
        for x in range(p1.x, p1.x+1, 1):
            p = Point(x, p1.y)
            if p not in destpad.keyname:
                ewfirst = False
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
    #print(NUMERIC_PAD.position)
    #print(NUMERIC_PAD.keyname)
    #print(DIRECTIONAL_PAD.position)
    #print(DIRECTIONAL_PAD.keyname)

    #print(move("A", "7", NUMERIC_PAD))
    print(move("A029A"))