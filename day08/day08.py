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

    def find_antinodes(self, p1: Point, p2: Point):
        fs
        delta = p2 - p1
        a1 = p1 - delta
        a2 = p2 + delta
        return {a1, a2}

if __name__ == '__main__':
    test = Antennas.from_file("test.txt")
    antinodes = test.find_antinodes(test.antennas["A"][0], test.antennas["A"][1])
    test.print(overset=antinodes)
    for k, v in test.antennas.items():
        print(k, v)
