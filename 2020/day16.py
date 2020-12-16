import collections
import math
import re
import sys

ranges, your, neighbor = [l.rstrip('\n') for l in sys.stdin.read().split('\n\n')]

rp = []
rpd = collections.defaultdict(list)
for line in ranges.splitlines():
    kind = line.split(': ')[0]
    for a, b in re.findall(r'(\d+)-(\d+)', line):
        rp.append((int(a),int(b),kind))
        rpd[kind].append((int(a), int(b)))

fail = 0
valtix = []
for line in neighbor.splitlines()[1:]:
    nums = [int(l) for l in line.split(',')]
    anyfail = False
    for num in nums:
        if any(a <= num <= b for a, b, _ in rp):
            pass
        else:
            fail += num
            anyfail = True
    if not anyfail:
        valtix.append(nums)
print(fail)

yourp = [int(l) for l in your.splitlines()[1].split(',')]
valtix.append(yourp)

overunder = collections.defaultdict(list)
numf = len(valtix[0])
for f in range(len(valtix[0])):
    overunder[f] = [t[f] for t in valtix]

memo = {}
def canmatch(fname, im):
    k = (fname, im)
    if k in memo:
        return memo[k]
    cm = all(any(a <= v <= b for a, b in rpd[fname]) for v in overunder[im])
    memo[k] = cm
    return cm

assign = {}
assignb = {}
while len(rpd) > len(assign):
    progress = False
    for im in range(numf):
        if im in assignb.keys():
            continue
        t = []
        for fname in rpd.keys():
            if fname in assign.keys():
                continue
            if canmatch(fname, im):
                t.append(fname)
        if len(t) == 1:
            assign[t[0]] = im
            assignb[im] = t[0]
            # print(im, 'is', t)


prod = 1
for fname, im in assign.items():
    if fname.startswith('departure'):
        print(fname, yourp[im])
        prod *= yourp[im]
print(prod)


