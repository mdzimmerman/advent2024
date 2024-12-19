import math
import sys
from collections import deque

sys.path.append("..")
from aoc import Logger, Point, CharArray, Dir


class Memory:
    def __init__(self, filename: str, width: int, height: int, loglevel="WARN"):
        self.filename = filename
        self.logger = Logger(loglevel)
        self.points = self._parse_file(filename)
        self.width = width
        self.height = height
        #self.grid = self._parse_file(filename, width, height)

    def _parse_file(self, filename):
        points = list()
        with open(filename, "r") as fh:
            for l in fh:
                x, y = (int(e) for e in l.strip().split(","))
                p = Point(x, y)
                self.logger.debug(p)
                points.append(p)
        return points

    def print_grid(self, n):
        npoints = set(self.points[:n])
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                c = '.'
                if p in npoints:
                    c = '#'
                print(c, end="")
            print()

    def in_bounds(self, p):
        return 0 <= p.x < self.width and 0 <= p.y < self.height

    def part1(self, n):
        """Do BFS """
        npoints = set(self.points[:n])
        start = Point(0, 0)
        end = Point(self.width-1, self.height-1)

        seen = set()
        queue = deque()
        queue.append((0, start))

        while queue:
            steps, pos = queue.popleft()
            self.logger.debug(pos, steps)

            if pos in seen:
                continue
            seen.add(pos)

            if pos == end:
                return steps

            for d in Dir.ALL:
                npos = pos.move(d)
                if self.in_bounds(npos) and npos not in npoints:
                    queue.append((steps+1, npos))


    def part2(self):
        """Do a linear search to find the point where the BFS path is blocked."""
        L = 0
        R = len(self.points)
        while (R-L) > 1:
            m = math.floor((L+R)//2)
            steps = self.part1(m)
            self.logger.warn(f"R={R} L={L} m={m} steps={steps}")
            if steps is None:
                R = m
            else:
                L = m
        self.logger.warn(f"R={R} L={L}")
        return self.points[L]


if __name__ == '__main__':
    test = Memory('test.txt', width=7, height=7)
    test.print_grid(12)
    print(test.part1(12))
    print(test.part2())

    inp = Memory('input.txt', width=71, height=71)
    #inp.print_grid(1024)
    print(inp.part1(1024))
    print(inp.part2())