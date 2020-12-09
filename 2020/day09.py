import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]
lines = [int(l) for l in lines]

def issumoftwo(n, options):
    options = set(options)
    for o in options:
        if n-o != o and n-o in options:
            return True
    return False

for i in range(25, len(lines)):
    if not issumoftwo(lines[i], lines[i-25:i]):
        goal = lines[i]
        print(goal)
        break

partsum = [0]
acc = 0
for x in lines:
    acc += x
    partsum.append(acc)
for i in range(len(partsum)):
    j = i + 2
    while 0 <= j < len(partsum) and partsum[j] - partsum[i] <= goal:
        if partsum[j] - partsum[i] == goal:
            print(max(lines[i:j]) + min(lines[i:j]))
            break
        j += 1
