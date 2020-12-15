import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]
lines = [int(l) for l in lines[0].split(',')]

spoken = collections.defaultdict(list)
last = None
spkc = 1
for line in lines:
    spoken[line].append(spkc)
    last = line
    spkc += 1
while spkc <= 30000000:
    if len(spoken[last]) > 1:
        last = spoken[last][-1] - spoken[last][-2]
    else:
        last = 0
    spoken[last].append(spkc)
    if spkc % 1000000 == 0:
        print(spkc,last)
    spkc += 1
print(last)
