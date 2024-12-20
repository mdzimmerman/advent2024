import sys
from collections import deque

sys.path.append("..")
from aoc import Logger, CharArray, Dir, Point


class Maze:
    filename: str
    grid: CharArray
    bfs_path: dict[Point, int]

    def __init__(self, filename: str):
        self.filename = filename
        self.grid = CharArray.from_file(filename)
        self.bfs_path = self._build_bfs_path()

    def _build_bfs_path(self):
        start = list(self.grid.find("S"))[0]

        #end = self.grid.find("E")

        seen = set()
        path = dict()
        queue = deque()
        queue.append((0, start))

        while queue:
            steps, pos = queue.popleft()
            if pos in seen:
                continue

            seen.add(pos)
            path[pos] = steps

            for d in Dir.ALL:
                npos = pos.move(d)
                if self.grid.get(npos) != '#':
                    queue.append((steps+1, npos))
        return path

if __name__ == '__main__':
    test = Maze("test.txt")
    for p, n in test.bfs_path.items():
        print(p, n)