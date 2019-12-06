import collections
import math
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]

    starts = set()
    d = collections.defaultdict(set)
    for line in lines:
        a, b = line.split(')')
        d[a].add(b)
        starts.add(a)

    bw = {}
    for a, bs in d.items():
        for b in bs:
            bw[b] = a

    n = 0
    for b in bw.keys():
        while True:
            par = bw.get(b)
            if par:
                n += 1
                b = par
            else:
                break
    print(n)

    # original part 2 approach that I scrapped (not the most efficient):
    #
    # for i in range(10000):
    # for j in range(10000):
    #     try:
    #         you = 'YOU'
    #         for _ in range(i):
    #             you = bw[you]
    #         san = 'SAN'
    #         for _ in range(i):
    #             san = bw[san]
    #     except KeyError:
    #         pass
    #     if san == you:
    #         print(i, j)
    #         sys.exit()


    def parents(n):
        l = []
        while n:
            l.append(n)
            n = bw.get(n)
        return l

    you = parents('YOU')
    san = parents('SAN')

    for i, (y, s) in enumerate(zip(reversed(you), reversed(san))):
        if y != s:
            print(len(you) - i + len(san) - i - 2)
            break
