import collections
import math
import re
import sys

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]

    nums = set(l[0] for l in lines)
    for num in nums:
        for num2 in nums:
            x = 2020 - num - num2
            if x in nums and len({x,num,num2})==3:
                print(num * num2 * (2020 - num - num2))