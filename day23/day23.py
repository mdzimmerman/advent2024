import sys

sys.path.append("..")

import aoc
#from aoc import Logger

class Graph:
    nodes: list[str]
    neighbors: dict[str, set[str]]
    tnodes: set[str]

    def __init__(self, filename):
        self.nodes, self.neighbors, self.tnodes = self._read_file(filename)

    def _read_file(self, filename):
        nodes = list()
        neighbors = dict()
        tnodes = set()
        for s in aoc.read_lines(filename):
            a, b = s.split("-")
            if a not in nodes:
                nodes.append(a)
                neighbors[a] = set()
            if b not in nodes:
                nodes.append(b)
                neighbors[b] = set()
            neighbors[a].add(b)
            neighbors[b].add(a)
        for n in nodes:
            if n[0] == "t":
                tnodes.add(n)
        return sorted(nodes), neighbors, tnodes

    def part1(self):
        count = 0
        nnodes = len(self.nodes)
        for i in range(nnodes-2):
            for j in range(i+1, nnodes-1):
                for k in range(j+1, nnodes):
                    ni = self.nodes[i]
                    nj = self.nodes[j]
                    nk = self.nodes[k]
                    if nj in self.neighbors[ni] and nk in self.neighbors[nj] and ni in self.neighbors[nk]:
                        if {ni, nj, nk}.intersection(self.tnodes):
                            count += 1
                            print(ni, nj, nk)
        return count

if __name__ == '__main__':
    test = Graph("test.txt")
    print(test.nodes)
    print(test.tnodes)
    for k, v in test.neighbors.items():
        print(k, v)
    print(test.part1())

    print()
    inp = Graph("input.txt")
    print(inp.part1())
