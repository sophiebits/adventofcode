import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

def step(grid):
    newgrid = []
    for row in range(len(grid)):
        newrow = ''
        for col in range(len(grid[0])):
            adj = []
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    if x == y == 0:
                        continue
                    # part 1 in comments:
                    # if 0 <= row+x < len(grid) and 0 <= col+y < len(grid[0]):
                    #     adj.append(grid[row+x][col+y])
                    i = 1
                    while 0 <= row+i*x < len(grid) and 0 <= col+i*y < len(grid[0]):
                        ch = grid[row+i*x][col+i*y]
                        if ch != '.':
                            adj.append(ch)
                            break
                        i += 1
            if grid[row][col] == 'L' and '#' not in adj:
                newrow += '#'
            # elif grid[row][col] == '#' and adj.count('#') >= 4:
            elif grid[row][col] == '#' and adj.count('#') >= 5:
                newrow += 'L'
            else:
                newrow += grid[row][col]
        newgrid.append(newrow)
    return newgrid

grid = lines
while True:
    after = step(grid)
    if after == grid:
        print(''.join(grid).count('#'))
        break
    grid = after
