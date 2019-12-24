import collections
import math
import re
import sys

import sortedcollections

def step(grid):
    grid2 = []
    def get(x, y):
        a = []
        if x > 0:
            a.append(grid[x-1][y])
        if x < len(grid)-1:
            a.append(grid[x+1][y])
        if y > 0:
            a.append(grid[x][y-1])
        if y < len(grid[0])-1:
            a.append(grid[x][y+1])
        return a
    for i in range(len(grid)):
        line2 = ''
        for j in range(len(grid[0])):
            if grid[i][j] == '#':
                ch = '#' if get(i,j).count('#') == 1 else '.'
            else:
                ch = '#' if get(i,j).count('#') in (1,2) else '.'
            line2 += ch
        grid2.append(line2)
    return grid2


def stepb(bugs):
    minlev = min(l for l, x, y in bugs)
    maxlev = max(l for l, x, y in bugs)

    def countadj(l, x, y):
        c = 0
        adj = [
            (l, x-1,y),
            (l, x+1,y),
            (l, x,y-1),
            (l, x,y+1),
        ]
        actadj = []
        for aa in adj:
            la, xa, ya = aa
            if xa == -1:
                actadj.append((la-1, 1, 2))
            elif xa == 2 and ya == 2 and x == 1:
                actadj.append((la+1, 0, 0))
                actadj.append((la+1, 0, 1))
                actadj.append((la+1, 0, 2))
                actadj.append((la+1, 0, 3))
                actadj.append((la+1, 0, 4))
            elif xa == 2 and ya == 2 and x == 3:
                actadj.append((la+1, 4, 0))
                actadj.append((la+1, 4, 1))
                actadj.append((la+1, 4, 2))
                actadj.append((la+1, 4, 3))
                actadj.append((la+1, 4, 4))
            elif xa == 5:
                actadj.append((la-1, 3, 2))
            elif ya == -1:
                actadj.append((la-1, 2, 1))
            elif ya == 2 and xa == 2 and y == 1:
                actadj.append((la+1, 0, 0))
                actadj.append((la+1, 1, 0))
                actadj.append((la+1, 2, 0))
                actadj.append((la+1, 3, 0))
                actadj.append((la+1, 4, 0))
            elif ya == 2 and xa == 2 and y == 3:
                actadj.append((la+1, 0, 4))
                actadj.append((la+1, 1, 4))
                actadj.append((la+1, 2, 4))
                actadj.append((la+1, 3, 4))
                actadj.append((la+1, 4, 4))
            elif ya == 5:
                actadj.append((la-1, 2, 3))
            else:
                actadj.append(aa)
        #print('actadj', l, x, y, sorted(actadj))
        return sum(1 for aa in actadj if aa in bugs)

    nbugs = set()
    for lev in range(minlev - 1, maxlev + 2):
        for i in range(5):
            for j in range(5):
                if i==2 and j==2:
                    continue
                if (lev,i,j) in bugs and countadj(lev,i,j) == 1:
                    nbugs.add((lev,i,j))
                if (lev,i,j) not in bugs and countadj(lev,i,j) in (1,2):
                    nbugs.add((lev,i,j))
    return nbugs


with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]

    grid = lines
    seengrid = set()
    while True:
        fgrid = ''.join(grid)
        if fgrid in seengrid:
            break
        seengrid.add(fgrid)
        grid = step(grid)
    print(sum(2 ** i for i, ch in enumerate(fgrid) if ch == '#'))

    bugs = set()
    for i in range(5):
        for j in range(5):
            if lines[i][j] == '#':
                bugs.add((0,i,j))
    for i in range(200):
        bugs = stepb(bugs)
    print(len(bugs))

