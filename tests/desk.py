
vars = {}

class DeskError:
  pass


import biab.parse

class parser(biab.parse.Parser):
  def __init__(self, infile='<unknown>'):
    biab.parse.Parser.__init__(self, infile)

    
    self.yyactions = {
      2 : self.yyact2,
      3 : self.yyact3,
      5 : self.yyact5,
      6 : self.yyact6,
      7 : self.yyact7,
      8 : self.yyact8,
      9 : self.yyact9,
      10 : self.yyact10,
      11 : self.yyact11,
      12 : self.yyact12,
      13 : self.yyact13,
      }

  YYFINAL = 2
  YYFLAG = None
  YYNTBASE = None
  YYNTOKENS = 13
  YYNNTS = 4
  YYNRULES = 14
  YYNSTATES = 26
  YYMAXUTOK = 259
  YYLAST = 46

  yyprhs = None
  yyrhs = None
  yyrline = None
  yytname = None
  yytoknum = None
  yyr1 = None
  yyr2 = None
  yydefact = None
  yydefgoto = None
  yypact = None
  yypgoto = None
  yytable = None
  yycheck = None
  yyelidables = []

  yycollapsables = []

  yyflattenables = []

  yyphantoms = []

  def yyact2(self, yy):
     print("%g" % (yy[1],)) 

  def yyact3(self, yy):
     vars[yy[1].value] = yy[3] 

  def yyact5(self, yy):
     return yy[0] + yy[2] 

  def yyact6(self, yy):
     return yy[0] - yy[2] 

  def yyact7(self, yy):
     return yy[0] * yy[2] 

  def yyact8(self, yy):
    
            try:
               return yy[0] / yy[2]
            except ZeroDivisionError:
               print("error: division by zero")
               raise DeskError
            

  def yyact9(self, yy):
     return yy[0] 

  def yyact10(self, yy):
     return float(yy[0].value) 

  def yyact11(self, yy):
     return -yy[1] 

  def yyact12(self, yy):
     return yy[1] 

  def yyact13(self, yy):
    
            if vars.has_key(yy[0].value):
                return vars[yy[0].value]
            else:
                print("error: unbound variable `%s'" % (yy[0].value,))
                raise DeskError
            


import re, sys
from biab import lex, token

class lexer(lex.luthor):
    CHAROPS = "+-*/()="
    NEWLINEP = 1

    PATTERNS = {
        'NUMBER' : lex.luthor.NUMBER,
        'IDENTIFIER' : lex.luthor.IDENTIFIER,
        }

    def __init__(self, cb, infile="<unknown>"):
        lex.luthor.__init__(self, cb, infile)

lex = lexer(lambda l, v, line, col:
             p.parse_token(token.token(l, v, line, col)),
            '<stdin>')

while 1:
    l = sys.stdin.readline()
    if not l: break
    # we create a new parser for every line!
    # this permits a crude form of error recovery
    p = parser('<stdin>')
    try: lex.lexline(l)
    except DeskError: pass

sys.exit(0)
