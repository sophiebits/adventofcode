import collections
import math
import re
import sys

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]

    valid = 0
    for line in lines:
        match = re.fullmatch(r'(\d+)-(\d+) (.): (.+)', line)
        lo, hi, ch, word = match.groups()
        lo = int(lo)
        hi = int(hi)

        # if lo <= word.count(ch) <= hi:
        #     valid += 1

        if (word[lo - 1] == ch) + (word[hi - 1] == ch) == 1:
            valid += 1
    print(valid)
