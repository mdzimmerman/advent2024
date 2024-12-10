import sys

sys.path.append("..")
from aoc import CharArray, Point

class Antennas(CharArray):
    def __init__(self, data, loglevel="WARN"):
        super().__init__(data, loglevel=loglevel)
        self.antennas = self._build_antennas()

    def _build_antennas(self):
        out = dict()
        for pt, ch in self.enumerate():
            if ch == '.':
                continue
            if ch not in out:
                out[ch] = []
            out[ch].append(pt)
        return out

    def find_antinodes(self, nmin=1, nmax=1):
        antinodes = set()
        for aname, apoints in self.antennas.items():
            self.logger.debug(aname, apoints)
            for i, ai in enumerate(apoints[:-1]):
                for aj in apoints[i+1:]:
                    self.logger.debug(ai, aj)
                    delta = aj - ai
                    n = nmin
                    while n <= nmax and self.in_bounds(ain := ai - delta * n):
                        antinodes.add(ain)
                        n += 1
                    n = nmin
                    while n <= nmax and self.in_bounds(ajn := aj + delta * n):
                        antinodes.add(ajn)
                        n += 1
        return set(filter(lambda p: self.in_bounds(p), antinodes))

    def part1(self):
        antinodes = self.find_antinodes()
        self.debug_array(overset=antinodes)
        return len(antinodes)

    def part2(self):
        antinodes = self.find_antinodes(nmin=0, nmax=1000)
        self.debug_array(overset=antinodes)
        return len(antinodes)


if __name__ == '__main__':
    test = Antennas.from_file("test.txt", loglevel="DEBUG")
    print(test.part1())
    print(test.part2())

    inp = Antennas.from_file("input.txt")
    print(inp.part1())
    print(inp.part2())