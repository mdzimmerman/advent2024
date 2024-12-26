import re
import sys
from dataclasses import dataclass

import numpy
import matplotlib.pyplot as plt
import networkx as nx

sys.path.append("..")
import aoc
from aoc import Logger


@dataclass
class Conn:
    in1: str
    in2: str
    op: str
    out: str

    PATTERN = re.compile(r"(.+) (AND|OR|XOR) (.+) -> (.+)")

    @classmethod
    def parse(cls, s):
        m = cls.PATTERN.match(s)
        if m:
            in1, op, in2, out = m.groups()
            return cls(in1, in2, op, out)

    def eval(self, in1val, in2val):
        if self.op == 'AND':
            return in1val & in2val
        elif self.op == 'OR':
            return in1val | in2val
        elif self.op == 'XOR':
            return in1val ^ in2val

class Graph:
    initial: dict[str, int]
    connection: list[Conn]
    conn_by_out: dict[str, Conn]

    def __init__(self, filename):
        self.initial, self.connection = self._read_file(filename)
        self.conn_by_out = {c.out: c for c in self.connection}

    def _read_file(self, filename):
        ls1, ls2 = aoc.split_xs(aoc.read_lines(filename), "")
        initial = dict()
        for l in ls1:
            name, val = l.split(": ")
            initial[name] = int(val)
        connection = list(Conn.parse(l) for l in ls2)
        return initial, connection

    def get_value(self, out):
        if out not in self.conn_by_out:
            return self.initial[out]
        else:
            conn = self.conn_by_out[out]
            in1val = self.get_value(conn.in1)
            in2val = self.get_value(conn.in2)
            return conn.eval(in1val, in2val)

    def get_zs(self):
        return sorted(list(filter(lambda s: s[0] == 'z', self.conn_by_out.keys())))

    def part1(self):
        out = 0
        zbits = reversed(list(self.get_value(z) for z in self.get_zs()))
        for b in zbits:
            out = (out << 1) | b
        return(out)

if __name__ == '__main__':
    print("-- test1 --")
    test1 = Graph("test1.txt")
    for ikey, ival in test1.initial.items():
        print(ikey, ival)
    for conn in test1.connection:
        print(conn)
    for z in test1.get_zs():
        print(z, test1.get_value(z))
    print(test1.part1())

    print()
    print("-- test2 --")
    test2 = Graph("test2.txt")
    for z in test2.get_zs():
        print(z, test2.get_value(z))
    print(test2.part1())

    print()
    print("-- input --")
    inp = Graph("input.txt")
    print(inp.part1())