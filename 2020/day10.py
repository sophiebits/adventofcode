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

# alternate part 2 solution, written after the contest:
# def countways2(nums):
#     top = max(nums) + 3
#     nums = set(nums)
#     nums.add(top)
#     a, b, c = 0, 0, 1
#     for i in range(1, top + 1):
#         if i in nums:
#             a, b, c = b, c, a + b + c
#         else:
#             a, b, c = b, c, 0
#     return c
#
# print(countways2(lines))
