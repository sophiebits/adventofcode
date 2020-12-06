import collections
import string
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin.read().split('\n\n')]

ct = 0
for line in lines:
    # part 1:
    # ct += len(set(c for c in line if 'a' <= c <= 'z'))
    alls = set(string.ascii_lowercase)
    for ll in line.split('\n'):
        alls &= set(c for c in ll if 'a' <= c <= 'z')
    ct += len(alls)
print(ct)
