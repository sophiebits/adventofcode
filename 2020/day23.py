import collections
from fractions import Fraction
import math
import re
import sys

line = [int(i) for i in [l.rstrip('\n') for l in sys.stdin][0]]

# part 1 (rearrange the final answer by hand):
# def step(line):
#     three = line[1:4]
#     dest = int(line[0]) - 1
#     if dest == 0:
#         dest = int(max(line))
#     while dest in three:
#         dest -= 1
#         if dest == 0:
#             dest = int(max(line))
#     idx = line.index(dest)
#     a, b = line[:idx], line[idx+1:]
#     return a[4:] + [dest] + three + b + [line[0]]
# for _ in range(100):
#     line = step(line)
# print(line)


class Node:
    __slots__ = ('value', 'next')
    def __init__(self, value):
        self.value = value
        self.next = None

def run(line, steps=100):
    nodes = {num: Node(num) for num in line}
    for num, num2 in zip(line, line[1:] + line[:1]):
        nodes[num].next = nodes[num2]
    front = nodes[line[0]]
    for stepno in range(steps):
        a = front.next
        b = a.next
        c = b.next

        look = front.value
        while True:
            look -= 1
            if look == 0:
                look = len(line)
            if look not in (a.value, b.value, c.value):
                break

        after = nodes[look]
        front.next, front, after.next, c.next = c.next, c.next, a, after.next

        if stepno % 500000 == 0:
            print(stepno)

    print(nodes[1].next.value * nodes[1].next.next.value)

line.extend(range(10, 10 ** 6 + 1))
run(line, 10 ** 7)
