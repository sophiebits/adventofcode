import collections
import itertools
import cmath
import math
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]

    # part 1
    maxcnt = 0
    best = None
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == '.':
                continue
            cnt = 0
            s = set()
            for x in range(len(lines)):
                for y in range(len(lines[0])):
                    if lines[x][y] == '.':
                        continue
                    gc = int(abs(math.gcd(x - i, y - j)))
                    no = False
                    #print(x,y, gc)
                    for q in range(1, gc):
                        if lines[i + (x - i) // gc * q][j + (y - j) // gc * q] == '#':
                            no = True
                            break
                    if not no:
                        s.add((x, y))
                        cnt += 1
            #print(i, j, cnt, sorted(s))
            maxcnt = max(cnt, maxcnt)
            if cnt == maxcnt:
                best = i, j
    print(maxcnt, best)

    # part 2
    allast = set()
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == '#':
                allast.add((i, j))
    phase = lambda xy: cmath.phase((xy[0] - best[0]) + (xy[1] - best[1]) * 1j)
    so = sorted(allast, key=phase,reverse=True)
    for i, (direc, asts) in enumerate(itertools.groupby(so, key=phase)):
        if i + 1 == 200:
            print(i + 1, direc, list(asts))

    # part 2 appendix: I didn't write this during the timed contest but if I
    # had to loop around to get the answer (i.e. if there were fewer than 200
    # different directions) it might've looked something like this:
    grouped = []
    for direc, asts in itertools.groupby(so, key=phase):
        grouped.append(list(asts))
    i = 0
    def pop():
        global i
        oi = i
        while not grouped[i]:
            i = (i + 1) % len(grouped)
            if i == oi:
                return None
        closest = min(grouped[i], key=lambda xy: math.hypot(xy[0] - best[0], xy[1] - best[1]))
        grouped[i][:] = [p for p in grouped[i] if p != closest]
        i = (i + 1) % len(grouped)
        return closest
    for _ in range(200 - 1):
        pop()
    print(pop())
