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

if __name__ == '__main__':
    print(NUMERIC_PAD.position)
    print(NUMERIC_PAD.keyname)
    print(DIRECTIONAL_PAD.position)
    print(DIRECTIONAL_PAD.keyname)