# adapted from an mlyacc example program

%token NUMBER IDENTIFIER

%left '+' '-'        # lowest precedence
%left '*' '/'        # higher precedence

{
vars = {}

class DeskError:
  pass
}

%%
        main:
				# empty	    
            | main expr '\n'    { print "%g" % (yy[1],) }
            | main IDENTIFIER '=' expr '\n'
	      { vars[yy[1].value] = yy[3] }
            | main '\n'
        ;

        expr:
            expr '+' expr       { return yy[0] + yy[2] }
          | expr '-' expr       { return yy[0] - yy[2] }
          | expr '*' expr       { return yy[0] * yy[2] }
          | expr '/' expr       
            { 
              try: return yy[0] / yy[2]
              except ZeroDivisionError:
               print "error: division by zero"
               raise DeskError
            }
	  | primary             { return yy[0] }
        ;

	primary:
            NUMBER              { return float(yy[0].value) }
          | '-' expr		{ return -yy[1] }
          | '(' expr ')'	{ return yy[1] }
          | IDENTIFIER
            { 
              if vars.has_key(yy[0].value): 
                return vars[yy[0].value]
              else: 
                print "error: unbound variable `%s'" % (yy[0].value,)
                raise DeskError
            }
	;

{
import re, string, sys
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
}
