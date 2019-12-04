import itertools
import re

uq = set()
for x in range(231832,767346+1):
    two = False
    for g, l in itertools.groupby(list(str(x)), lambda x: x):
        q = len(list(l))
        if q == 2:
            two = True
    # part 1: if re.match(r'.*(\d)\1', str(x)) and
    if two and sorted(str(x)) == list(str(x)):
        uq.add(x)

print(sorted(uq))
print(len(uq))

