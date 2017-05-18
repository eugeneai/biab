
import biab.parse

class parser(biab.parse.Parser):
  def __init__(self, infile='<unknown>'):
    biab.parse.Parser.__init__(self, infile)

    
    self.yyactions = {
      2 : self.yyact2,
      }

  YYFINAL = 2
  YYFLAG = None
  YYNTBASE = None
  YYNTOKENS = 13
  YYNNTS = 5
  YYNRULES = 15
  YYNSTATES = 26
  YYMAXUTOK = 259
  YYLAST = 36

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
  yyelidables = ["'('", "')'"]

  yycollapsables = ['expr', 'primary']

  yyflattenables = []

  yyphantoms = ['primary']

  def yyact2(self, yy):
     print(yy[1]) 


import re, string, sys
import biab.lex, biab.token

class lexer(biab.lex.luthor):
    CHAROPS = "+-*/()="
    NEWLINEP = 1

    PATTERNS = {
        'NUMBER' : biab.lex.luthor.NUMBER,
        'IDENTIFIER' : biab.lex.luthor.IDENTIFIER,
        }

    def __init__(self, cb, infile="<unknown>"):
        biab.lex.luthor.__init__(self, cb, infile)

def main():

    lex = lexer(lambda l, v, line, col:
                 p.parse_token(biab.token.token(l, v, line, col)),
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

if __name__=="__main__":
    main()

