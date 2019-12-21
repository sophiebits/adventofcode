import collections
import math
import itertools
import re
import sys

import sortedcollections
import z3

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


def solve(outputs):
    s = z3.Solver()
    insts = [z3.Int(f'inst{i}') for i in range(15)]
    opas = [z3.Int(f'opa{i}') for i in range(15)]
    opbs = [z3.Int(f'opb{i}') for i in range(15)]
    steps = z3.Int('steps')
    A,B,C,D = z3.Bools('a b c d')
    for inst in insts:
        s.add(0 <= inst, inst <= 2)
    for opa in opas:
        s.add(0 <= opa, opa < 6)
    for opb in opas:
        s.add(4 <= opb, opb < 6)
    s.add(1 <= steps, steps <= 15)
    T = False  # 4
    J = False  # 5
    for i in range(15):
        firstarg = z3.If(opas[i] == 0, A,
            z3.If(opas[i] == 1, B,
            z3.If(opas[i] == 2, C,
            z3.If(opas[i] == 3, D,
            z3.If(opas[i] == 4, T, J)))))
        sndarg = z3.If(opbs[i] == 0, A,
            z3.If(opbs[i] == 1, B,
            z3.If(opbs[i] == 2, C,
            z3.If(opbs[i] == 3, D,
            z3.If(opbs[i] == 4, T, J)))))
        newout = z3.If(
            insts[i] == 0, z3.And(firstarg, sndarg),
            z3.If(insts[i] == 1, z3.Or(firstarg, sndarg),
            z3.Not(firstarg)))
        newT = z3.If(opbs[i] == 4, newout, T)
        newJ = z3.If(opbs[i] == 5, newout, J)
        T = z3.If(i + 1 <= steps, newT, T)
        J = z3.If(i + 1 <= steps, newJ, J)
    for j, (a,b,c,d) in enumerate(itertools.product((False,True), repeat=4)):
        res = bool(outputs[j])
        s.add(z3.Implies(A == a and B == b and C == c and D == d, res))
    if s.check() == z3.sat:
        mod = s.model()
        prog = ''
        print(outputs, mod)
        for i in range(mod[steps].as_long()):
            def k(f,z):
                return f.as_long() if f else z
            inst = k(mod[insts[i]],0)
            opa = k(mod[opas[i]],0)
            opb = k(mod[opbs[i]],4)
            prog += f'{["AND","OR","NOT"][inst]} {"ABCDTJ"[opa]} {"ABCDTJ"[opb]}\n'
        return prog


with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    #lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]
    prog = [[int(i) for i in l.split(',')] for l in lines][0]

    #for out in itertools.product((0,1), repeat=16):
    #    script = solve(out)
    #    if script:
    #        print(out, script.replace('\n',' '))

    p = tryprog(prog)
    while True:
        o = next(p)
        if type(o) == tuple:
            break
    #for c in 'NOT T T\nAND A T\nAND B T\nAND C T\nNOT T J\nAND D J\nWALK\n':
    # (not A or not B or not C) and D and (H or E and I)
    for c in ''.join([l.strip() + '\n' for l in '''
        NOT J J
        AND E J
        AND I J
        OR H J
        NOT T T
        AND A T
        AND B T
        AND C T
        NOT T T
        AND T J
        AND D J
        NOT A T
        OR T J
        RUN
    '''.strip().splitlines()]):
        o = p.send(ord(c))
        if type(o) == int:
            print(f'{chr(o)}',end='')
    while True:
        try:
            o = p.send(None)
        except StopIteration:
            break
        if type(o) == int and o < 128:
            print(f'{chr(o)}',end='')
        else:
            print(f'\n{o}')

