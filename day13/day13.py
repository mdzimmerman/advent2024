import re
import sys
from dataclasses import dataclass

sys.path.append("..")
import aoc
from aoc import Logger, Point
import numpy as np

@dataclass
class ClawMachine:
    a: Point
    b: Point
    prize: Point

    PATT_BUTTON = re.compile(r"Button (.): X\+(\d+), Y\+(\d+)")
    PATT_PRIZE  = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    def __init__(self, a: Point, b: Point, prize: Point):
        self.a = a
        self.b = b
        self.prize = prize

    def solve(self):
        out = []
        amax = min(self.prize.x//self.a.x, self.prize.y//self.a.y)
        for i in range(amax+1):
            adeltax = i * self.a.x
            adeltay = i * self.a.y
            bdeltax = self.prize.x - adeltax
            bdeltay = self.prize.y - adeltay
            if (bdeltax % self.b.x) == 0 and (bdeltay % self.b.y) == 0:
                j1 = bdeltax // self.b.x
                j2 = bdeltay // self.b.y
                if j1 == j2:
                    j = j1
                    cost = 3 * i + j
                    out.append((cost, i, j))
        if out:
            return list(sorted(out))[0][0]
        else:
            return 0

    def solve2(self, delta=0):
        A = np.array([[self.a.x, self.b.x], [self.a.y, self.b.y]])
        P = np.array([self.prize.x, self.prize.y]) + delta
        x = np.linalg.solve(A, P)
        i, j = round(x[0]), round(x[1])
        valid = (self.a.x * i + self.b.x * j) == (self.prize.x+delta) and (self.a.y * i + self.b.y * j) == (self.prize.y+delta)
        if valid:
            return 3 * i + j
        else:
            return 0

    @classmethod
    def parse(cls, lines: list[str]):
        out = dict()
        for l in lines[:2]:
            m = cls.PATT_BUTTON.match(l)
            if m:
                button = m.group(1).lower()
                x = int(m.group(2))
                y = int(m.group(3))
                out[button] = Point(x, y)
        m = cls.PATT_PRIZE.match(lines[2])
        if m:
            x = int(m.group(1))
            y = int(m.group(2))
            out["prize"] = Point(x, y)
        return cls(**out)

def readfile(filename):
    return list(ClawMachine.parse(xs) for xs in aoc.split_xs(aoc.read_lines(filename), ""))

if __name__ == '__main__':
    print("-- test --")
    test = readfile("test.txt")
    for m in test:
        print(m)
        print(m.solve2())
        print(m.solve2(delta=10000000000000))
    print(sum(m.solve2() for m in test))
    print(sum(m.solve2(delta=10000000000000) for m in test))

    print()
    print("-- input --")
    inp = readfile("input.txt")
    print(sum(m.solve2() for m in inp))
    print(sum(m.solve2(delta=10000000000000) for m in inp))