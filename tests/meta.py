
import biab.parse

class parser(biab.parse.Parser):
  def __init__(self, infile='<unknown>'):
    biab.parse.Parser.__init__(self, infile)

    
    self.prolog = ''
    self.init = ''
    self.postlog = ''
    

    self.yyactions = {
      1 : self.yyact1,
      2 : self.yyact2,
      4 : self.yyact4,
      20 : self.yyact20,
      }

  YYFINAL = 3
  YYFLAG = None
  YYNTBASE = None
  YYNTOKENS = 19
  YYNNTS = 9
  YYNRULES = 28
  YYNSTATES = 42
  YYMAXUTOK = 273
  YYLAST = 33

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
  yyelidables = ['COLON', 'BAR', 'SEMI']

  yycollapsables = []

  yyflattenables = ['idents', 'disjunct', 'disjuncts', 'dex', 'grammar']

  yyphantoms = []

  def yyact1(self, yy):
     self.dex = yy[0]; self.productions = yy[2] 

  def yyact2(self, yy):
     self.dex = yy[0]; self.productions = yy[2]; self.postlog = yy[3].value[1:-1] 

  def yyact4(self, yy):
    self.prolog += yy[1].value[1:-1] + "\n"; return yy[0]

  def yyact20(self, yy):
    self.init += yy[0].value[1:-1] + "\n"

