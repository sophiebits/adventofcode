import collections
import array
import math
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]

    digits = array.array('b', [int(c) for c in list(lines[0])]* 10000)
    offset = int(''.join(str(c) for c in digits[:7]))

    q = [0, 1, 0, -1]
    # pds = [None]
    # for x in range(2, len(digits) + 10):
    #     pd = {}

    #     ox = x - 1

    #     op = ox - 1
    #     oc = 0
    #     np = x - 1
    #     nc = 0

    #     while op < len(digits) or np < len(digits):
    #         if op <= np:
    #             oc += 1
    #             oc %= 4
    #             if q[nc] - q[oc]:
    #                 for i in range(op, min(np, len(digits))):
    #                     pd[i] = q[nc] - q[oc]
    #             op += ox
    #         else:
    #             nc += 1
    #             nc %= 4
    #             if q[nc] - q[oc]:
    #                 for i in range(np, min(op, len(digits))):
    #                     pd[i] = q[nc] - q[oc]
    #             np += x

    #     #for y in range(0, len(digits)):
    #     #    dif = q[(y + 1) // x % 4] - (q[(y + 1) // (x-1) % 4] if x>1 else 0)
    #     #    if dif != 0:
    #     #        pd[y] = dif
    #     pds.append(pd)
    #     print(x, len(pd))
    # #print(pds)
    # print([len(pd) for pd in pds if pd is not None])
    #        if i <= 2:
    #            n = sum(
    #                q[(j + 1) // i % 4] * b
    #                for j, b in enumerate(digits)
    #                if (j+1) // i % 2
    #            )
    #            #print(',', i, digits, n)
    #        else:
    #            pd = pds[i-1]
    #            n += sum(
    #                digits[idx] * mul
    #                for idx, mul in pd.items()
    #            )
    #            #print(',', i, digits, pd, n)

    ld = len(digits)
    for x in range(100):
        ps = array.array('l', [0])
        pss = 0
        for d in digits:
            pss += d
            ps.append(pss)
        assert len(ps) == ld+1

        ds = array.array('b',[])
        n = None
        for i, d in enumerate(digits, 1):
            n = 0
            #print(digits)
            for startof1 in range(i-1, ld, 4*i):
                endof1 = startof1 + i
                n += ps[min(endof1, ld)] - ps[startof1]
                #print('+', startof1, endof1, '=', ps[min(endof1, ld)] - ps[startof1])
            for startofn1 in range(3*i-1, ld, 4*i):
                endofn1 = startofn1 + i
                n -= ps[min(endofn1, ld)] - ps[startofn1]
                #print('-', startofn1, endofn1, '=', ps[min(endofn1, ld)] - ps[startofn1])
            ds.append(abs(n) % 10)
            #print('=>', n, 'from', ds[-1])

        digits = ds
        #print(ds)
        print(x, ''.join(str(c) for c in ds[0:0+8]))

    print(''.join(str(c) for c in ds[0:0+8]))
    print(''.join(str(c) for c in ds[offset:offset+8]))
