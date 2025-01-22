import sys
from collections import deque
from dataclasses import dataclass, field

sys.path.append("..")
import aoc
from aoc import CharArray, Point, Dir, PriorityQueue

@dataclass(frozen=True)
class State:
    pos: Point
    dir: str

    def forward(self):
        return State(self.pos.move(self.dir), self.dir)

    def rot_cw(self):
        return State(self.pos, Dir.rot_cw(self.dir))

    def rot_ccw(self):
        return State(self.pos, Dir.rot_ccw(self.dir))

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

def solve(maze: CharArray):
    start = list(maze.find("S"))[0]
    end = list(maze.find("E"))[0]

    startstate = State(start, "E")
    seen = dict()
    prev = dict()
    prev[startstate] = set()
    queue = PriorityQueue()
    queue.append(Item(0, startstate))

    score = None
    while queue:
        item = queue.popleft()

        if item.state in seen:
            continue
        seen[item.state] = item.score

        if item.state.pos == end:
            score = item.score
            break

        # moves
        nstates = [(item.state.forward(), item.score+1),
                   (item.state.rot_cw(),  item.score+1000),
                   (item.state.rot_ccw(), item.score+1000)]

        for nstate, nscore in nstates:
            if maze.get(nstate.pos) != '#':
                if nstate not in prev:
                    prev[nstate] = set()
                if nstate not in seen: # or seen[nstate] > nscore:
                    prev[nstate].add(item.state)
                queue.append(Item(nscore, nstate))

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
        #print(state)
        best.add(state.pos)
        for nstate in prev[state]:
            queue.append(nstate)

    return best

if __name__ == '__main__':
    print("-- test 1 --")
    test1 = CharArray.from_file("test1.txt")
    score, best = solve(test1)
    print(f"score = {score}")
    print(f"best = {len(best)}")
    test1.print(overset=best, overchar="O")

    print()
    print("-- test 2 --")
    test2 = CharArray.from_file("test2.txt")
    score, best = solve(test2)
    print(f"score = {score}")
    print(f"best = {len(best)}")
    test2.print(overset=best, overchar="O")

    print()
    print("-- input --")
    inp = CharArray.from_file("input.txt")
    score, best = solve(inp)
    print(f"score = {score}")
    print(f"best = {len(best)}")
    inp.print(overset=best, overchar="O")

