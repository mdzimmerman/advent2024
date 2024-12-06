from dataclasses import dataclass
from enum import Enum

class Logger:
    LEVELS = {"WARN": 0, "INFO": 1, "DEBUG": 2}

    def __init__(self, level: str="WARN"):
        cls = self.__class__
        self.nlevel = cls.LEVELS["WARN"]
        if level in cls.LEVELS:
            self.nlevel = cls.LEVELS[level]

    def _print_message(self, *xs, level: str="WARN"):
        cls = self.__class__
        n = cls.LEVELS["WARN"]
        if level in cls.LEVELS:
            n = cls.LEVELS[level]
        if n <= self.nlevel:
            print(f"[{level}]", *xs)

    def warn(self, *xs):
        self._print_message(*xs, level="WARN")

    def info(self, *xs):
        self._print_message(*xs, level="INFO")

    def debug(self, *xs):
        self._print_message(*xs, level="DEBUG")

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    MOVES_SQUARE = ["N", "E", "S", "W"]
    MOVES_DIAG = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    DELTAS = dict(
        N =( 0, -1),
        NE=( 1, -1),
        E =( 1,  0),
        SE=( 1,  1),
        S =( 0,  1),
        SW=(-1,  1),
        W =(-1,  0),
        NW=(-1, -1))

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        else:
            raise TypeError

    def move(self, dir):
        if dir in type(self).DELTAS:
            return self + type(self).DELTAS[dir]
        else:
            raise Exception(f"bad direction '{dir}'")

    def move_n(self, dir, n):
        if dir in type(self).DELTAS:
            curr = self
            for _ in range(n):
                curr = curr.move(dir)
                yield curr

class CharArray:
    def __init__(self, data, logger: Logger = Logger()):
        self.logger = logger
        self.data = data
        self.width = len(self.data[0])
        self.height = len(self.data)

    @classmethod
    def from_file(cls, filename, logger: Logger = Logger()):
        out = []
        with open(filename, "r") as fh:
            for l in fh:
                l = l.strip()
                out.append(l)
        return cls(out, logger=logger)

    def print(self):
        for l in self.data:
            print(l)

    def in_bounds(self, p):
        return 0 <= p.y < self.height and 0 <= p.x < self.width

    def get(self, p: Point, default: str = None):
        if self.in_bounds(p):
            return self.data[p.y][p.x]
        else:
            return default

    def enumerate(self):
        for j in range(self.height):
            for i in range(self.width):
                yield Point(i, j), self.data[j][i]

    def find(self, target):
        for j, row in enumerate(self.data):
            for i, c in enumerate(row):
                if c == target:
                    yield Point(i, j)

@dataclass
class Interval:
    start: int
    end: int

    def __len__(self):
        return self.end - self.start

    def intersect(self, other):
        if self.end <= other.start or other.end <= self.start:
            return None
        else:
            start = max(self.start, other.start)
            end = min(self.end, other.end)
            return Interval(start, end)


def read_lines(filename):
    """Read in each line of a file as an element in a list"""

    lines = []
    with open(filename, "r") as fh:
        for l in fh:
            lines.append(l.rstrip())
    return lines

def read_string(filename):
    return "".join(read_lines(filename))

def split_xs(xs, sep):
    """Split the iterable xs on the separator sep"""
    out = [[]]
    for x in xs:
        if x == sep:
            out.append([])
        else:
            out[-1].append(x)
    return out
