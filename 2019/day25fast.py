import collections
import copy
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
        try:
            return self.prog[i]
        except IndexError:
            return 0
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

def powerset(iterable):
    xs = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(xs,n) for n in range(len(xs)+1)
    )

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    prog = [[int(i) for i in l.split(',')] for l in lines][0]

    p = Intcode(prog)

    rooms = {}
    have = set()
    def traverse(path):
        global p
        state = ''.join(map(chr, p.outputs())).splitlines()
        roomname = state[3]
        assert roomname.startswith('== '), state
        if roomname in rooms:
            return
        rooms[roomname] = path

        if 'Items here:' in state:
            it = state[state.index('Items here:')+1][2:]
            assert not state[state.index('Items here:')+2].startswith('- ')
            if it not in ('escape pod', 'infinite loop', 'giant electromagnet', 'photons', 'molten lava'):
                p = p.send(*(ord(c) for c in f'take {it}\n'))
                tkm = ''.join(map(chr, p.outputs())).splitlines()
                print('took', tkm)
                assert p.state != 'stopped'
                have.add(it)

        for direc in ['north', 'south', 'east', 'west']:
            if f'- {direc}' in state:
                p.send(*(ord(c) for c in f'{direc}\n'))
                traverse(path + (direc,))
                bw = {
                    'north': 'south',
                    'south': 'north',
                    'east': 'west',
                    'west': 'east',
                }
                p.send(*(ord(c) for c in f'{bw[direc]}\n'))
                list(p.outputs())
    traverse(())

    for step in rooms['== Security Checkpoint ==']:
        p.send(*(ord(c) for c in f'{step}\n'))
        list(p.outputs())

    for it in have:
        p.send(*(ord(c) for c in f'drop {it}\n'))
        list(p.outputs())

    for ss in powerset(have):
        p2 = copy.deepcopy(p)
        for it in ss:
            p2.send(*(ord(c) for c in f'take {it}\n'))
            list(p2.outputs())
        p2.send(*(ord(c) for c in f'west\n'))
        o = ''.join(map(chr, p2.outputs())).splitlines()
        print(ss)
        if p2.state == 'stopped':
            print('\n'.join(o))
            break
