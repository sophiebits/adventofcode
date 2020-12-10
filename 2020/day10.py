import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]
lines = [int(l) for l in lines]

# part 1:
# lines.append(0)
# lines.append(max(lines)+3)
# lines.sort()
# ones = 0
# threes = 0
# for a, b in zip(lines, lines[1:]):
#     if b-a == 1:
#         ones +=1
#     elif b-a == 3:
#         threes += 1
# print(ones * threes)

memo = {}
def countways(adapters, start, goal):
    k = (len(adapters), start)
    if k in memo:
        return memo[k]
    ways = 0
    if goal - start <= 3:
        ways += 1
    if not adapters:
        return ways
    if adapters[0] - start <= 3:
        ways += countways(adapters[1:], adapters[0], goal)
    ways += countways(adapters[1:], start, goal)
    memo[k] = ways
    return ways

print(countways(sorted(lines), 0, max(lines) + 3))