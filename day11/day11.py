import sys
from collections.abc import Iterable

sys.path.append("..")
from aoc import Logger

class Stones:
    data: list[int]

    def __init__(self, items: Iterable[int]):
        self.data = list(items)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        return str(self.data)

    def _calc_next(self, x: int):
        if x == 0:
            return [1]
        xs = str(x)
        n = len(xs)
        if n % 2 == 0:
            return [int(xs[:n//2]), int(xs[n//2:])]
        return [x * 2024]

    def blink(self):
        out = []
        for x in self.data:
            out.extend(self._calc_next(x))
        return type(self)(out)

    def blinkn(self, n: int):
        xs = self
        for _ in range(n):
            xs = xs.blink()
        return xs

    @classmethod
    def from_string(cls, s):
        return cls(int(x) for x in s.split())

if __name__ == '__main__':
    test = Stones([125, 17])
    t = test
    print(t)
    for _ in range(6):
        t = t.blink()
        print(t)
    print(len(test.blinkn(25)))

    inp = Stones.from_string("965842 9159 3372473 311 0 6 86213 48")
    print(inp)
    print(len(inp.blinkn(25)))