
import biab.parse

class parser(biab.parse.Parser):
  def __init__(self, infile='<unknown>'):
    biab.parse.Parser.__init__(self, infile)

    
    self.yyactions = {
      }

  YYFINAL = 61
  YYFLAG = None
  YYNTBASE = None
  YYNTOKENS = 85
  YYNNTS = 64
  YYNRULES = 212
  YYNSTATES = 350
  YYMAXUTOK = 315
  YYLAST = 1301

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

