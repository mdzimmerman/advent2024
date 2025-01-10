import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Any

sys.path.append("..")
import aoc
from aoc import CharArray, Point, PriorityQueue

@dataclass(frozen=True)
class State:
    pos: Point
    dir: str

@dataclass(order=True)
class Item:
    score: int
    state: State=field(compare=False)
    prevstate: State=field(compare=False)

def count_path_pos(starts, seen):
    seenpos = set()
    queue = deque()
    for s in starts:
        queue.append(s)

    while queue:
        state = queue.popleft()
        print(state)
        seenpos.add(state.pos)
        if state in seen and seen[state] is not None:
            for nstate in seen[state]:
                queue.append(nstate)

    return seenpos

def part1(maze: CharArray):
    start = list(maze.find("S"))[0]
    end = list(maze.find("E"))[0]
    #print(start)
    #print(end)

    startstate = State(start, "E")
    seen = dict()
    queue = PriorityQueue()
    queue.append(Item(0, startstate, None))

    bestscore = None
    endstates = set()

    while queue:
        item = queue.popleft()
        #print(item)
        if bestscore is not None and item.score > bestscore:
            break

        if item.state in seen:
            seen[item.state].add(item.prevstate)
            continue
        else:
            seen[item.state] = set()
            seen[item.state].add(item.prevstate)

        spos = item.state.pos
        sdir = item.state.dir
        if spos == end:
            endstates.add(item.state)
            if bestscore is None:
                bestscore = item.score

        else:
            # moves
            # straight first
            npos = spos.move(sdir)
            if maze.get(npos) != '#':
                queue.append(Item(item.score+1, State(npos, sdir), State(spos, sdir)))
            # then turns
            for ndir in (aoc.Dir.rot_cw(sdir), aoc.Dir.rot_ccw(sdir)):
                queue.append(Item(item.score+1000, State(spos, ndir), State(spos, sdir)))

    allpaths = count_path_pos(endstates, seen)

    return bestscore, allpaths

if __name__ == '__main__':
    test1 = CharArray.from_file("test1.txt")
    tscore, tpaths = part1(test1)
    print(tscore, len(tpaths))
    test1.print(overset=tpaths, overchar="O")

    test2 = CharArray.from_file("test2.txt")
    tcore, tpaths = part1(test2)
    print(tpaths)
    print(tscore, len(tpaths))
    test2.print(overset=tpaths, overchar="O")

    inp = CharArray.from_file("input.txt")
    #print(part1(inp))

