import collections
import math
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]

    pic = list(lines[0])
    image = pic[:25*6]

    fewest = 1000000000
    ott = 0
    while pic:
        layer = pic[:25*6]
        pic = pic[25*6:]

        # part 1
        zs = layer.count('0')
        if zs < fewest:
            fewest = zs
            ott = layer.count('1') * layer.count('2')

        # part 2
        s = ''
        for lc, ic in zip(layer, image):
            if ic == '2':
                s += lc
            else:
                s += ic
        image = s

    print(ott)
    for i in range(6):
        print(image[i*25:(i+1)*25].replace('0', ' '))


