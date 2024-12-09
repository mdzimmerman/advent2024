import sys
from dataclasses import dataclass
import itertools

sys.path.append("..")

@dataclass
class Equation:
    total: int
    terms: list[int]

    @classmethod
    def parse(cls, s):
        s1, s2 = s.split(": ")
        total = int(s1)
        terms = [int(x) for x in s2.split()]
        return cls(total, terms)

    def eval(self, *ops):
        t = self.terms[0]
        for i in range(len(self.terms)-1):
            if ops[i] == "*":
                t *= self.terms[i+1]
            elif ops[i] == "+":
                t += self.terms[i+1]
            elif ops[i] == "|":
                t = int(str(t) + str(self.terms[i+1]))
            else:
                raise Exception("bad op")
        return t

    def isvalid(self, avail_ops="+*"):
        nops = len(self.terms)-1
        for ops in itertools.product(avail_ops, repeat=nops):
            if self.eval(*ops) == self.total:
                return True
        return False

class Equations:
    def __init__(self, filename):
        self.filename = filename
        self.equations = self._from_file(filename)

    def _from_file(self, filename):
        out = []
        with open(filename, "r") as fh:
            for l in fh:
                out.append(Equation.parse(l.strip()))
        return out

    def part1(self):
        out = 0
        for eq in self.equations:
            if eq.isvalid():
                out += eq.total
        return out

    def part2(self):
        out = 0
        for eq in self.equations:
            if eq.isvalid(avail_ops="+*|"):
                out += eq.total
        return out

if __name__ == '__main__':
    test = Equations("test.txt")
    for t in test.equations:
        print(t, t.isvalid(avail_ops="+*|"))
    print(test.part1())
    print(test.part2())

    inp = Equations("input.txt")
    print(inp.part1())
    print(inp.part2())