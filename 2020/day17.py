import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

def step(grid):
    ng = {}
    for x in range(min(k[0] for k in grid.keys())-1, max(k[0] for k in grid.keys())+2):
        for y in range(min(k[1] for k in grid.keys())-1, max(k[1] for k in grid.keys())+2):
            for z in range(min(k[2] for k in grid.keys())-1, max(k[2] for k in grid.keys())+2):
                for q in range(min(k[3] for k in grid.keys())-1, max(k[3] for k in grid.keys())+2):
                    s = grid.get((x,y,z,q), False)
                    an = 0
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            for dz in (-1, 0, 1):
                                for dq in (-1, 0, 1):
                                    if dx == dy == dz == dq == 0:
                                        continue
                                    if grid.get((x+dx,y+dy,z+dz,q+dq),False):
                                        an += 1
                    if (s and an in (2, 3)) or (not s and an == 3):
                        ng[(x,y,z,q)] = True
    return ng

grid = {}
for row, line in enumerate(lines):
    for col, ch in enumerate(line):
        grid[(row, col, 0, 0)] = ch == '#'


for i in range(6):
    print(i, sum(grid.values()))
    grid = step(grid)
print(sum(grid.values()))
