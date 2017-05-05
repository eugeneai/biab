
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

  YYLAST = 34
  YYFLAG = -32768
  YYNRULES = 27
  YYNSTATES = 43
  YYNTOKENS = 19
  YYNNTS = 8
  YYNTBASE = 19
  YYFINAL = 42
  YYMAXUTOK = 272

  yyr2 = [     0,
     3,     4,     2,     2,     0,     2,     2,     2,     2,     2,
     2,     2,     2,     2,     2,     2,     0,     2,     1,     1,
     4,     3,     1,     0,     2,     2,     2
    ]

  yyrline = [ 0,
    11,    12,    15,    16,    17,    20,    21,    22,    23,    24,
    25,    26,    27,    28,    31,    32,    33,    36,    37,    38,
    41,    44,    45,    48,    49,    50,    51
    ]

  yypact = [-32768,
    -7,-32768,    10,-32768,-32768,-32768,-32768,    11,-32768,-32768,
-32768,-32768,-32768,    26,-32768,    12,-32768,     4,     4,     4,
     4,-32768,     4,     4,     4,     4,-32768,-32768,-32768,-32768,
-32768,    23,     9,-32768,-32768,-32768,-32768,-32768,     9,    31,
    32,-32768
    ]

  yyr1 = [     0,
    19,    19,    20,    20,    20,    21,    21,    21,    21,    21,
    21,    21,    21,    21,    22,    22,    22,    23,    23,    23,
    24,    25,    25,    26,    26,    26,    26
    ]

  yyrhs = [    20,
     8,    23,     0,    20,     8,    23,     7,     0,    20,    21,
     0,    20,     7,     0,     0,     9,    22,     0,    10,    22,
     0,    11,    22,     0,    12,    22,     0,    15,    22,     0,
    16,    22,     0,    17,    22,     0,    18,    22,     0,    13,
     3,     0,    22,     3,     0,    22,    14,     0,     0,    23,
    24,     0,    24,     0,     7,     0,     3,     4,    25,     5,
     0,    25,     6,    26,     0,    26,     0,     0,    26,     3,
     0,    26,    14,     0,    26,     7,     0
    ]

  yydefact = [     5,
     0,     4,     0,    17,    17,    17,    17,     0,    17,    17,
    17,    17,     3,     0,    20,     1,    19,     6,     7,     8,
     9,    14,    10,    11,    12,    13,    24,     2,    18,    15,
    16,     0,    23,    21,    24,    25,    27,    26,    22,     0,
     0,     0
    ]

  yytable = [     2,
     3,     4,     5,     6,     7,     8,    30,     9,    10,    11,
    12,    36,    14,    22,    14,    37,    15,    31,    28,    19,
    20,    21,    38,    23,    24,    25,    26,    34,    35,    27,
    41,    42,    29,    39
    ]

  yytname = [   "$","error","$undefined.","IDENTIFIER",
"COLON","SEMI","BAR","ACTION","YACCSEP","TOKEN","LEFT","RIGHT","NONASSOC","START",
"CHAR","ELIDE","COLLAPSE","FLATTEN","PHANTOM","ox","dex","dec","idents","grammar",
"production","disjuncts","disjunct", None
    ]

  yyprhs = [     0,
     0,     4,     9,    12,    15,    16,    19,    22,    25,    28,
    31,    34,    37,    40,    43,    46,    49,    50,    53,    55,
    57,    62,    66,    68,    69,    72,    75
    ]

  yytoknum = [ 0,
   256,     2,   257,   258,   259,   260,   261,   262,   263,   264,
   265,   266,   267,   268,   269,   270,   271,   272,     0
    ]

  yycheck = [     7,
     8,     9,    10,    11,    12,    13,     3,    15,    16,    17,
    18,     3,     3,     3,     3,     7,     7,    14,     7,     5,
     6,     7,    14,     9,    10,    11,    12,     5,     6,     4,
     0,     0,    16,    35
    ]

  yypgoto = [-32768,
-32768,-32768,    15,-32768,    17,-32768,    -1
    ]

  yydefgoto = [    40,
     1,    13,    18,    16,    17,    32,    33
    ]

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

