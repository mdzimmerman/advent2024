import sys

sys.path.append("..")
from aoc import Logger, Point

class Grid:
    def __init__(self, filename: str, logger: Logger=Logger()):
        self.filename = filename
        self.logger = logger
        self.data = self._get_data(filename)
        self.width = len(self.data[0])
        self.height = len(self.data)

    def _get_data(self, filename):
        out = []
        with open(filename, "r") as fh:
            for l in fh:
                l = l.strip()
                out.append(l)
        return out

    def print(self):
        for l in self.data:
            print(l)

    def get(self, p: Point):
        if 0 <= p.y < self.height and 0 <= p.x < self.width:
            return self.data[p.y][p.x]
        else:
            return ""

    def part1(self):
        matches = 0
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if self.get(p) == 'X':
                    for d in Point.MOVES_DIAG:
                        s = "".join(self.get(pn) for pn in p.move_n(d, 3))
                        if s == "MAS":
                            self.logger.debug(p, d)
                            matches += 1
        return matches

    def part2(self):
        matches = 0
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if self.get(p) == 'A':
                    s1 = "".join(self.get(pn) for pn in [p.move("NW"), p, p.move("SE")])
                    s2 = "".join(self.get(pn) for pn in [p.move("SW"), p, p.move("NE")])
                    if (s1 == "MAS" or s1 == "SAM") and (s2 == "MAS" or s2 == "SAM"):
                        self.logger.debug(p)
                        matches += 1
        return matches

if __name__ == '__main__':
    center = Point(10, 10)
    for d in Point.MOVES_DIAG:
        print(d, center.move(d))

    print([x for x in center.move_n("NE", 3)])

    test = Grid("test.txt", logger=Logger("DEBUG"))
    test.print()
    print(test.part1())
    print(test.part2())

    inp = Grid("input.txt")
    print(inp.part1())
    print(inp.part2())