import collections
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]
    print(lines)

    fuel = 0
    for line in lines:
        f = line[0]
        while True:
            f = f // 3 - 2
            if f > 0:
                fuel += f
            else:
                break
    print(fuel)