import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

def domask(arg, mask):
    arg |= int(mask.replace('X', '0'), 2)
    arg &= int(mask.replace('X', '1'), 2)
    return arg

def allmasks(pos, mask):
    if not mask:
        yield 0
    else:
        # (yes, I probably could have done the ifs *inside* the loop...)
        if mask[-1] == '0':
            for m in allmasks(pos // 2, mask[:-1]):
                yield 2*m + pos % 2
        if mask[-1] == '1':
            for m in allmasks(pos // 2, mask[:-1]):
                yield 2*m + 1
        if mask[-1] == 'X':
            for m in allmasks(pos // 2, mask[:-1]):
                yield 2*m + 0
                yield 2*m + 1

# part 2 alternate solution, written later:
# def allmasks(mask):
#     if not mask:
#         yield ''
#         return
#     for m in allmasks(mask[1:]):
#         if mask[0] == '0':
#             yield 'X' + m  # leave unchanged
#         elif mask[0] == '1':
#             yield '1' + m  # replace with 1
#         elif mask[0] == 'X':
#             yield '0' + m  # replace with 0
#             yield '1' + m  # replace with 1


mask = None
mem = collections.defaultdict(int)
for line in lines:
    op, arg = line.split(' = ')
    if op == 'mask':
        mask = arg
    else:
        pos = int(op[4:-1])
        # part 1:
        # mem[pos] = domask(int(arg), mask)
        for m in allmasks(pos, mask):
            mem[m] = int(arg)
        # part 2 alternate solution:
        # for m in allmasks(mask):
        #     mem[domask(pos, m)] = int(arg)

print(sum(mem.values()))
