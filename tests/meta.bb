# our meta-grammar

%token IDENTIFIER COLON SEMI BAR ACTION YACCSEP 
%token TOKEN LEFT RIGHT NONASSOC START CHAR ELIDE COLLAPSE FLATTEN PHANTOM

%flatten idents disjunct disjuncts dex grammar
%elide COLON BAR SEMI

%start ox

%%

{
self.prolog = ''
self.init = ''
self.postlog = ''
}

ox		: dex YACCSEP grammar
		  { self.dex = yy[0]; self.productions = yy[2] }
		| dex YACCSEP grammar ACTION
		  { self.dex = yy[0]; self.productions = yy[2]; self.postlog = yy[3].value[1:-1] }
		;

dex		: dex dec
		| dex ACTION
		  {self.prolog += yy[1].value[1:-1] + "\n"; return yy[0]}
		|
		;

dec		: TOKEN idents
		| LEFT idents	
		| RIGHT idents	
		| NONASSOC idents
		| ELIDE idents		
		| COLLAPSE idents	
		| FLATTEN idents	
		| PHANTOM idents	
		| START IDENTIFIER	
		;

idents		: idents IDENTIFIER	
		| idents CHAR		
		|			
		;

grammar 	: grammar production 
		| production
		| ACTION		{self.init += yy[0].value[1:-1] + "\n"}
		;

production	: IDENTIFIER COLON disjuncts SEMI
		;

disjuncts	: disjuncts BAR disjunct
		| disjunct		
    		;

disjunct	: 			
		| disjunct IDENTIFIER	
		| disjunct CHAR
		| disjunct ACTION
		;
