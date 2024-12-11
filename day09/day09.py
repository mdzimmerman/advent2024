from itertools import islice
import sys

sys.path.append("..")
import aoc
from aoc import Logger

def batched(iterable, n):
    """batched('ABCDEFG', 3) → ABC DEF G"""

    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch

class Disk:
    def __init__(self, diskmap, loglevel="WARN"):
        self.logger = Logger(loglevel)
        self.diskmap = diskmap
        self.reset_blocks()

    def reset_blocks(self):
        id = 0
        self.blocks = []
        infile = True
        for x in self.diskmap:
            size = int(x)
            if infile:
                self.blocks.extend([id] * size)
                id += 1
                infile = False
            else:
                self.blocks.extend([None] * size)
                infile = True

    def _next_pd(self, pd):
        npd = pd
        while self.blocks[npd] is not None:
            npd += 1
        return npd

    def _next_ps(self, ps):
        nps = ps
        while self.blocks[nps] is None:
            nps -= 1
        return nps

    def compact(self):
        self.logger.info("len(self.blocks) =", len(self.blocks))
        pd = self._next_pd(0)
        ps = self._next_ps(len(self.blocks)-1)
        i = 0
        while pd <= ps:
            i += 1
            self.logger.info(f"pd = {pd}, ps = {ps}")
            self.logger.debug(self.render_blocks())
            self.blocks[pd] = self.blocks[ps]
            self.blocks[ps] = None
            pd = self._next_pd(pd)
            ps = self._next_ps(ps)
        self.logger.debug(self.render_blocks())

    def checksum(self):
        sum = 0
        for i, id in enumerate(self.blocks):
            if id is None:
                break
            sum += (i * id)
        return sum

    def _block_to_char(self, b) -> str:
        if b is None:
            return "."
        else:
            return str(b % 10)

    def render_blocks(self):
        return "".join(self._block_to_char(b) for b in self.blocks)

    @classmethod
    def from_file(cls, filename, loglevel="WARN"):
        return cls(aoc.read_string(filename), loglevel=loglevel)


if __name__ == '__main__':
    test1 = Disk.from_file("test1.txt", loglevel="DEBUG")
    print(test1.render_blocks())
    test1.compact()
    print(test1.checksum())

    test2 = Disk("12345", loglevel="DEBUG")
    test2.compact()
    print(test2.checksum())

    inp = Disk.from_file("input.txt", loglevel="INFO")
    inp.compact()
    print(inp.checksum())
