# adapted from an mlyacc example program

%token NUMBER IDENTIFIER

%left '+' '-'        # lowest precedence
%left '*' '/'        # higher precedence

%elide '(' ')'
%collapse expr primary
%phantom primary

%%
        main:
				# empty	    
            | main stmt '\n'    { print yy[1] }
            | main '\n'
        ;

	stmt:
              expr
            | IDENTIFIER '=' expr
        ;

        expr:
            expr '+' expr
          | expr '-' expr
          | expr '*' expr
          | expr '/' expr       
	  | primary
        ;

	primary:
            NUMBER 
          | IDENTIFIER
	  | '-' primary
          | '(' expr ')'
	;

{
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
}
