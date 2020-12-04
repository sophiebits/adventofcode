import collections
import math
import re
import sys

lines = [l.rstrip('\n') for l in sys.stdin.read().split('\n\n')]


ALL = {'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'}

valid = 0
# part 1:
# for line in lines:
#     chunks = re.findall(r'(\w+):', line)
#     if len(ALL - set(chunks)) == 0:
#         valid += 1
for line in lines:
    chunks = re.findall(r'(\w+):(\S+)', line)

    if len(ALL - set(c[0] for c in chunks)) != 0:
        continue

    allvalid = True
    for typ, val in chunks:
        isv = False
        if typ == 'byr':
            isv = 1920 <= int(val) <= 2002
        elif typ == 'iyr':
            isv = 2010 <= int(val) <= 2020
        elif typ == 'eyr':
            isv = 2020 <= int(val) <= 2030
        elif typ == 'hgt':
            if val.endswith('cm'):
                isv = 150 <= int(val[:-2]) <= 193
            elif val.endswith('in'):
                isv = 59 <= int(val[:-2]) <= 76
        elif typ == 'hcl':
            isv = bool(re.fullmatch(r'#[0-9a-f]{6}', val))
        elif typ == 'ecl':
            isv = val in 'amb blu brn gry grn hzl oth'.split()
        elif typ == 'pid':
            isv = bool(re.fullmatch(r'[0-9]{9}', val))
        elif typ == 'cid':
            isv = True

        allvalid = allvalid and isv

    if allvalid:
        valid += 1

print(valid)