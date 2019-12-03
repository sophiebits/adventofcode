import collections
import math
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    lines = [l.split(',') for l in lines]

    grid = collections.defaultdict(lambda: '.')
    grid[(0, 0)] = 'o'
    ga = {}
    x, y = 0, 0
    steps = 0
    for ins in lines[0]:
        d, l = ins[0], int(ins[1:])
        for i in range(l):
            if d == 'R':
                x += 1
            elif d == 'L':
                x -= 1
            elif d == 'U':
                y += 1
            elif d == 'D':
                y -= 1
            else:
                assert False
            grid[(x, y)] = '-'
            if (x, y) not in ga:
                ga[(x, y)] = steps
            steps += 1

    coll = {}

    x, y = 0, 0
    steps = 0
    for ins in lines[1]:
        d, l = ins[0], int(ins[1:])
        for i in range(l):
            if d == 'R':
                x += 1
            elif d == 'L':
                x -= 1
            elif d == 'U':
                y += 1
            elif d == 'D':
                y -= 1
            else:
                assert False
            if grid[(x, y)] == '-':
                coll[(x, y)] = steps + ga[(x, y)]
                grid[(x, y)] = '+'
            else:
                grid[(x, y)] = '|'
            steps += 1



    print(coll)
    #print(sorted(coll, key=lambda xy: abs(xy[0]) + abs(xy[1])))
    #print(min(abs(x) + abs(y) for x, y in coll))
    m = min(coll.values())
    print(m)
    #print([k, v for k, v in coll.items() if v == m])