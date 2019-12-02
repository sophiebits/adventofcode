import collections
import math
import re
import sys

import sortedcollections

def tryrun(prog, n, v):
    pc = 0
    prog[1] = n
    prog[2] = v

    while prog[pc] != 99:
        if prog[pc] == 1:
            a = prog[pc + 1]
            b = prog[pc + 2]
            c = prog[pc + 3]
            prog[c] = prog[a] + prog[b]
            pc += 4
        elif prog[pc] == 2:
            a = prog[pc + 1]
            b = prog[pc + 2]
            c = prog[pc + 3]
            prog[c] = prog[a] * prog[b]
            pc += 4
    return prog[0]


with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]

    pc = 0
    prog = lines[0]

    for n in range(12, 20000):
        x = tryrun(prog[:], n, 49)
        print(n, x)
        if x >= 19690720:
            break