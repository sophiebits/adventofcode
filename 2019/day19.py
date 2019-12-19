import collections
import math
import re
import sys

import sortedcollections

demo = '''
#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########
'''.split()

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
    prog = [[int(i) for i in l.split(',')] for l in lines][0]

    demomode = 0
    def ck(i, j):
        if demomode:
            return int(demo[i][j] != '.')
        p = tryprog(prog)
        next(p)
        p.send(i)
        o = p.send(j)
        return o

    s = 0
    for i in range(50):
    #for i in range(1820, 1930):
        print('%02d' % i, end=' ')
        for j in range(50):
        #for j in range(1980, 2090):
            p = tryprog(prog)
            next(p)
            p.send(i)
            o = p.send(j)
            s += o
            print('#' if o else '.', end='')
        print()
    print(s)

    tryto = 10000
    sqsi = 100 - 1
    if demomode:
        tryto = 35
        sqsi = 10 - 1
    distfromleftedge = {}
    j = 0
    for i in range(10, tryto):
        while ck(i, j) == 0:
            j += 1
        distfromleftedge[i] = j
        if i % 100 == 0:
            print(i, j)

    i = 0
    for j in range(10, tryto):
        while ck(i, j) == 0:
            i += 1
        if j % 100 == 0:
            print(i, j, '--', distfromleftedge.get(i + sqsi, 1e99) , j - sqsi)
        if distfromleftedge.get(i + sqsi, 1e99) <= j - sqsi:
            print(i, 'yes', distfromleftedge.get(i+sqsi))
            print('tr corner', i, j)
            print('bl corner', i + sqsi, distfromleftedge[i+sqsi])
            print(10000 * distfromleftedge.get(i+sqsi) + i)
            break
        #pts[j,i] = True

