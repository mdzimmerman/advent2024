import re
import sys
import time
from dataclasses import dataclass

import aoc

sys.path.append("..")
from aoc import Point, Logger

@dataclass(frozen=True
           )
class Robot:
    p: Point
    v: Point

    PATTERN = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

    @classmethod
    def parse(cls, s):
        m = cls.PATTERN.match(s)
        if m:
            px, py, vx, vy = tuple(int(n) for n in m.groups())
            return cls(Point(px, py), Point(vx, vy))

    def move(self, t, w, h):
        np = self.p + self.v * t
        np = Point(np.x % w, np.y % h)
        return Robot(np, self.v)

class Ensemble:
    filename: str
    robots: list[Robot]
    width: int
    height: int

    def __init__(self, filename, width, height):
        self.filename = filename
        self.robots = [Robot.parse(l) for l in aoc.read_lines(filename)]
        self.width = width
        self.height = height

    def move(self, t):
        return list(r.move(t, self.width, self.height) for r in self.robots)

    def count(self, robots):
        out = dict()
        for r in robots:
            if r.p not in out:
                out[r.p] = 0
            out[r.p] += 1
        return out

    def print(self, robots):
        c = self.count(robots)
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p in c:
                    print(c[p] % 10, end="")
                else:
                    print(".", end="")
            print()

    def partition(self, robots):
        xmid = self.width // 2
        ymid = self.height // 2
        q = [0, 0, 0, 0]
        for r in robots:
            pt = r.p
            if   pt.x < xmid and pt.y < ymid:
                q[0] += 1
            elif pt.x > xmid and pt.y < ymid:
                q[1] += 1
            elif pt.x < xmid and pt.y > ymid:
                q[2] += 1
            elif pt.x > xmid and pt.y > ymid:
                q[3] += 1
        return q[0] * q[1] * q[2] * q[3]

    def count_touching(self, robots):
        count = 0
        rpos = list(r.p for r in robots)
        for i in range(len(rpos)-1):
            for j in range(i+1, len(rpos)):
                d = rpos[i].dist(rpos[j])
                if d == 1:
                    count += 1
        return count

if __name__ == '__main__':
    print("-- test --")
    test = Ensemble("test.txt", width=11, height=7)
    for r in test.robots:
        print(r)
    test.print(test.robots)
    print()
    robots100 = test.move(100)
    test.print(robots100)
    print("part 1")
    print(test.partition(robots100))

    print()
    print("-- input --")
    inp = Ensemble("input.txt", width=101, height=103)
    robots100 = inp.move(100)
    print("part 1")
    print(inp.partition(robots100))
    print("part 2")
    #imax = 0
    #pmax = 0
    #def calc_hash(rs):
    #    return sum(hash(r) for r in rs)

    #def count_touching(robots, ):
    #    rpos = sorted(r.p for r in robots)
    #    for x in range()

    cycle = dict()
    cmax = 0
    imax = 0
    for i in range(11_000):
        if i % 1_000 == 0:
            print(i)
        rs = inp.move(i)
        c = inp.count_touching(rs)
        print(i, inp.count_touching(rs))
        if c > cmax:
            cmax = c
            imax = i

    inp.print(inp.move(imax))
    print(imax)