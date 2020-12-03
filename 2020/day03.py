import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

rows = len(lines)
cols = len(lines[0])

def tryy(rs, cs):
    row = 0
    col = 0
    ct = 0
    while row < rows:
        row += rs
        col += cs
        if row >= rows:
            break
        if lines[row][col % cols] == '#':
            ct += 1
    return ct

print(
    tryy(1, 1)
    * tryy(1, 3)
    * tryy(1, 5)
    * tryy(1, 7)
    * tryy(2, 1)
)
