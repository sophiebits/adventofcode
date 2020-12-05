import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

# part 1 in comments:
# mm = 0
allst = set()
for line in lines:
    line = line.replace('F', '0')
    line = line.replace('B', '1')
    line = line.replace('L', '0')
    line = line.replace('R', '1')
    num = int(line, 2)
    # mm = max(num, mm)
    allst.add(num)

# print(mm)
for i in range(256 * 8):
    if i not in allst and i+1 in allst and i-1 in allst:
        print(i)
