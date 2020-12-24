import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

#    nw ne
# w  .  e
# sw se

flips = collections.defaultdict(int)
for line in lines:
    dirs = re.findall('e|se|sw|w|nw|ne', line)
    x, y = 0, 0
    for d in dirs:
        ch = {
            'e': (1, 0),
            'se': (0, -1),
            'sw': (-1, -1),
            'w': (-1, 0),
            'nw': (0, 1),
            'ne': (1, 1),
        }[d]
        x += ch[0]
        y += ch[1]
    flips[(x,y)] += 1

print(sum(1 for k, v in flips.items() if v % 2 == 1))

def step(flips):
    adjblack = collections.defaultdict(int)
    for k, v in flips.items():
        if v % 2 == 0:
            continue
        for adj in [
            (1, 0),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (0, 1),
            (1, 1),
        ]:
            pt = (k[0] + adj[0], k[1] + adj[1])
            adjblack[pt] += 1

    newflips = {}
    for k, v in flips.items():
        if v % 2 == 1:
            if adjblack.get(k, 0) not in (1, 2):
                # flip to white
                pass
            else:
                newflips[k] = 1
    for k, v in adjblack.items():
        if v == 2 and flips.get(k, 0) % 2 == 0:
            newflips[k] = 1
    return newflips

for i in range(100):
    flips = step(flips)
    print(i+1, sum(1 for k, v in flips.items() if v % 2 == 1))