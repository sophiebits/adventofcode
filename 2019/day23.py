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
        #print(name,pc)
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
    #lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]
    prog = [[int(i) for i in l.split(',')] for l in lines][0]

    qs = [[] for _ in range(50)]
    ps = [tryprog(prog, name=i) for i in range(50)]
    for p in ps:
        assert type(p.send(None)) == tuple
    ns = [i for i in range(50)]

    done = False
    part1 = True
    nat = None
    lastY = None
    while not done:
        if not any(qs) and all(a == -1 for a in ns) and nat:
            qs[0].append(nat)
            if lastY == nat[1]:
                print(nat[1])
                break
            lastY = nat[1]
            nat = None
        for i in range(50):
            t = ps[i].send(ns[i])
            if type(t) == tuple:
                # input
                if qs[i]:
                    x, y = qs[i][0]
                    del qs[i][0]
                    ps[i].send(x)
                    ns[i] = y
                else:
                    ns[i] = -1
            else:
                add = t
                x = ps[i].send(None)
                y = ps[i].send(None)
                if add == 255:
                    if part1:
                        print(y)
                        part1 = False
                    nat = x, y
                    continue
                assert 0 <= add <= 49
                qs[add].append((x,y))
