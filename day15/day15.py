import sys

import aoc

sys.path.append("..")
from aoc import Point, CharArray


class Warehouse:
    grid: CharArray
    walls: set[aoc.Point]
    boxes: dict[Point, str]
    robot: Point
    directions: str

    DIRS = {"<": "W", "^": "N", ">": "E", "v": "S"}

    def __init__(self, filename, expand=False):
        xs1, xs2 = aoc.split_xs(aoc.read_lines(filename), "")
        self.grid = self._parse_grid(xs1, expand)
        self.walls = set(self.grid.find("#"))
        self.directions = "".join(xs2)
        self.reset()

    def _parse_grid(self, xs, expand=False):
        if not expand:
            return CharArray(xs)
        else:
            EXPANSION = {"#": "##", ".": "..", "O": "[]", "@": "@."}
            data = []
            for x in xs:
                data.append("")
                for c in x:
                    data[-1] += EXPANSION[c]
            return CharArray(data)

    def reset(self):
        self.boxes = dict()
        for p, c in self.grid.enumerate():
            if c == 'O' or c == '[' or c == ']':
                self.boxes[p] = c
        self.robot = list(self.grid.find("@"))[0]

    def print(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                p = Point(x, y)
                if p in self.walls:
                    print("#", end="")
                elif p in self.boxes:
                    print(self.boxes[p], end="")
                elif p == self.robot:
                    print("@", end="")
                else:
                    print(".", end="")
            print()

    def move(self, dir):
        d = self.DIRS[dir]
        dest = self.robot.move(d)
        stack = []
        while True:
            if dest in self.walls:
                # can't move
                return False
            elif dest in self.boxes:
                stack.append(dest)
                dest = dest.move(d)
            else:
                # can move stack
                if stack:
                    for s in reversed(stack):
                        self.boxes[s.move(d)] = self.boxes[s]
                        del self.boxes[s]
                self.robot = self.robot.move(d)
                return True

    def gps(self):
        return sum(100 * b.y + b.x for b in self.boxes)

    def part1(self):
        self.reset()
        for d in self.directions:
            self.move(d)
        return self.gps()

if __name__ == '__main__':
    print("-- test --")
    print("part 1")
    test = Warehouse("test.txt")
    test.print()
    print()
    print(test.part1())
    test.print()

    print("part 2")
    testx = Warehouse("test.txt", expand=True)
    testx.print()
    testx.move("<")
    print()
    testx.print()
    testx.move("^")
    print()
    testx.print()


    print()
    print("-- input --")
    inp = Warehouse("input.txt")
    print("part 1")
    print(inp.part1())

