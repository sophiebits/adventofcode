import collections
import math
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]

    grid = lines

    warpa = {}
    warpb = {}
    for i in range(2, len(grid) - 2):
        for j in range(2, len(grid[0]) - 2):
            if grid[i][j] != '.':
                continue
            for pair in [
                grid[i][j-2:j],
                grid[i][j+1:j+3],
                grid[i-2][j]+grid[i-1][j],
                grid[i+1][j]+grid[i+2][j],
            ]:
                if pair.isalpha():
                    if pair in warpa:
                        warpb[i,j] = warpa[pair]
                        warpa[i,j] = pair
                        warpb[warpa[pair]] = i,j
                    else:
                        warpa[pair] = i,j
                        warpa[i,j] = pair
                    continue

    bfs = collections.deque([(warpa['AA'], 0, 0, '')])
    seen = {}
    while bfs:
        pt, dist, depth, debug = bfs.popleft()
        if (pt, depth) in seen:
            continue
        seen[pt, depth] = dist
        if warpa['ZZ'] == pt and depth == 0:
            print(dist, debug)
            break
        i,j = pt
        for si,sj in [
            (i,j+1),
            (i,j-1),
            (i+1,j),
            (i-1,j),
        ]:
            if grid[si][sj] == '.':
                bfs.append(((si, sj), dist+1, depth, debug))
        if pt in warpb:
            # if 6 <= i <= 30 and 6 <= j <= 40:
            if 25 <= i <= 105 and 20 <= j <= 110:
                # inner
                bfs.append((warpb[pt], dist+1, depth+1, debug + ' +' + warpa[pt]))
            elif depth >= 1:
                # outer
                bfs.append((warpb[pt], dist+1, depth-1, debug + ' -' + warpa[pt]))



