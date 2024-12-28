import sys

import aoc

sys.path.append("..")
from aoc import Point, CharArray


class Warehouse:
    grid: CharArray
    walls: set[aoc.Point]
    boxes: set[Point]
    robot: Point
    directions: str

    DIRS = {"<": "W", "^": "N", ">": "E", "v": "S"}

    def __init__(self, filename):
        xs1, xs2 = aoc.split_xs(aoc.read_lines(filename), "")
        self.grid = CharArray(xs1)
        self.walls = set(self.grid.find("#"))
        self.directions = "".join(xs2)
        self.reset()

    def reset(self):
        self.boxes = set(self.grid.find("O"))
        self.robot = list(self.grid.find("@"))[0]

    def print(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                p = Point(x, y)
                if p in self.walls:
                    print("#", end="")
                elif p in self.boxes:
                    print("O", end="")
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
                    self.boxes.remove(stack[0])
                    self.boxes.add(dest)
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
    test = Warehouse("test.txt")
    #test.grid.print()
    #print(test.directions)
    test.print()
    #print()
    #test.move("<")
    #test.print()
    print()
    print(test.part1())
    test.print()

    print()
    print("-- input --")
    inp = Warehouse("input.txt")
    print("part 1")
    print(inp.part1())

