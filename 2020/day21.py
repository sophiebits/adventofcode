import collections
import math
import re
import sys

import z3

lines = [l.rstrip('\n') for l in sys.stdin]

allwhere = collections.defaultdict(set)
ingwhere = collections.defaultdict(set)

for i, line in enumerate(lines):
    ingredients, allergens = line.split('contains', 1)
    ingredients = re.findall(r'\w+', ingredients)
    allergens = re.findall(r'\w+', allergens)

    for ingredient in ingredients:
        ingwhere[ingredient].add(i)
    for allergen in allergens:
        allwhere[allergen].add(i)

inert = set()
ct = 0
for ing, vals2 in ingwhere.items():
    canallerg = False
    for allergen, vals in allwhere.items():
        if vals < vals2:
            canallerg = True
    if not canallerg:
        inert.add(ing)
        ct += len(ingwhere[ing])
print(ct)

possing = list(set(ingwhere.keys()) - inert)
possall = list(set(allwhere.keys()))
assert len(possing) == len(possall)

assignments = z3.IntVector('allergen', len(possall))
solver = z3.Solver()
for a in assignments:
    solver.add(0 <= a)
    solver.add(a < len(possall))
solver.add(z3.Distinct(assignments))
for ai, allergen in enumerate(possall):
    conds = []
    for ii, ing in enumerate(possing):
        if ingwhere[ing] >= allwhere[allergen]:
            conds.append(assignments[ii] == ai)
    solver.add(z3.Or(conds))
assert solver.check() == z3.sat
m = solver.model()
matches = []
for ii, a in enumerate(assignments):
    matches.append((possall[m.evaluate(assignments[ii]).as_long()], possing[ii]))

matches.sort()
print(','.join(m[1] for m in matches))

