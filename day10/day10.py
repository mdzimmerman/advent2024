import sys
from collections import deque

import aoc

sys.path.append("..")
from aoc import Dir, CharArray

def part1(array: CharArray):
    trails = dict()
    for start in array.find(0):
        print(start)
        trails[start] = list()

        #seen = list()
        queue = deque()
        queue.append((start, 0))

        while queue:
            pos, value = queue.popleft()
            #if pos in seen:
            #    continue
            #seen.add(pos)
            if value == 9:
                trails[start].append(pos)
            else:
                for d in Dir.ALL:
                    npos = pos.move(d)
                    if array.in_bounds(npos):
                        nvalue = array.get(npos)
                        if nvalue == value+1:
                            queue.append((npos, nvalue))

    count = 0
    for start, ends in trails.items():
        count += len(ends)
    return count

if __name__ == '__main__':
    test = aoc.CharArray.from_file_int("test.txt")
    test.print()
    print(part1(test))

    inp = aoc.CharArray.from_file_int("input.txt")
    inp.print()
    print(part1(inp))