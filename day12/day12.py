import sys
from collections import deque
from dataclasses import dataclass

sys.path.append("..")
from aoc import CharArray, Dir, Point, Logger

@dataclass
class Region:
    name: str
    area: int
    perimeter: int

    def price(self):
        return self.area * self.perimeter

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
                region = Region(name, 0, 0)

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

                regions.append(region)

    return regions

def part1(grid):
    regions = find_regions(grid)
    return(sum(r.price() for r in regions))

if __name__ == '__main__':
    test1 = CharArray.from_file("test1.txt")
    test1.print()
    print(part1(test1))

    test3 = CharArray.from_file("test3.txt")
    print(part1(test3))

    inp = CharArray.from_file("input.txt")
    print(part1(inp))