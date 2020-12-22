import collections
import math
import re
import sys

decks = [l.rstrip('\n') for l in sys.stdin.read().split('\n\n')]
decks = [[int(i) for i in re.findall(r'(?<=\n)(\d+)', l)] for l in decks]

a, b = decks
a = collections.deque(a)
b = collections.deque(b)

# part 1:
# while a and b:
#     aa = a.popleft()
#     bb = b.popleft()
#     if aa > bb:
#         winner = a
#     elif bb > aa:
#         winner = b
#     else:
#         assert False, aa
#     winner.append(max(aa, bb))
#     winner.append(min(aa, bb))
# winner = a or b

def combat(a, b):
    seen = set()
    while a and b:
        kk = (tuple(a), tuple(b))
        if kk in seen:
            return 1, a
        seen.add(kk)
        aa = a.popleft()
        bb = b.popleft()
        if len(a) >= aa and len(b) >= bb:
            winnum, _ = combat(
                collections.deque(list(a)[:aa]),
                collections.deque(list(b)[:bb]),
            )
            winner = a if winnum == 1 else b
        else:
            if aa > bb:
                winner = a
            elif bb > aa:
                winner = b
            else:
                assert False, aa
        winner.append(aa if winner is a else bb)
        winner.append(aa if winner is not a else bb)
    return 1 if winner is a else 2, winner
winnum, winner = combat(a, b)

print(sum(i * v for i, v in enumerate(reversed(winner), 1)))
