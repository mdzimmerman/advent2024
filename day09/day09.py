import itertools
from dataclasses import dataclass
from itertools import islice
import sys

sys.path.append("..")
import aoc
from aoc import Logger

@dataclass
class Blocks:
    pos: int
    size: int
    fileid: int

    def render(self):
        if self.fileid is None:
            return "." * self.size
        else:
            return str(self.fileid % 10) * self.size

    def checksum(self):
        if self.fileid is None:
            return 0
        else:
            return sum(self.fileid * x for x in range(self.pos, self.pos + self.size))

class Disk:
    def __init__(self, diskmap, loglevel="WARN"):
        self.logger = Logger(loglevel)
        self.diskmap = diskmap
        self.reset_blocks()

    def reset_blocks(self):
        id = 0
        self.blocks = dict()
        self.prev = dict()
        self.next = dict()
        infile = True
        pos = 0
        for x in self.diskmap:
            size = int(x)
            npos = pos + size
            #self.next[pos] = npos
            #self.prev[npos] = pos
            if infile:
                self.blocks[pos] = Blocks(pos, size, id)
                pos = npos
                id += 1
                infile = False
            else:
                self.blocks[pos] = Blocks(pos, size, None)
                pos = npos
                infile = True

        for p1, p2 in itertools.pairwise(sorted(self.blocks.keys())):
            self.next[p1] = p2
            self.prev[p2] = p1


    def _next_pd(self, pd):
        npd = pd
        while self.blocks[npd].fileid is not None:
            npd = self.next[npd]
        return npd

    def _next_ps(self, ps):
        nps = ps
        while self.blocks[nps].fileid is None:
            #print(nps)
            nps = self.prev[nps]
        return nps

    def split(self, pos1, size1):
        if size1 < self.blocks[pos1].size:
            size2 = self.blocks[pos1].size - size1
            pos2 = pos1 + size1
            pos3 = pos2 + size2
            self.blocks[pos1].size = size1
            self.blocks[pos2] = Blocks(pos2, size2, self.blocks[pos1].fileid)
            self.next[pos2] = pos3
            self.next[pos1] = pos2
            self.prev[pos3] = pos2
            self.prev[pos2] = pos1

    def debug_state(self):
        self.logger.debug(self.prev)
        self.logger.debug(self.next)
        for pos, blk in sorted(self.blocks.items()):
            self.logger.debug(pos, blk)

    def compact(self):
        self.logger.info("len(self.blocks) =", len(self.blocks))
        pd = self._next_pd(0)
        ps = self._next_ps(max(self.blocks.keys()))
        i = 0
        while pd <= ps:
            i += 1
            self.logger.info(f"pd = {pd}, ps = {ps}")
            self.logger.debug(self.render_blocks())
            if self.blocks[pd].size > self.blocks[ps].size:
                self.split(pd, self.blocks[ps].size)
            elif self.blocks[pd].size < self.blocks[ps].size:
                self.split(ps, self.blocks[ps].size - self.blocks[pd].size)
                ps = self.next[ps]

            self.blocks[pd].fileid = self.blocks[ps].fileid
            self.blocks[ps].fileid = None
            #self.debug_state()
            pd = self._next_pd(pd)
            ps = self._next_ps(ps)
        self.logger.debug(self.render_blocks())

    def compact2(self):
        fileid_idx = dict()
        for pos, blk in self.blocks.items():
            if blk.fileid is not None:
                fileid_idx[blk.fileid] = pos

        fid = max(fileid_idx.keys())
        print(fid)
        self.logger.debug(self.render_blocks())
        while fid >= 0:
            spos = fileid_idx[fid]
            sblk = self.blocks[spos]
            dpos = list(sorted(blk.pos for blk in filter(lambda x: x.size >= sblk.size and x.fileid is None and x.pos < spos, self.blocks.values())))
            if dpos:
                dpos = dpos[0]
                dblk = self.blocks[dpos]
                if dblk.size > sblk.size:
                    self.split(dpos, sblk.size)
                dblk.fileid = sblk.fileid
                sblk.fileid = None
                self.logger.debug(self.render_blocks())
            fid -= 1

    def checksum(self):
        return sum(x.checksum() for x in self.blocks.values())

    def render_blocks(self):
        return "".join(blks.render() for pos, blks in sorted(self.blocks.items()))

    @classmethod
    def from_file(cls, filename, loglevel="WARN"):
        return cls(aoc.read_string(filename), loglevel=loglevel)


if __name__ == '__main__':
    test0 = Disk("999", loglevel="DEBUG")
    test0.debug_state()
    test0.split(18, 5)
    test0.debug_state()

    test1 = Disk.from_file("test1.txt", loglevel="DEBUG")
    print(test1.render_blocks())
    #test1.debug_state()
    test1.compact()
    print(test1.checksum())

    test1.reset_blocks()
    test1.compact2()
    print(test1.checksum())

    #test2 = Disk("12345", loglevel="DEBUG")
    #test2.compact()
    #print(test2.checksum())

    inp = Disk.from_file("input.txt", loglevel="WARN")
    inp.compact2()
    print(inp.checksum())
