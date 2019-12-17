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
    if lines[0][0] != '#':
        # real program
        lines = [[int(i) for i in l.split(',')] for l in lines]
        prog = lines[0]
        grid = ''.join(chr(c) for c in tryprog(lines[0])).strip().split('\n')
        x, y = 0, 2
    else:
        # demo grid
        grid = lines
        x, y = 6, 0
    print('\n'.join(grid))

    # part 1
    s = 0
    for ax in range(1, len(grid) - 1):
        for ay in range(1, len(grid[0]) - 1):
            if (
                grid[ax][ay] == '#' and
                grid[ax-1][ay] == '#' and
                grid[ax+1][ay] == '#' and
                grid[ax][ay-1] == '#' and
                grid[ax][ay+1] == '#'
            ):
                s += ax * ay
    print(s)

    # part 2
    turnR = {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1),
    }
    turnL = {
        (0, 1): (-1, 0),
        (-1, 0): (0, -1),
        (0, -1): (1, 0),
        (1, 0): (0, 1),
    }
    direc = 0, +1
    path = ['R', 0]
    while True:
        nx, ny = x + direc[0], y + direc[1]
        if 0 <= nx <= len(grid) - 1 and 0 <= ny <= len(grid[0]) - 1 and grid[nx][ny] == '#':
            x, y = nx, ny
            path[-1] += 1
        else:
            tryR = turnR[direc]
            nx, ny = x + tryR[0], y + tryR[1]
            if 0 <= nx <= len(grid) - 1 and 0 <= ny <= len(grid[0]) - 1 and grid[nx][ny] == '#':
                x, y = nx, ny
                direc = tryR
                path.append('R')
                path.append(1)
            else:
                tryL = turnL[direc]
                nx, ny = x + tryL[0], y + tryL[1]
                if 0 <= nx <= len(grid) - 1 and 0 <= ny <= len(grid[0]) - 1 and grid[nx][ny] == '#':
                    x, y = nx, ny
                    direc = tryL
                    path.append('L')
                    path.append(1)
                else:
                    break

    # compress this by hand, then continue:
    print(','.join(str(s) for s in path))
    prog[0] = 2
    p = tryprog(prog)
    cs = 'A,B,B,A,C,A,C,A,C,B\nR,6,R,6,R,8,L,10,L,4\nR,6,L,10,R,8\nL,4,L,12,R,6,L,10\nn\n'
    while True:
        try:
            r = next(p)
        except StopIteration:
            break
        while isinstance(r, tuple) and r[0] == 'needinput':
            r = p.send(ord(cs[0]))
            cs = cs[1:]
    print(r)

