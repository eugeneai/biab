#!/usr/bin/env python
#
# -*- Python -*-
#
# ppp - very crude python preprocessor
#
# analogous to cpp, this only handles ifdef and endif
#
# TODO
# -D
# detect nesting errors

import sys, re, getopt

defined = {}

opts, args = getopt.getopt(sys.argv[1:],
                           'D:',
                           [
    'define=',
    ])

for opt, val in opts:
    if opt == '--define' or opt == '-D':
        defined[val] = 1

stack = [1]

ifdef = re.compile(r'^\#ifdef\s+(\w+)')
endif = re.compile(r'^\#endif\s*(\#.*)?$')

rc = 0

while 1:
    l = sys.stdin.readline()
    if not l:
        if len(stack) != 1:
            sys.stderr.write("ppp: unclosed #ifdef!\n")
            rc = 1
        break
    m = ifdef.match(l)
    if m:
        if defined.has_key(m.group(1)):
            stack.append(1)
        else:
            stack.append(0)
        continue
    m = endif.match(l)
    if m:
        stack.pop()
        continue
    if stack[-1]:
        sys.stdout.write(l)

sys.exit(rc)
