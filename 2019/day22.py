import collections
import math
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    nlines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]

    ld = 10007
    deck = list(range(ld))
    for line, nline in zip(lines, nlines):
        if line.startswith('deal with increment'):
            ndeck = [0] * ld
            inc = nline[0]
            for i in range(ld):
                ndeck[i * inc % ld] = deck[i]
            assert len(set(ndeck)) == ld
        elif line.startswith('cut'):
            inc = nline[0]
            ndeck = deck[inc:] + deck[:inc]
        elif line == 'deal into new stack':
            ndeck = deck[::-1]
        else:
            assert False, line
        #print(line, deck.index(2019))
        deck = ndeck
    print(deck.index(2019))

    ld = 119315717514047
    card = 2020
    times = 101741582076661
    # ld, card, times = 10007, 7665, 1

    # q came from aq + b
    a = 1
    b = 0
    for line, nline in reversed(list(zip(lines, nlines))):
        if line.startswith('deal with increment'):
            inc = nline[0]
            #card = card * pow(inc, ld-2,ld) % ld
            p = pow(inc, ld-2,ld)
            a *= p
            b *= p
        elif line.startswith('cut'):
            inc = nline[0]
            #card = (card - inc + ld) % ld
            b += inc
        elif line == 'deal into new stack':
            #card = ld - 1 - card
            b += 1
            a *= -1
            b *= -1
        else:
            assert False, line
        a %= ld
        b %= ld
        # print(line, (a * card + b) % ld)

    # q
    # aq + b
    # a(aq+b) + b = a^2q + ab + b
    # a(a^2q + ab + b) = a^3q + a^2b + ab + b
    # ...
    # a^t q + b * (a^t - 1) / (a - 1)
    print((
        pow(a, times, ld) * card +
        b * (pow(a, times, ld) +ld- 1)
          * (pow(a-1, ld - 2, ld))
    ) % ld)