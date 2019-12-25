import collections
import itertools
import math
import re
import sys

import sortedcollections

class Intcode:
    def __init__(self, prog, pc=0, name=''):
        self.prog = prog[:]
        self.pc = pc
        self.name = name
        self.relbase = 0
        # stopped in out
        self.state = None
        self.outputq = None
        self.inputq = None
        self._run()
    def _pset(self, i, v):
        if i >= len(self.prog):
            self.prog.extend(0 for _ in range(1 + i - len(self.prog)))
        self.prog[i] = v
    def _pget(self, i):
        if i >= len(self.prog):
            self.prog.extend(0 for _ in range(1 + i - len(self.prog)))
        return self.prog[i]
    def outputs(self):
        while self.state == 'out':
            yield self.nextout()
    def nextout(self):
        assert self.state == 'out', self.state
        assert self.outputq is not None
        o = self.outputq
        self.outputq = None
        self.state = None
        self._run()
        return o
    def send(self, *inp):
        for v in inp:
            assert self.state == 'in', self.state
            self._pset(self.inputq, v)
            self.inputq = None
            self.state = None
            self._run()
        return self
    def _run(self):
        if self.state:
            raise ValueError(self.state)
        arity = {99: 0, 1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1}
        def parse():
            op = self._pget(self.pc)
            self.pc += 1
            vals = []
            locs = []
            for i in range(arity[op % 100]):
                mode = (op // (10 ** (2 + i))) % 10
                vals.append(
                    self._pget(self.pc) if mode == 1 else
                    self._pget(self._pget(self.pc) + self.relbase) if mode == 2 else
                    self._pget(self._pget(self.pc))
                )
                locs.append(
                    None if mode == 1 else
                    self._pget(self.pc) + self.relbase if mode == 2 else
                    self._pget(self.pc)
                )
                self.pc += 1
            return op % 100, vals, locs
        while True:
            if self._pget(self.pc) == 99:
                self.state = 'stopped'
                return
            opc = self.pc
            op, vals, locs = parse()
            #print(self.name,opc,op)
            if op == 1:
                self._pset(locs[2], vals[0] + vals[1])
            elif op == 2:
                self._pset(locs[2], vals[0] * vals[1])
            elif op == 3:
                assert self.inputq is None
                self.state = 'in'
                self.inputq = locs[0]
                return
            elif op == 4:
                #print(name, 'returning', self._pget(locs[0]))
                assert self.outputq is None
                self.state = 'out'
                self.outputq = vals[0]
                return
            elif op == 5:
                if vals[0] != 0:
                    self.pc = vals[1]
            elif op == 6:
                if vals[0] == 0:
                    self.pc = vals[1]
            elif op == 7:
                self._pset(locs[2], int(vals[0] < vals[1]))
            elif op == 8:
                self._pset(locs[2], int(vals[0] == vals[1]))
            elif op == 9:
                self.relbase += vals[0]
            else:
                assert False


with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    prog = [[int(i) for i in l.split(',')] for l in lines][0]

    qs = [[] for _ in range(50)]
    ps = [Intcode(prog, name=i).send(i) for i in range(50)]

    part1 = True
    nat = None
    lastY = None
    while True:
        if not any(qs) and nat:
            qs[0].append(nat)
            if lastY == nat[1]:
                print(nat[1])
                break
            lastY = nat[1]
            nat = None
        for i in range(50):
            if ps[i].state == 'in':
                if qs[i]:
                    x, y = qs[i].pop(0)
                    ps[i].send(x, y)
                else:
                    ps[i].send(-1)
            while ps[i].state == 'out':
                add = ps[i].nextout()
                x = ps[i].nextout()
                y = ps[i].nextout()
                if add == 255:
                    if part1:
                        print(y)
                        part1 = False
                    nat = x, y
                    continue
                assert 0 <= add <= 49
                qs[add].append((x,y))
