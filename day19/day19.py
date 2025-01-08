import functools
import sys
from dataclasses import dataclass, field
from typing import Any

sys.path.append("..")
import aoc
from aoc import Logger, PriorityQueue


@dataclass(order=True)
class Item:
    score: int
    design: str
    patterns: Any=field(compare=False)

class Towels:
    patterns: dict[int, set[str]]
    pattern_lengths: list[int]
    designs: list[str]
    logger: Logger

    def __init__(self, filename, loglevel="WARN"):
        xs, ys = aoc.split_xs(aoc.read_lines(filename), "")
        self.patterns = self._build_patterns(xs[0])
        self.pattern_lengths = sorted(list(self.patterns.keys()))
        self.designs = ys
        self.logger = Logger(loglevel)

    def _build_patterns(self, s) -> dict[int, set[str]]:
        ps = s.split(", ")
        out = dict()
        for p in ps:
            plen = len(p)
            if plen not in out:
                out[plen] = set()
            out[plen].add(p)
        return out

    @functools.lru_cache(maxsize=None)
    def solutions(self, design):
        ldesign = len(design)
        n = 0
        for i in self.pattern_lengths:
            if i == ldesign:
                if design in self.patterns[i]:
                    n += 1
            elif i < ldesign:
                p = design[:i]
                if p in self.patterns[i]:
                    n += self.solutions(design[i:])
        return n

    def find(self, design):
        queue = PriorityQueue()
        queue.append(Item(len(design), design, ""))

        while queue:
            item = queue.popleft()
            self.logger.debug(item.design, item.patterns)
            if item.score == 0:
                return [item.patterns]
            else:
                for i in self.pattern_lengths:
                    p = item.design[:i]
                    if p in self.patterns[i]:
                        dnew = item.design[i:]
                        psnew = item.patterns
                        if psnew == "":
                            psnew = p
                        else:
                            psnew += ","
                            psnew += p
                        queue.append(Item(len(dnew), dnew, psnew))
        return []

    def part1(self):
        npossible = 0
        for i, design in enumerate(self.designs):
            self.logger.info(i)
            patterns = self.find(design)
            self.logger.debug(design, patterns)
            if len(patterns) > 0:
                npossible += 1
        return npossible

    def part2(self):
        nsolutions = 0
        for i, design in enumerate(self.designs):
            n = self.solutions(design)
            self.logger.debug(design, n)
            nsolutions += n
        return nsolutions


if __name__ == '__main__':
    print("-- test --")
    test = Towels("test.txt", loglevel="DEBUG")
    print(test.patterns)
    print(test.designs)
    print("part 1")
    print(test.part1())
    print("part 2")
    print(test.part2())

    print()
    print("-- input --")
    inp = Towels("input.txt", loglevel="WARN")
    print("part 1")
    print(inp.part1())
    print("part 2")
    print(inp.part2())

