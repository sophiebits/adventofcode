import collections
import math
import re
import sys

import sortedcollections

def step(moons):
    outmoons = [m[:] for m in moons]
    for i, moon in enumerate(moons):
        for j, moon2 in enumerate(moons):
            if i >= j:
                continue
            for q in (0, 1, 2):
                if moon[q] < moon2[q]:
                    outmoons[i][q+3] += 1
                    outmoons[j][q+3] -= 1
                elif moon[q] > moon2[q]:
                    outmoons[i][q+3] -= 1
                    outmoons[j][q+3] += 1
    for moon in outmoons:
        moon[0] += moon[3]
        moon[1] += moon[4]
        moon[2] += moon[5]
    return outmoons


with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]

    # part 1
    moons = [line + [0,0,0] for line in lines]
    for i in range(1000):
        moons = step(moons)
    kes = [(abs(a)+abs(b)+abs(c)) * (abs(x) + abs(y) + abs(z)) for a,b,c,x,y,z in moons]
    print(sum(kes))

    # part 2
    moons = [line + [0,0,0] for line in lines]
    seenx = set()
    repx = None
    seeny = set()
    repy = None
    seenz = set()
    repz = None
    for i in range(1000000):
        if repx and repy and repz:
            break
        moons = step(moons)
        if not repx:
            xk = str([[m[0], m[3]] for m in moons])
            if xk in seenx:
                repx = i
            seenx.add(xk)
        if not repy:
            yk = str([[m[1], m[4]] for m in moons])
            if yk in seeny:
                repy = i
            seeny.add(yk)
        if not repz:
            zk = str([[m[2], m[5]] for m in moons])
            if zk in seenz:
                repz = i
            seenz.add(zk)
    print(repx, repy, repz)

    # part 2 appendix: didn't write this during the contest (I just copied my
    # three into Wolfram Alpha after typing "lcm of") but it would've been:
    def lcm(x, y):
        return x // math.gcd(x, y) * y
    print(lcm(lcm(repx, repy), repz))
