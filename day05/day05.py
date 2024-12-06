import re
import sys

sys.path.append("..")
import aoc
from aoc import Logger

class Manual:
    def __init__(self, filename):
        self.filename = filename
        self.rules, self.pages = self._read_file(filename)

    def _read_file(self, filename):
        rules, pages = aoc.split_xs(aoc.read_lines(filename), "")
        return [tuple(int(x) for x in r.split("|")) for r in rules], [list(int(x) for x in ps.split(",")) for ps in pages]

    def part1(self):
        out = 0
        for ps in self.pages:
            pindex = dict()
            for i, p in enumerate(ps):
                pindex[p] = i
            valid = True
            for r in self.rules:
                a, b = r
                if a in pindex and b in pindex:
                    if pindex[a] >= pindex[b]:
                        valid = False
                        break
            #print(ps, valid)
            if valid:
               out += self.mid(ps)
        return out

    def part2(self):
        r

    def mid(self, xs):
        return xs[len(xs) // 2]


if __name__ == '__main__':
    test = Manual("test.txt")
    print(test.rules)
    print(test.pages)
    print(test.part1())

    inp = Manual("input.txt")
    print(inp.part1())