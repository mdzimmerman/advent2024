import re
import sys

sys.path.append("..")
import aoc
from aoc import Logger

class Manual:
    def __init__(self, filename):
        self.filename = filename
        self._read_file(filename)

    def _read_file(self, filename):
        rules, pages = aoc.split_xs(aoc.read_lines(filename), "")
        self.rules = [tuple(int(x) for x in r.split("|")) for r in rules]
        self.before = self._read_rules(rules)
        self.pages = [list(int(x) for x in ps.split(",")) for ps in pages]

    def _read_rules(self, xs):
        before = dict()
        for x in xs:
            a, b = tuple(int(x) for x in x.split("|"))
            if a not in before:
                before[a] = set()
            if b not in before:
                before[b] = set()
            before[b].add(a)
        return before

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
        total = 0
        for ps in self.pages:
            out = []
            for p in ps:
                #print(p)
                if not out:
                    out.append(p)
                else:
                    found = False
                    i = 0
                    while not found and i <= len(out):
                        #print(out[0:i], out[i:])
                        if out[i:] and any(e in self.before[p] for e in out[i:]):
                            i += 1
                        else:
                            found = True
                    out.insert(i, p)
            #print(ps, out, ps == out)
            if ps != out:
                total += self.mid(out)
        return total

    def mid(self, xs):
        return xs[len(xs) // 2]


if __name__ == '__main__':
    print("-- test --")
    test = Manual("test.txt")
    print(test.rules)
    print(test.pages)
    print("part1")
    print(test.part1())
    print("part2")
    print(test.part2())

    print()
    print("-- input --")
    inp = Manual("input.txt")
    print("part1")
    print(inp.part1())
    print("part2")
    print(inp.part2())