#                                                            -*- Python -*-
#    nosib  -  grab data from .tab.c ouput of bison 1.28
#    Copyright (C) 2001  Eric S. Tiedemann <est@hyperreal.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import sys
import os
import re

# typical entities of interest
# (some of these require the %token-table directive in bison 1.28)
DEFINES = ('YYFINAL', 'YYFLAG', 'YYNTBASE', 'YYNTOKENS', 'YYNNTS',
           'YYNRULES', 'YYNSTATES', 'YYMAXUTOK', 'YYLAST')

TABLES = ('yyprhs', 'yyrhs', 'yyrline', 'yytname', 'yytoknum',
          'yyr1', 'yyr2', 'yydefact', 'yydefgoto',
          'yypact', 'yypgoto', 'yytable', 'yycheck')

# very bison-specific patterns (derived from version 1.28)
TABLE_RE = re.compile(
    r'^static const [a-zA-Z_]+ ([a-zA-Z0-9_]+)\[\] \= \{(.*\n)')
TABLE_END_RE = re.compile(r'^\}\;')
DEFINE_RE = re.compile(r'^\#define\s+([a-zA-Z0-9_]+)\s+(\-?\d+)')


def read_tab(f, ds, ts):
    '''
    read_tab(f, ds, ts) Read a yacc/bison .tab.c file from file F
    and return two dicts of defines and tables.  The dicts are indexed
    by the names requested via DS and TS and their values are integers
    and tuples respectively.
    '''

    defines = {}
    for d in ds:
        defines[d] = None

    tables = {}
    for t in ts:
        tables[t] = None

    while 1:
        l = f.readline()

        if not l:
            break

        m = TABLE_RE.match(l)
        if m:
            print("Matched beg:", m)
            name = m.group(1)
            if name in tables:
                out = '[' + m.group(2)
                while 1:
                    l = f.readline()
                    if not l or TABLE_END_RE.match(l):
                        out = out.replace('NULL', 'None')
                        tables[name] = out + '    ]\n'
                        break
                    else:
                        out += l

        m = DEFINE_RE.match(l)
        if m:
            print("Matched end:", m)
            name = m.group(1)
            if name in defines:
                defines[name] = m.group(2)

    return defines, tables


if __name__ == '__main__':
    import sys

    d, t = read_tab(sys.stdin, DEFINES, TABLES)

    for i in t.items():
        print("%s = %s" % i)

    for i in d.items():
        print("%s = %s" % i)

    sys.exit(0)
