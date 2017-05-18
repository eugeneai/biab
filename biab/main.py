#                                                            -*- Python -*-
#    biab -- the main application class for the biab program
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

import os
import subprocess
import re
import getopt

from . import nosib, lex, meta

from .token import token

from .program import *


class biab_lexer(lex.luthor):
    PATTERNS = {
        'IDENTIFIER': lex.luthor.IDENTIFIER,
        'COLON': re.compile(r'\:'),
        'CHAR': re.compile(r"^\'\\?.\'"),
        'SEMI': re.compile(r'\;'),
        'BAR': re.compile(r'\|'),
        'TOKEN': re.compile(r'\%token'),
        'LEFT': re.compile(r'\%left'),
        'RIGHT': re.compile(r'\%right'),
        'NONASSOC': re.compile(r'\%nonassoc'),
        'ELIDE': re.compile(r'\%elide'),
        'COLLAPSE': re.compile(r'\%collapse'),
        'FLATTEN': re.compile(r'\%flatten'),
        'PHANTOM': re.compile(r'\%phantom'),
        'START': re.compile(r'\%start'),
        'YACCSEP': re.compile(r'^%%'),
    }

    def __init__(self, cb, infile="<unknown>"):
        lex.luthor.__init__(self, cb, infile)
        self.codelevel = 0
        self.code = ''

    def lexchunk(self, l):
        if self.codelevel:
            # machinery for our naive brace balancing
            if l[0] == '{':
                self.codelevel += 1
            elif l[0] == '}':
                self.codelevel -= 1
            c = l[0]
            self.code += c
            l = l[1:]
            if c == "\t":
                self.col += 8
            elif c == "\n":
                self.line += 1
                self.col = 0
            else:
                self.col += 1
            if self.codelevel == 0:
                self.cb('ACTION', self.code, self.codeline, self.codecol)
                self.code = ''

            return l
        elif l[0] == '{':
            self.flush_cruft()
            self.codeline = self.line
            self.codecol = self.col
            self.codelevel = 1
            self.code = l[0]
            self.col += 1
            return l[1:]
        elif l[0] == "\n":
            return l[1:]
        else:
            return lex.luthor.lexchunk(self, l)


def stringtuple2text(ss):
    if not ss:
        return ''
    t = ss[0]
    for s in ss[1:]:
        t += ', ' + s
    return t


def validate_grammar(dex, productions):
    # XXX
    # only terminals or unit nonterminals elidable (+ other ast constraints)
    # no chars as nts
    # valid char tokens..canonicalize wrt escapes
    # no terminals with dots
    # no use of error token, all terminals declared, no terminal used as nt
    # no identical productions
    # no midrule actions

    return 1


def indent(s, n):
    i = n * ' '
    s = i + s
    f = s[-1] == "\n"
    s = s.replace("\n", "\n" + i)
    if f:
        s = s[:-n]
    return s


class biab(program):
    USAGE = "Usage: biab <file>.bb\n"

    def __init__(self):
        program.__init__(self)
        self.NO_CLEAN = 0
        self.DIAGNOSE = 0

    def main(self, args):
        opts, args = getopt.getopt(args, "", [
            'no-clean',
            'diagnose',
        ])

        for opt, val in opts:
            if opt == '--no-clean':
                self.NO_CLEAN = 1
            elif opt == '--diagnose':
                self.DIAGNOSE = 1
            else:
                self.die(self.USAGE)

        # get <prefix>.bb file
        if len(args) != 1:
            self.die(self.USAGE)

        self.check_bison_version(('1.28',))

        infile = args[0]

        if infile.rfind('.bb') != len(infile) - 3:
            self.die(self.USAGE)

        prefix = infile[:-3]

        f = self.open(infile)

        # lex the .bb file, noting semantic actions and outputting a .y file

        p = meta.parser(infile)

        def lexcb(l, v, line, col, p=p):
            if l != 'WHITESPACE':
                p.parse_token(token(l, v, line, col))

        luthor = biab_lexer(lexcb, infile)

        while 1:
            l = f.readline()
            if not l:
                break
            luthor.lexline(l)

        p.parse_eof()

        if p.errorp():
            self.exit(1)

        if not validate_grammar(p.dex, p.productions):
            self.exit(1)

        yfile = prefix + '.y'
        yf = self.open(yfile, 'w')

        # get extended information in the bison-generated .tab.c file
        yf.write("%token-table\n\n")

        self.elidables = []
        self.collapsables = []
        self.flattenables = []
        self.phantoms = []

        for dec in p.dex:
            dectype = dec[0].value
            idents = dec[1]

            if dectype in ('%token', '%left', '%right',
                           '%nonassoc', '%start'):
                yf.write("%s" % (dectype,))
                if hasattr(idents, 'kids'):
                    for i in idents:
                        yf.write(" %s" % (i.value,))
                else:
                    yf.write(" %s" % (idents.value,))
                yf.write("\n\n")
            elif dectype == '%elide':
                self.elidables += idents.kids
            elif dectype == '%collapse':
                self.collapsables += idents.kids
            elif dectype == '%flatten':
                self.flattenables += idents.kids
            elif dectype == '%phantom':
                self.phantoms += idents.kids

        yf.write("%%\n\n")

        nrule = 0
        self.actions = {}

        for prod in p.productions:
            # skip over init actions
            if prod == None:
                continue
            nt = prod[0]
            disjuncts = prod[1]
            yf.write(nt.value)
            first_disjunct = 1
            for disjunct in disjuncts:
                nrule += 1
                if first_disjunct:
                    yf.write("\t:")
                    first_disjunct = 0
                else:
                    yf.write("\t|")
                for i in disjunct:
                    if i.type == 'ACTION':
                        self.actions[nrule] = i.value
                    else:
                        yf.write(" %s" % (i.value,))
                yf.write("\n")
            yf.write("\t;\n\n")

        yf.close()

        # run bison
        if self.DIAGNOSE:
            bison = 'bison -v'
        else:
            bison = 'bison'
        CMD = bison + ' ' + yfile
        # print("Issuing:", CMD)
        if os.system(CMD) != 0:
            self.die("Problem running bison on `%s'!\n" % (yfile,))

        if not self.NO_CLEAN:
            os.remove(yfile)

        # get the definitions we want from the <prefix>.tab.c file
        # bison created
        tabfile = prefix + '.tab.c'

        tf = self.open(tabfile)
        defines, tables = nosib.read_tab(tf, nosib.DEFINES, nosib.TABLES)
        tf.close()

        if not self.NO_CLEAN:
            os.remove(tabfile)

        # generate .py file with defines and tables and actions

        pyfile = prefix + '.py'
        pyf = self.open(pyfile, 'w')

        pyf.write(p.prolog)

        pyf.write("""
import biab.parse

class parser(biab.parse.Parser):
  def __init__(self, infile='<unknown>'):
    biab.parse.Parser.__init__(self, infile)

""")

        pyf.write(indent(p.init, 4))

        pyf.write("\n    self.yyactions = {\n")
        ks = list(self.actions.keys())
        ks.sort()
        for k in ks:
            pyf.write("      %d : self.yyact%d,\n" % (k, k))
        pyf.write("      }\n\n")

        for k, v in defines.items():
            pyf.write("  %s = %s\n" % (k, defines[k]))

        pyf.write("\n")

        for k, v in tables.items():
            pyf.write("  %s = %s" % (k, tables[k]))
            pyf.write("\n")

        def valify(l):
            return [v.value for v in l]

        pyf.write("  yyelidables = %s\n\n" % (valify(self.elidables),))
        pyf.write("  yycollapsables = %s\n\n" % (valify(self.collapsables,)))
        pyf.write("  yyflattenables = %s\n\n" % (valify(self.flattenables,)))
        pyf.write("  yyphantoms = %s\n\n" % (valify(self.phantoms,)))

        ks = list(self.actions.keys())
        ks.sort()
        for k in ks:
            pyf.write("  def yyact%d(self, yy):\n    %s\n\n"
                      % (k, self.actions[k][1:-1]))

        pyf.write(p.postlog)

        pyf.close()

        return 0
        # end main()

    def check_bison_version(self, recommended):
        status, output = subprocess.getstatusoutput('bison --version')
        if status != 0:
            self.die("Problem running bison!  I quit!\n")
        m = re.compile(r'\s+(\S+)\D*$').search(output)
        if not m:
            self.die("Problem parsing bison version from: %s\nI quit!" %
                     (output,))
        v = m.group(1)
        if v not in recommended:
            self.carp("Your bison version is %s; one of (%s) is recommended\n..continuing anyway.\n" % (
                v, stringtuple2text(recommended)))


if __name__ == '__main__':
    p = biab()
    p.run()
