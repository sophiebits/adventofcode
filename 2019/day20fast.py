import collections
import heapq
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

    interesting = set(pt for pt in warpa.keys() if type(pt) == tuple)
    bfs = [(0, pt, pt) for pt in interesting]
    seen = {}
    dists = collections.defaultdict(list)
    while bfs:
        dist, start, pt = heapq.heappop(bfs)
        if (start, pt) in seen:
            continue
        if pt in interesting:
            dists[start].append((pt, dist))
        seen[start, pt] = dist
        i,j = pt
        for si,sj in [
            (i,j+1),
            (i,j-1),
            (i+1,j),
            (i-1,j),
        ]:
            if grid[si][sj] == '.':
                heapq.heappush(bfs, (dist + 1, start, (si,sj)))

    bfs = [(0, warpa['AA'], 0, '')]
    seen = {}
    part1done = False
    while bfs:
        dist, pt, depth, debug = heapq.heappop(bfs)
        if (pt, depth) in seen:
            continue
        seen[pt, depth] = dist
        if not part1done and warpa['ZZ'] == pt:
            part1done = True
            print(dist, debug)
        if warpa['ZZ'] == pt and depth == 0:
            print(dist, debug)
            break
        i,j = pt
        if pt in dists:
            for pt2, d in dists[pt]:
                heapq.heappush(bfs, (dist+d, pt2, depth, debug))
        if pt in warpb:
            if 3 <= i < len(grid) - 3 and 3 <= j < len(grid[0]) - 3:
                # inner
                heapq.heappush(bfs, (dist+1, warpb[pt], depth+1, debug + ' +' + warpa[pt]))
            elif depth >= 1:
                # outer
                heapq.heappush(bfs, (dist+1, warpb[pt], depth-1, debug + ' -' + warpa[pt]))



