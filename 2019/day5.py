import collections
import math
import re
import sys

import sortedcollections

def tryrun(prog):
    pc = 0
    inputs = [5]

    arity = {99: 0, 1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3}
    def parse():
        nonlocal pc
        op = prog[pc]
        pc += 1
        vals = []
        locs = []
        for i in range(arity[op % 100]):
            mode = (op // (10 ** (2 + i))) % 10
            vals.append(prog[pc] if mode == 1 else prog[prog[pc]])
            locs.append(None if mode == 1 else prog[pc])
            pc += 1
        return op % 100, vals, locs

    while prog[pc] != 99:
        op, vals, locs = parse()
        if op == 1:
            prog[locs[2]] = vals[0] + vals[1]
        elif op == 2:
            prog[locs[2]] = vals[0] * vals[1]
        elif op == 3:
            prog[locs[0]] = inputs[0]
            del inputs[0]
        elif op == 4:
            print('out:', vals[0])
        elif op == 5:
            if vals[0] != 0:
                pc = vals[1]
        elif op == 6:
            if vals[0] == 0:
                pc = vals[1]
        elif op == 7:
            prog[locs[2]] = int(vals[0] < vals[1])
        elif op == 8:
            prog[locs[2]] = int(vals[0] == vals[1])
        else:
            assert False

    return prog[0]


with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    lines = [[int(i) for i in l.split(',')] for l in lines]

    tryrun(lines[0])
