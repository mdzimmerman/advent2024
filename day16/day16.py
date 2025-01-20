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
    seen = set()
    prev = dict()
    prev[startstate] = set()
    queue = PriorityQueue()
    queue.append(Item(0, startstate))

    score = None
    while queue:
        item = queue.popleft()

        if item.state in seen:
            continue
        seen.add(item.state)

        spos = item.state.pos
        sdir = item.state.dir
        if spos == end:
            score = item.score
            break

        # moves
        npos = spos.move(sdir)
        if maze.get(npos) != '#':
            nstate = State(npos, sdir)
            if nstate not in prev:
                prev[nstate] = set()
            prev[nstate].add(item.state)
            queue.append(Item(item.score+1, State(npos, sdir)))
        for ndir in (aoc.Dir.rot_cw(sdir), aoc.Dir.rot_ccw(sdir)):
            if maze.get(spos.move(ndir)) != '#':
                nstate = State(spos, ndir)
                if nstate not in prev:
                    prev[nstate] = set()
                prev[nstate].add(item.state)
                queue.append(Item(item.score+1000, State(spos, ndir)))

    best = get_best(prev, end)

    return score, best

def get_best(prev, end):
    best = set()
    queue = deque()
    queue.extend(filter(lambda x: x.pos == end, (x for x in prev.keys())))
    seen = set()
    while queue:
        state = queue.popleft()
        if state in seen:
            continue
        seen.add(state)
        print(state)
        best.add(state.pos)
        for nstate in prev[state]:
            queue.append(nstate)

    return best

if __name__ == '__main__':
    test1 = CharArray.from_file("test1.txt")
    print(part1(test1))
    score, best = part1(test1)
    print(score)
    test1.print(overset=best, overchar="O")

    inp = CharArray.from_file("input.txt")
    #print(part1(inp))

