import collections
import copy
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
    #lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]
    prog = [[int(i) for i in l.split(',')] for l in lines][0]

    p = Intcode(prog)

    bfs = collections.deque([(0, 0, frozenset(), p)])
    seen = {}
    rooms = {}
    msgseen = set()
    while bfs:
        x, y, ic, p = bfs.popleft()
        #if (x,y, ic) in seen:
        #    continue
        #seen[(x,y,ic)]=True
        state = ''.join(map(chr, p.outputs())).splitlines()
        if len(state) >= 5:
            roomname = state[4]
            if (roomname,ic) in seen:
                continue
            seen[(roomname,ic)] = True
        else:
            print('huh?', ic, state)
            break
        print(x, y, ic)
        state1 = ' '.join(state)
        if state1 not in msgseen:
            msgseen.add(state1)
            print(state1)
        if "You can't go that way." in state:
            continue
        #if '== Security Checkpoint ==' in state:
        #    p.send(*(ord(c) for c in 'inv\n'))
        #    its = frozenset([l[2:] for l in ''.join(map(chr, p.outputs())).splitlines() if l.startswith('- ')])
        #    print(ic == its)
        #if '== Arcade ==' in state and 'fuel cell' in ic:
        #    p.send(*(ord(c) for c in 'drop fuel cell\n'))
        #    print(''.join(map(chr, p.outputs())).splitlines())
        def f(p, ic):
            if '- north' in state:
                bfs.append((x-1,y,ic, copy.deepcopy(p).send(*(ord(c) for c in 'north\n'))))
            if '- south' in state:
                bfs.append((x+1,y,ic, copy.deepcopy(p).send(*(ord(c) for c in 'south\n'))))
            if '- east' in state:
                # I typoed this line as 'west\n' and ended up never traversing the 'east' branches
                bfs.append((x,y+1,ic, copy.deepcopy(p).send(*(ord(c) for c in 'east\n'))))
            if '- west' in state:
                bfs.append((x,y-1,ic, copy.deepcopy(p).send(*(ord(c) for c in 'west\n'))))
        f(p, ic)
        if 'Items here:' in state:
            it = state[state.index('Items here:')+1][2:]
            assert not state[state.index('Items here:')+2].startswith('- ')
            if it not in ('escape pod', 'infinite loop', 'giant electromagnet', 'photons'):
                p2 = copy.deepcopy(p).send(*(ord(c) for c in f'take {it}\n'))
                tkm = ''.join(map(chr, p2.outputs())).splitlines()
                print('took', tkm)
                if p2.state != 'stopped':
                    f(p2, ic.union([it]))
        #for it in ic:
        #    p2 = copy.deepcopy(p).send(*(ord(c) for c in f'drop {it}\n'))
        #    print('dropped', ''.join(map(chr, p2.outputs())).splitlines())
        #    if p2.state != 'stopped':
        #        f(p2, ic.difference([it]))


    #print(state)
    #p.send(*(ord(c) for c in 'north\n'))
    #state = ''.join(map(chr, p.outputs())).splitlines()
    #print(state)
    #p.send(*(ord(c) for c in 'north\n'))
    #state = ''.join(map(chr, p.outputs())).splitlines()
    #print(state)
