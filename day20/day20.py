import sys
from collections import deque

sys.path.append("..")
from aoc import Logger, CharArray, Dir, Point


class Maze:
    filename: str
    grid: CharArray
    path: dict[Point, int]
    path_steps: list[Point]

    def __init__(self, filename: str):
        self.filename = filename
        self.grid = CharArray.from_file(filename)
        self.path, self.path_steps = self._build_path_bfs()

    def _build_path_bfs(self):
        start = list(self.grid.find("S"))[0]

        #end = self.grid.find("E")

        seen = set()
        path = dict()
        queue = deque()
        queue.append((0, start))

        while queue:
            steps, pos = queue.popleft()
            if pos in seen:
                continue

            seen.add(pos)
            path[pos] = steps

            for d in Dir.ALL:
                npos = pos.move(d)
                if self.grid.get(npos) != '#':
                    queue.append((steps+1, npos))

        path_steps = [None] * len(path.items())
        for pos, n in path.items():
            path_steps[n] = pos
        return path, path_steps

    def move2(self, pos):
        moves = [(-2,  0),
                 (-1, -1),
                 ( 0, -2),
                 ( 1, -1),
                 ( 2,  0),
                 ( 1,  1),
                 ( 0,  2),
                 (-1,  1)]
        for ndiff in moves:
            npos = pos + ndiff
            if self.grid.in_bounds(pos + ndiff):
                yield npos

    def part1(self, dtlimit=100):
        #start = list(self.grid.find("S"))[0]
        hist = dict()
        for spos, steps in self.path.items():
            for epos in self.move2(spos):
                if epos in self.path and self.path[epos] > (steps+2):
                    dt = self.path[epos] - (steps+2)
                    #print(spos, epos, dt)
                    if dt not in hist:
                        hist[dt] = 0
                    hist[dt] += 1
        total = 0
        for k in sorted(hist.keys()):
            #print(k, hist[k])
            if k >= dtlimit:
                total += hist[k]
        return total

    def part2(self, dtlimit=50):
        hist = dict()
        nsteps = len(self.path_steps)
        for i in range(nsteps-1):
            spos = self.path_steps[i]
            for j in range(i, nsteps):
                epos = self.path_steps[j]
                d = spos.dist(epos)
                dt = (j-i)-d
                if d <= 20 and dt > 0:
                    #print(spos, epos, d, dt)
                    if dt not in hist:
                        hist[dt] = 0
                    hist[dt] += 1
        total = 0
        for k in sorted(hist.keys()):
            if k >= dtlimit:
                #print(k, hist[k])
                total += hist[k]
        return total

        #for npos in self.move2(start):
        #    print(npos)


if __name__ == '__main__':
    print("-- test --")
    test = Maze("test.txt")
    #for p, n in test.path.items():
    #    print(p, n)
    print(test.part1())
    #test.grid.print()
    #for p in test.path_steps:
    #    print(p)
    print(test.part2())

    print()
    print("-- input --")
    inp = Maze("input.txt")
    print(inp.part1())
    print(inp.part2(dtlimit=100))