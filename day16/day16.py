import heapq
import sys
from dataclasses import dataclass, field
from typing import Any

sys.path.append("..")
import aoc
from aoc import CharArray

class PriorityQueue():
    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def append(self, item):
        heapq.heappush(self.heap, item)

    def popleft(self):
        return heapq.heappop(self.heap)

@dataclass(order=True)
class Item:
    score: int
    state: Any=field(compare=False)

def part1(maze: CharArray):
    start = list(maze.find("S"))[0]
    end = list(maze.find("E"))[0]
    print(start)
    print(end)

    startstate = (start, "E")
    seen = set()
    queue = PriorityQueue()
    queue.append(Item(0, startstate))

    while queue:
        item = queue.popleft()

        if item.state in seen:
            continue
        seen.add(item.state)

        spos, sdir = item.state
        if spos == end:
            return item.score

        # moves
        npos = spos.move(sdir)
        if maze.get(npos) != '#':
            queue.append(Item(item.score+1, (npos, sdir)))
        for ndir in (aoc.Dir.rot_cw(sdir), aoc.Dir.rot_ccw(sdir)):
            queue.append(Item(item.score+1000, (spos, ndir)))


if __name__ == '__main__':
    test1 = CharArray.from_file("test1.txt")
    print(part1(test1))
    #test1.print()

    inp = CharArray.from_file("input.txt")
    print(part1(inp))

