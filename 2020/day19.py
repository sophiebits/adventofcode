import collections
import math
import re
import sys

rules, strings = [l.rstrip('\n') for l in sys.stdin.read().split('\n\n')]

rules = dict([rule.split(': ', 1) for rule in rules.split('\n')])
def getre(rulenum):
    # for part 1, delete these two rules:
    if rulenum == '8':
        return getre('42') + '+'
    elif rulenum == '11':
        a = getre('42')
        b = getre('31')
        return '(?:' + '|'.join(f'{a}{{{n}}}{b}{{{n}}}' for n in range(1, 100)) + ')'

    rule = rules[rulenum]
    if re.fullmatch(r'"."', rule):
        return rule[1]
    else:
        parts = rule.split(' | ')
        res = []
        for part in parts:
            nums = part.split(' ')
            res.append(''.join(getre(num) for num in nums))
        return '(?:' + '|'.join(res) + ')'


z = getre('0')
ct = 0
for string in strings.split('\n'):
    ct += bool(re.fullmatch(z, string))
print(ct)
