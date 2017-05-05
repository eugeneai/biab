#                                                            -*- Python -*-
#    lex -- a simple lexer class
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

# TODO
# postprocessing of keywords
# genericize (e.g., ws and patterns args)
# line matches (e.g. for yacc separator)
# string and comment nesting
# language-specific action scans

import re, string, sys

class luthor:
    COMMENT = re.compile(r'^\#.*')
    IDENTIFIER = re.compile(r'^[a-zA-Z_\.][a-zA-Z0-9_\.]*')
    NUMBER = re.compile(r'^(\d+(\.\d*)?|\d*\.\d+)')
    WHITESPACE = re.compile(r'^\s+')

    CHAROPS = ''
    PATTERNS = {}

    NEWLINEP = 0
    
    def __init__(self, cb, infile="<unknown>"):
        self.cb = cb
        self.infile = infile
        self.line = 0
        self.cruft = ''
        self.errorp = 0
        
    def lexline(self, l):
        self.l0 = l                          # for error reporting
        self.line += 1
        self.col = 0
        
        while l:
            l = self.lexchunk(l)

    def lexchunk(self, l):
        if self.COMMENT.match(l):
            return ''
        elif l[0] == '\t':
            l = l[1:]
            self.col = (self.col/8 + 1) * 8
            return l
        elif l[0] == ' ':
            l = l[1:]
            self.col += 1
            return l
        elif l[0] == "\n":
            l = l[1:]
            # we should be fed single lines
            assert not l
            self.flush_cruft()
            if self.NEWLINEP:
                self.cb("'\\n'", 'newline', self.line, self.col)
            self.col += 1
            l = l[1:]
            return l
        else:
            for c in self.CHAROPS:
                if c == l[0]:
                  self.flush_cruft()
                  self.cb("'%s'" % (l[0],), l[0], self.line, self.col)
                  self.col += 1
                  l = l[1:]
                  return l

            for lexeme, regexp in self.PATTERNS.items():
                m = regexp.match(l)
                if m:
                    self.flush_cruft()
                    self.cb(lexeme, m.group(), self.line, self.col)
                    l = l[m.end():]
                    self.col += m.end()
                    return l

            self.cruft += l[0]
            l = l[1:]
            self.col += 1
            return l

    def error(self, msg):
        sys.stderr.write("\"%s\", line %d: %s\n"
                         % (self.infile, self.line, msg))
        self.errorp = 1
        
    def flush_cruft(self):
        if self.cruft:
            self.error("unlexable characters `%s'" % (self.cruft,))
        self.cruft = ''

if __name__ == '__main__':
    import sys
    
    def foo(l, v, line, col):
        print l, v
        
    lex = luthor(foo)

    while 1:
        l = sys.stdin.readline()
        if not l: break
        lex.lexline(l)

    sys.exit(0)
