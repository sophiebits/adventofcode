import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

# part 1:
# acc = 0
# pc = 0
# seen = set()
# while True:
#     if pc in seen:
#         print(acc)
#         break
#     seen.add(pc)
#     line = lines[pc]
#     inst, arg = line.split()
#     arg = int(arg)
#
#     if inst == 'jmp':
#         pc += arg
#         continue
#     if inst == 'acc':
#         acc += arg
#     if inst == 'nop':
#         pass
#
#     pc += 1

def tryprog(prog):
    acc = 0
    pc = 0
    seen = set()
    while True:
        if pc == len(prog):
            return acc
        if pc in seen:
            return None
        seen.add(pc)
        line = prog[pc]
        inst, arg = line.split()
        arg = int(arg)

        if inst == 'jmp':
            pc += arg
            continue
        if inst == 'acc':
            acc += arg
        if inst == 'nop':
            pass

        pc += 1

for i in range(len(lines)):
    prog = lines[:]
    if prog[i].startswith('jmp'):
        prog[i] = prog[i].replace('jmp', 'nop')
    elif prog[i].startswith('nop'):
        prog[i] = prog[i].replace('nop', 'jmp')
    x = tryprog(prog)
    if x:
        print(x)