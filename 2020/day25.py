import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]
a, b = [int(i) for i in lines]

def root(a):
    for i in range(100000000):
        if pow(7, i, 20201227) == a:
            return i

print(pow(a, root(b), 20201227))
print(pow(b, root(a), 20201227))
