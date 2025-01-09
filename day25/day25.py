import sys
from dataclasses import dataclass

import aoc

sys.path.append("..")
from aoc import Logger

@dataclass
class Lockset:
    tumblers: list[int]
    identity: str

    def __init__(self, schematic: list[str]):
        if schematic[0] == "....." and schematic[-1] == "#####":
            self.identity = 'key'
        elif schematic[0] == "#####" and schematic[-1] == ".....":
            self.identity = 'lock'
        else:
            raise Exception("bad input schematic")
        self.tumblers = self._parse_schematic(schematic)

    def _parse_schematic(self, schematic: list[str]):
        tumblers = [0] * 5
        for j in range(5, 0, -1):
            for i in range(0, 5):
                if schematic[j][i] == "#":
                    tumblers[i] += 1
        return tumblers


class Locksets:
    keys: list[Lockset]
    locks: list[Lockset]

    def __init__(self, filename):
        xss = aoc.split_xs(aoc.read_lines(filename), "")
        self.keys = []
        self.locks = []
        for xs in xss:
            ls = Lockset(xs)
            if ls.identity == 'lock':
                self.locks.append(ls)
            elif ls.identity == 'key':
                self.keys.append(ls)

    def valid_pairs(self):
        nvalid = 0
        for k in self.keys:
            for l in self.locks:
                valid = True
                for i in range(5):
                    if k.tumblers[i] + l.tumblers[i] > 5:
                        valid = False
                        break
                if valid:
                    nvalid += 1
                    #print(k, l)
        return nvalid

if __name__ == '__main__':
    print("-- test --")
    test = Locksets("test.txt")
    for t in test.locks:
        print(t)
    for t in test.keys:
        print(t)
    print("part 1")
    print(test.valid_pairs())

    print()
    print("-- input --")
    inp = Locksets("input.txt")
    print("part 1")
    print(inp.valid_pairs())