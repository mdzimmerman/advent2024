import sys
from collections import deque
from collections.abc import Hashable, MutableSet, Iterable
from dataclasses import dataclass

sys.path.append("..")
from aoc import CharArray, Dir, Point, Logger

class PointSet(MutableSet):
    def __init__(self, iterable: Iterable[Point]=()):
        self.data: set[Point] = set(iterable)
        self._update_bounds()

    def _update_bounds(self):
        self.xmin: int = None
        self.xmax: int = None
        self.ymin: int = None
        self.ymax: int = None
        for item in self.data:
            self._update_bounds_point(item)

    def _update_bounds_point(self, item):
        if self.xmin is None or item.x < self.xmin:
            self.xmin = item.x
        if self.xmax is None or item.x > self.xmax:
            self.xmax = item.x
        if self.ymin is None or item.y < self.ymin:
            self.ymin = item.y
        if self.ymax is None or item.y > self.ymax:
            self.ymax = item.y

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

    def add(self, item: Point):
        self.data.add(item)
        self._update_bounds_point(item)

    def discard(self, item: Point):
        self.data.discard(item)
        self._update_bounds()

    def get_row(self, y):
        return sorted(filter(lambda p: p.y == y, self.data), key=lambda p: p.x)

    def get_col(self, x):
        return sorted(filter(lambda p: p.x == x, self.data), key=lambda p: p.y)

    def print(self):
        for y in range(self.ymin, self.ymax+1):
            for x in range(self.xmin, self.xmax+1):
                p = Point(x, y)
                if p in self.data:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

@dataclass
class Region:
    name: str
    area: int
    perimeter: int
    fence: dict[str,PointSet]

    def price(self):
        return self.area * self.perimeter

    def price2(self):
        return self.area * self.fence_segments()

    def _count_segments(self, xs):
        segments = []
        if len(xs) > 0:
            segments.append([xs[0], xs[0]])
            for x in xs[1:]:
                if segments[-1][1]+1 == x:
                    segments[-1][1] = x
                else:
                    segments.append([x, x])
        #print(segments)
        return len(segments)

    def fence_segments(self):
        out = 0
        for d in ["N", "S"]:
            fence = self.fence[d]
            for y in range(fence.ymin, fence.ymax+1):
                xs = [p.x for p in fence.get_row(y)]
                out += self._count_segments(xs)
        for d in ["E", "W"]:
            fence = self.fence[d]
            for x in range(fence.xmin, fence.xmax+1):
                ys = [p.y for p in fence.get_col(x)]
                out += self._count_segments(ys)
        return out


def find_regions(grid: CharArray):
    """ """

    seen = set()
    regions = list()
    queue = deque()
    for y in range(grid.height):
        for x in range(grid.width):
            start = Point(x, y)
            if start not in seen:
                name = grid.get(start)
                region = Region(name, 0, 0, dict())

                queue.append(start)

                while queue:
                    pos = queue.popleft()

                    if pos in seen:
                        continue
                    seen.add(pos)

                    region.area += 1
                    for d in Dir.ALL:
                        npos = pos.move(d)
                        nname = grid.get(npos)
                        if nname == name:
                            queue.append(npos)
                        else:
                            region.perimeter += 1
                            if d not in region.fence:
                                region.fence[d] = PointSet()
                            region.fence[d].add(pos)

                regions.append(region)
    return regions

def part1(grid):
    regions = find_regions(grid)
    return(sum(r.price() for r in regions))

def part2(grid):
    regions = find_regions(grid)
    return(sum(r.price2() for r in regions))

if __name__ == '__main__':
    print("-- test1 --")
    test1 = CharArray.from_file("test1.txt")
    test1.print()
    #for r in find_regions(test1):
    #    print(r)
    #    print(r.fence_segments())
    print(part1(test1))
    print(part2(test1))

    print()
    print("-- test3 --")
    test3 = CharArray.from_file("test3.txt")
    test3.print()
    #for r in find_regions(test3):
    #    print(r)
    #    print(r.fence_segments())
    print(part1(test3))
    print(part2(test3))

    print()
    print("-- input --")
    inp = CharArray.from_file("input.txt")
    print(part1(inp))
    print(part2(inp))