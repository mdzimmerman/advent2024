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

    def find_antinodes(self):
        antinodes = set()
        for aname, apoints in self.antennas.items():
            self.logger.debug(aname, apoints)
            for i in range(len(apoints)-1):
                for j in range(i+1, len(apoints)):
                    pi = apoints[i]
                    pj = apoints[j]
                    self.logger.debug(pi, pj)
                    delta = pj - pi
                    antinodes.add(pi - delta)
                    antinodes.add(pj + delta)
        return set(filter(lambda p: self.in_bounds(p), antinodes))

if __name__ == '__main__':
    test = Antennas.from_file("test.txt", loglevel="DEBUG")
    antinodes = test.find_antinodes()
    test.print(overset=antinodes)
    print(len(antinodes))

    inp = Antennas.from_file("input.txt")
    antinodes = inp.find_antinodes()
    print(len(antinodes))