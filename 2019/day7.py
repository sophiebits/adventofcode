import collections
import math
import re
import sys

import sortedcollections

def tryprog(prog, name):
    pc = 0
    outputs = []

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
        opc = pc
        op, vals, locs = parse()
        #print(name,opc,op, prog[:opc], prog[opc], prog[opc+1:])
        if op == 1:
            prog[locs[2]] = vals[0] + vals[1]
        elif op == 2:
            prog[locs[2]] = vals[0] * vals[1]
        elif op == 3:
            #print(pc, prog, inputs)
            prog[locs[0]] = yield
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
        else:
            assert False

    #print(name,'done')
    return prog[0], outputs[0] if outputs else None

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    prog = [int(c) for c in lines[0].split(',')]

    m = 0
    for a in range(5,10):
        for b in range(5,10):
            for c in range(5,10):
                for d in range(5,10):
                    for e in range(5,10):
                        if len(set([a,b,c,d,e]))!=5:
                            continue
                        #if [a,b,c,d,e]!=[9,8,7,6,5]:
                        #    continue
                        ap = tryprog(prog[:],'a')
                        bp = tryprog(prog[:],'b')
                        cp = tryprog(prog[:],'c')
                        dp = tryprog(prog[:],'d')
                        ep = tryprog(prog[:],'e')

                        next(ap); ap.send(a)
                        next(bp); bp.send(b)
                        next(cp); cp.send(c)
                        next(dp); dp.send(d)
                        next(ep); ep.send(e)

                        eo = -123
                        val = 0
                        for lo in range(10000000000000000):
                            done = False
                            for p in (ap, bp, cp, dp, ep):
                                try:
                                    #print('[')
                                    if lo != 0:
                                        next(p)
                                    val = p.send(val)
                                    #print(']')
                                    if p == ep:
                                        eo = val
                                except StopIteration:
                                    done = True
                                    break
                            if done:
                                break
                        #print(eo, a, b, c, d, e)
                        if eo > m:
                            m = eo
                            print('best', m, a, b, c, d, e)




                        #_, eo = tryprog(prog, [e, do])
                        #maxe = eo
                        #o = eo
                        #while True:
                        #    stop = False
                        #    for p in (a, b, c, d, e):
                        #        _, o = tryprog(prog, [p, o])
                        #        if o is None:
                        #            stop = True
                        #            break
                        #        if p == e and True:#o > maxe:
                        #            maxe = o
                        #    if stop:
                        #        break
                        #if maxe > m:
                        #    m = maxe
                        #    #print(m, a, b, c, d, e)
