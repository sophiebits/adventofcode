import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

def crt(pairs):
    M = 1
    for x, mx in pairs:
        M *= mx
    total = 0
    for x, mx in pairs:
        b = M // mx
        total += x * b * pow(b, mx-2, mx)
        total %= M
    return total


start = int(lines[0])
pairs = []
for i, n in enumerate(lines[1].split(',')):
    if n == 'x':
        continue
    n = int(n)
    pairs.append((n - i, n))
print(crt(pairs))
