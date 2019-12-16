import copy
import collections
import math
import re
import sys

import sortedcollections

def tryprog(prog, pc=0, name=''):
    outputs = []

    if isinstance(prog, collections.defaultdict):
        prog = collections.defaultdict(int, prog)
    else:
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
            prog[locs[0]] = yield ('needinput', prog, opc)
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

    op = tryprog(lines[0])
    _, prog, pc = next(op)
    seen = {
        (0, 0): (1, prog, pc, 0),
    }
    dirs = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
    bfs = collections.deque([(0, 0)])
    otank = None
    while bfs:
        x, y = bfs.popleft()
        _, prog, pc, omd = seen[x, y]
        for dic, dixy in dirs.items():
            nxy = (x + dixy[0], y + dixy[1])
            if nxy in seen:
                continue
            p = tryprog(prog, pc=pc)
            assert next(p)[0] == 'needinput'
            ans = p.send(dic)
            a, prog2, pc2 = next(p)
            assert a == 'needinput'
            seen[nxy] = (ans, prog2, pc2, omd + 1)
            if ans == 2:
                otank = nxy
                print(otank, omd+1)
            if ans != 0:
                bfs.append(nxy)

    clean = {otank: 0}
    bfs = collections.deque([otank])
    while bfs:
        x, y = bfs.popleft()
        for dic, dixy in dirs.items():
            nxy = (x + dixy[0], y + dixy[1])
            if nxy in clean:
                continue
            if seen[nxy][0] == 1:
                clean[nxy] = clean[x, y] + 1
                bfs.append(nxy)

    print(max(clean.values()))
