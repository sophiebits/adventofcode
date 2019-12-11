import collections
import math
import re
import sys

import sortedcollections

def tryprog(prog, name=''):
    pc = 0
    outputs = []

    progd = collections.defaultdict(int)
    for i, v in enumerate(prog):
        progd[i] = v
    prog = progd

    relbase = 0

    arity = {99: 0, 1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1}
    def parse():
        nonlocal pc
        op = prog[pc]
        pc += 1
        vals = []
        locs = []
        for i in range(arity[op % 100]):
            mode = (op // (10 ** (2 + i))) % 10
            vals.append(prog[pc] if mode == 1 else prog[prog[pc] + relbase] if mode == 2 else prog[prog[pc]])
            locs.append(None if mode == 1 else prog[pc] + relbase if mode == 2 else prog[pc])
            pc += 1
        return op % 100, vals, locs

    while prog[pc] != 99:
        opc = pc
        op, vals, locs = parse()
        #print(name,opc,op)
        if op == 1:
            prog[locs[2]] = vals[0] + vals[1]
        elif op == 2:
            prog[locs[2]] = vals[0] * vals[1]
        elif op == 3:
            #print(pc, prog, inputs)
            prog[locs[0]] = yield 'needinput'
            #print(name, 'got', prog[locs[0]])
            assert prog[locs[0]] is not None
        elif op == 4:
            #print('out:', vals[0])
            #outputs.append(vals[0])
            #print(name, 'returning', prog[locs[0]])
            yield vals[0]
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
        elif op == 9:
            relbase += vals[0]
        else:
            assert False

    #print(name,'done')
    return prog[0], outputs[0] if outputs else None

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    lines = [[int(i) for i in l.split(',')] for l in lines]

    p = tryprog(lines[0][:])
    px, py = 0, 0
    dx, dy = 0, 1
    white_panels = set()
    white_panels.add((0, 0))  # part 2 only
    painted = set()
    nin = None
    while True:
        try:
            o = p.send(nin)
        except StopIteration:
            break
        if o == 'needinput':
            nin = 1 if (px, py) in white_panels else 0
            continue

        if o == 0:
            if (px, py) in white_panels:
                white_panels.remove((px, py))
                painted.add((px, py))
        elif o == 1:
            white_panels.add((px, py))
            painted.add((px, py))
        else:
            assert False

        o2 = next(p)
        if o2 == 0:
            dx, dy = -dy, dx
        elif o2 == 1:
            dx, dy = dy, -dx
        else:
            assert False
        px += dx
        py += dy

    #print(len(painted))

    graphic = [[' '] * 40 for i in range(10)]

    for x, y in white_panels:
        graphic[2 - y][x] = '#'

    for ll in graphic:
        print(''.join(c*2 for c in ll))




