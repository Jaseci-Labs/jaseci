grammar jac;

/* Sentinels handle these top rules */
start: element+ EOF;

element: architype | walker;

architype:
	KW_NODE NAME (COLON INT)? attr_block
	| KW_EDGE NAME attr_block
	| KW_GRAPH NAME graph_block;

walker:
	KW_WALKER NAME LBRACE attr_stmt* walk_entry_block? (
		statement
		| walk_activity_block
	)* walk_exit_block? RBRACE;

walk_entry_block: KW_WITH KW_ENTRY code_block;

walk_exit_block: KW_WITH KW_EXIT code_block;

walk_activity_block: KW_WITH KW_ACTIVITY code_block;

attr_block: LBRACE (attr_stmt)* RBRACE | COLON attr_stmt | SEMI;

attr_stmt: has_stmt | can_stmt;

graph_block: graph_block_spawn | graph_block_dot;

graph_block_spawn:
	LBRACE has_root KW_SPAWN code_block RBRACE
	| COLON has_root KW_SPAWN code_block SEMI;

graph_block_dot:
	LBRACE has_root dot_graph RBRACE
	| COLON has_root dot_graph SEMI;

has_root: KW_HAS KW_ANCHOR NAME SEMI;

has_stmt: KW_HAS KW_PRIVATE? KW_ANCHOR? NAME (COMMA NAME)* SEMI;

def_assign: NAME | NAME EQ expression;

/* Need to be heavily simplified */ can_stmt:
	KW_CAN dotted_name preset_in_out? event_clause? (
		COMMA dotted_name preset_in_out? event_clause?
	)* SEMI
	| KW_CAN NAME event_clause? code_block;

event_clause: KW_WITH (KW_ENTRY | KW_EXIT | KW_ACTIVITY);

preset_in_out:
	DBL_COLON NAME (COMMA NAME)* (DBL_COLON | COLON_OUT NAME)?;

dotted_name: NAME (DOT NAME)*;

code_block: LBRACE statement* RBRACE | COLON statement;

node_ctx_block: NAME (COMMA NAME)* code_block;

statement:
	code_block
	| node_ctx_block
	| expression SEMI
	| if_stmt
	| for_stmt
	| while_stmt
	| ctrl_stmt SEMI
	| report_action
	| walker_action;

if_stmt: KW_IF expression code_block (elif_stmt)* (else_stmt)?;

elif_stmt: KW_ELIF expression code_block;

else_stmt: KW_ELSE code_block;

for_stmt:
	KW_FOR expression KW_TO expression KW_BY expression code_block
	| KW_FOR NAME KW_IN expression code_block;

while_stmt: KW_WHILE expression code_block;

ctrl_stmt: KW_CONTINUE | KW_BREAK | KW_SKIP;

report_action: KW_REPORT expression SEMI;

walker_action:
	ignore_action
	| take_action
	| destroy_action
	| KW_DISENGAGE SEMI;

ignore_action: KW_IGNORE expression SEMI;

take_action: KW_TAKE expression (SEMI | else_stmt);

destroy_action: KW_DESTROY expression SEMI;

expression: assignment | connect;

assignment:
	dotted_name index* EQ expression
	| inc_assign
	| copy_assign;

inc_assign:
	dotted_name index* (PEQ | MEQ | TEQ | DEQ) expression;

copy_assign: dotted_name index* CPY_EQ expression;

connect: logical ( (NOT)? edge_ref expression)?;

logical: compare ((KW_AND | KW_OR) compare)*;

compare:
	NOT compare
	| arithmetic (
		(EE | LT | GT | LTE | GTE | NE | KW_IN | nin) arithmetic
	)*;

nin: NOT KW_IN;

arithmetic: term ((PLUS | MINUS) term)*;

term: factor ((MUL | DIV | MOD) factor)*;

factor: (PLUS | MINUS) factor | power;

power: func_call (POW factor)* | func_call index+;

func_call:
	atom (LPAREN (expression (COMMA expression)*)? RPAREN)?
	| atom DOT func_built_in
	| atom? DBL_COLON NAME;

func_built_in:
	| KW_LENGTH
	| KW_KEYS
	| KW_EDGE
	| KW_NODE
	| KW_DESTROY LPAREN expression RPAREN;

atom:
	INT
	| FLOAT
	| STRING
	| BOOL
	| node_edge_ref
	| list_val
	| dict_val
	| dotted_name
	| LPAREN expression RPAREN
	| spawn
	| DEREF expression;

node_edge_ref: node_ref | edge_ref (node_ref)?;

node_ref: KW_NODE DBL_COLON NAME;

walker_ref: KW_WALKER DBL_COLON NAME;

graph_ref: KW_GRAPH DBL_COLON NAME;

edge_ref: edge_to | edge_from | edge_any;

edge_to: '-->' | '-' ('[' NAME ']')? '->';

edge_from: '<--' | '<-' ('[' NAME ']')? '-';

edge_any: '<-->' | '<-' ('[' NAME ']')? '->';

list_val: LSQUARE (expression (COMMA expression)*)? RSQUARE;

index: LSQUARE expression RSQUARE;

dict_val: LBRACE (kv_pair (COMMA kv_pair)*)? RBRACE;

kv_pair: STRING COLON expression;

spawn: KW_SPAWN expression? spawn_object;

spawn_object: node_spawn | walker_spawn | graph_spawn;

node_spawn: edge_ref? node_ref spawn_ctx?;

graph_spawn: edge_ref graph_ref;

walker_spawn: walker_ref spawn_ctx?;

spawn_ctx: LPAREN (assignment (COMMA assignment)*)? RPAREN;

/* DOT grammar below */
dot_graph:
	KW_STRICT? (KW_GRAPH | KW_DIGRAPH) dot_id? '{' dot_stmt_list '}';

dot_stmt_list: ( dot_stmt ';'?)*;

dot_stmt:
	dot_node_stmt
	| dot_edge_stmt
	| dot_attr_stmt
	| dot_id '=' dot_id
	| dot_subgraph;

dot_attr_stmt: ( KW_GRAPH | KW_NODE | KW_EDGE) dot_attr_list;

dot_attr_list: ( '[' dot_a_list? ']')+;

dot_a_list: ( dot_id ( '=' dot_id)? ','?)+;

dot_edge_stmt: (dot_node_id | dot_subgraph) dot_edgeRHS dot_attr_list?;

dot_edgeRHS: ( dot_edgeop ( dot_node_id | dot_subgraph))+;

dot_edgeop: '->' | '--';

dot_node_stmt: dot_node_id dot_attr_list?;

dot_node_id: dot_id dot_port?;

dot_port: ':' dot_id ( ':' dot_id)?;

dot_subgraph: ( KW_SUBGRAPH dot_id?)? '{' dot_stmt_list '}';

dot_id:
	NAME
	| STRING
	| INT
	| FLOAT
	| KW_GRAPH
	| KW_NODE
	| KW_EDGE;

/* Lexer rules */
KW_GRAPH: 'graph';
KW_STRICT: 'strict';
KW_DIGRAPH: 'digraph';
KW_SUBGRAPH: 'subgraph';
KW_NODE: 'node';
KW_IGNORE: 'ignore';
KW_TAKE: 'take';
KW_SPAWN: 'spawn';
KW_WITH: 'with';
KW_ENTRY: 'entry';
KW_EXIT: 'exit';
KW_LENGTH: 'length';
KW_KEYS: 'keys';
KW_ACTIVITY: 'activity';
COLON: ':';
DBL_COLON: '::';
COLON_OUT: '::>';
LBRACE: '{';
RBRACE: '}';
KW_EDGE: 'edge';
KW_WALKER: 'walker';
SEMI: ';';
EQ: '=';
PEQ: '+=';
MEQ: '-=';
TEQ: '*=';
DEQ: '/=';
CPY_EQ: ':=';
KW_AND: 'and' | '&&';
KW_OR: 'or' | '||';
KW_IF: 'if';
KW_ELIF: 'elif';
KW_ELSE: 'else';
KW_FOR: 'for';
KW_TO: 'to';
KW_BY: 'by';
KW_WHILE: 'while';
KW_CONTINUE: 'continue';
KW_BREAK: 'break';
KW_DISENGAGE: 'disengage';
KW_SKIP: 'skip';
KW_REPORT: 'report';
KW_DESTROY: 'destroy';
DEREF: '&';
DOT: '.';
NOT: '!' | 'not';
EE: '==';
LT: '<';
GT: '>';
LTE: '<=';
GTE: '>=';
NE: '!=';
KW_IN: 'in';
KW_ANCHOR: 'anchor';
KW_HAS: 'has';
KW_PRIVATE: 'private';
COMMA: ',';
KW_CAN: 'can';
PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';
POW: '^';
LPAREN: '(';
RPAREN: ')';
LSQUARE: '[';
RSQUARE: ']';
FLOAT: ([0-9]+)? '.' [0-9]+;
STRING: '"' ~ ["\r\n]* '"' | '\'' ~ ['\r\n]* '\'';
BOOL: 'true' | 'false';
INT: [0-9]+;
NAME: [a-zA-Z_] [a-zA-Z0-9_]*;
COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
PY_COMMENT: '#' ~[\r\n]* -> skip;
WS: [ \t\r\n] -> skip;
ErrorChar: .;
