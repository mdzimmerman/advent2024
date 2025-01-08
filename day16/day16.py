import sys
from dataclasses import dataclass, field
from typing import Any

sys.path.append("..")
import aoc
from aoc import CharArray, Point, PriorityQueue

@dataclass(order=True)
class Item:
    score: int
    state: Any=field(compare=False)
    prev: Any=field(compare=False)

def part1(maze: CharArray):
    start = list(maze.find("S"))[0]
    end = list(maze.find("E"))[0]
    #print(start)
    #print(end)

    startstate = (start, "E")
    seen = set()
    queue = PriorityQueue()
    queue.append(Item(0, startstate, None))

    bestscore = None
    allpaths = set()

    while queue:
        item = queue.popleft()
        if bestscore is not None and item.score > bestscore:
            break

        if item.state in seen:
            continue
        #seen.add(item.state)

        spos, sdir = item.state
        if spos == end:
            if bestscore is None:
                bestscore = item.score
            while item is not None:
                pos = item.state[0]
                allpaths.add(pos)
                item = item.prev
        else:
            # moves
            npos = spos.move(sdir)
            if maze.get(npos) != '#':
                queue.append(Item(item.score+1, (npos, sdir), item))
            for ndir in (aoc.Dir.rot_cw(sdir), aoc.Dir.rot_ccw(sdir)):
                queue.append(Item(item.score+1000, (spos, ndir), item))

    return bestscore, allpaths

if __name__ == '__main__':
    test1 = CharArray.from_file("test1.txt")
    tscore, tpaths = part1(test1)
    print(tscore, len(tpaths))
    test1.print(overset=tpaths, overchar="O")

    test2 = CharArray.from_file("test2.txt")
    tcore, tpaths = part1(test2)
    print(tscore, len(tpaths))
    test2.print(overset=tpaths, overchar="O")

    inp = CharArray.from_file("input.txt")
    #print(part1(inp))

