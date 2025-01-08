import re
import sys
from dataclasses import dataclass

import aoc

sys.path.append("..")
from aoc import Logger

@dataclass
class Program:
    A: int
    B: int
    C: int
    register0: dict[str, int]
    program: list[int]

    PATT_REGISTER = re.compile(r"Register (.): (\d+)")

    def __init__(self, filename):
        xs1, xs2 = aoc.split_xs(aoc.read_lines(filename), "")
        self.register0 = self._read_register(xs1)
        self.program = self._read_program(xs2[0])
        self.init()

    def _read_register(self, xs):
        register = dict()
        for x in xs:
            m = type(self).PATT_REGISTER.match(x)
            if m:
                name = m.group(1)
                value = int(m.group(2))
                register[name] = value
        return register

    def _read_program(self, s):
        _, values = s.split(": ")
        return list(int(x) for x in values.split(","))

    def init(self):
        self.A = self.register0["A"]
        self.B = self.register0["B"]
        self.C = self.register0["C"]

    def literal(self, ptr):
        return self.program[ptr]

    def combo(self, ptr):
        x = self.program[ptr]
        if 0 <= x <= 3:
            return x
        elif x == 4:
            return self.A
        elif x == 5:
            return self.B
        elif x == 6:
            return self.C
        else:
            raise Exception()

    def eval(self, A=None):
        self.init()
        if A is not None:
            self.A = A
        out = []
        ptr = 0
        while 0 <= ptr < len(self.program):
            opcode = self.literal(ptr)
            #operand = self.program[ptr+1]
            if opcode == 0:
                # adv
                operand = self.combo(ptr+1)
                self.A = self.A // (2 ** operand)
            elif opcode == 1:
                # bxl
                operand = self.literal(ptr+1)
                self.B = self.B ^ operand
            elif opcode == 2:
                # bst
                operand = self.combo(ptr+1)
                self.B = operand % 8
            elif opcode == 3:
                # jnz
                if self.A != 0:
                    ptr = self.literal(ptr+1)
                    continue
            elif opcode == 4:
                # bxc
                self.B = self.B ^ self.C
            elif opcode == 5:
                # out
                out.append(self.combo(ptr+1) % 8)
            elif opcode == 6:
                # bdv
                operand = self.combo(ptr+1)
                self.B = self.A // (2 ** operand)
            elif opcode == 7:
                # cdv
                operand = self.combo(ptr+1)
                self.C = self.A // (2 ** operand)
            ptr += 2
        return ",".join(str(x) for x in out)



if __name__ == '__main__':
    print("-- test --")
    test = Program("test.txt")
    print(test)
    print("part 1")
    print(test.eval())
    print("part 2")
    test2 = Program("test2.txt")
    for a in range(2024, 2024+100):
        print(a, test2.eval(A=a))

    print()
    print("-- input --")
    inp = Program("input.txt")
    print(inp)
    print("part 1")
    print(inp.eval())
    print("part 2")
    A0 = inp.register0["A"]
    for a in range(A0, A0+100):
        print(a, inp.eval(A=a))