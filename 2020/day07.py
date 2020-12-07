import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

containedin = collections.defaultdict(set)
contains = collections.defaultdict(list)
for line in lines:
    color = re.match(r'(.+?) bags contain', line)[1]
    for ct, innercolor in re.findall(r'(\d+) (.+?) bags?[,.]', line):
        ct = int(ct)
        containedin[innercolor].add(color)
        contains[color].append((ct, innercolor))

# part 1:
# holdsgold = set()
# def check(color):
#     for c in containedin[color]:
#         holdsgold.add(c)
#         check(c)
# check('shiny gold')
# print(len(holdsgold))

def cost(color):
    total = 0
    for ct, inner in contains[color]:
        total += ct
        total += ct * cost(inner)
    return total
print(cost('shiny gold'))
