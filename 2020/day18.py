import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin]

def solve(line):
    def doInner(inner):
        # part 1:
        # while '+' in inner or '*' in inner:
        #     inner = re.sub('^(\d+)\s*\+\s*(\d+)', lambda m: str(int(m.group(1)) + int(m.group(2))), inner)
        #     inner = re.sub('^(\d+)\s*\*\s*(\d+)', lambda m: str(int(m.group(1)) * int(m.group(2))), inner)
        while '+' in inner:
            inner = re.sub('(\d+)\s*\+\s*(\d+)', lambda m: str(int(m.group(1)) + int(m.group(2))), inner)
        while '*' in inner:
            inner = re.sub('(\d+)\s*\*\s*(\d+)', lambda m: str(int(m.group(1)) * int(m.group(2))), inner)
        return inner
    while '(' in line:
        def doExpr(match):
            inner = match.group(1)
            return doInner(inner)
        line = re.sub(r'\(([^()]+)\)', doExpr, line)
    return doInner(line)

total = 0
for line in lines:
    total += int(solve(line))

print(total)