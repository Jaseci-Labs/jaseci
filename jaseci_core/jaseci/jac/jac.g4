grammar jac;

start: ver_label? import_module* element+ EOF;

import_module:
	KW_IMPORT LBRACE (import_items | STAR_MUL) RBRACE KW_WITH STRING SEMI;

ver_label: 'version' COLON STRING SEMI?;

import_items:
	KW_WALKER (STAR_MUL | import_names) (COMMA import_items)?
	| KW_NODE (STAR_MUL | import_names) (COMMA import_items)?
	| KW_EDGE (STAR_MUL | import_names) (COMMA import_items)?
	| KW_GRAPH (STAR_MUL | import_names) (COMMA import_items)?;

import_names:
	DBL_COLON NAME
	| DBL_COLON LBRACE name_list RBRACE;

element: architype | walker | test;

architype:
	KW_NODE NAME (COLON INT)? attr_block
	| KW_EDGE NAME attr_block
	| KW_GRAPH NAME graph_block;

walker:
	KW_WALKER NAME namespaces? LBRACE attr_stmt* walk_entry_block? (
		statement
		| walk_activity_block
	)* walk_exit_block? RBRACE;

test: KW_TEST graph_ref walker_ref | KW_TEST graph_ref walker;

namespaces: COLON name_list;

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

has_stmt:
	KW_HAS KW_PRIVATE? KW_ANCHOR? has_assign (COMMA has_assign)* SEMI;

has_assign: NAME | NAME EQ expression;

can_stmt:
	KW_CAN dotted_name (preset_in_out event_clause)? (
		COMMA dotted_name (preset_in_out event_clause)?
	)* SEMI
	| KW_CAN NAME event_clause? code_block;

event_clause:
	KW_WITH name_list? (KW_ENTRY | KW_EXIT | KW_ACTIVITY);

preset_in_out:
	DBL_COLON expr_list? (DBL_COLON | COLON_OUT expression);

dotted_name: NAME DOT NAME;

name_list: NAME (COMMA NAME)*;

expr_list: expression (COMMA expression)*;

code_block: LBRACE statement* RBRACE | COLON statement;

node_ctx_block: name_list code_block;

statement:
	code_block
	| node_ctx_block
	| expression SEMI
	| if_stmt
	| try_stmt
	| for_stmt
	| while_stmt
	| assert_stmt SEMI
	| ctrl_stmt SEMI
	| destroy_action
	| report_action
	| walker_action;

if_stmt: KW_IF expression code_block elif_stmt* else_stmt?;

try_stmt: KW_TRY code_block else_from_try?;

else_from_try:
	KW_ELSE (LPAREN NAME RPAREN)? code_block
	| KW_ELSE (KW_WITH NAME)? code_block;

elif_stmt: KW_ELIF expression code_block;

else_stmt: KW_ELSE code_block;

for_stmt:
	KW_FOR expression KW_TO expression KW_BY expression code_block
	| KW_FOR NAME KW_IN expression code_block;

while_stmt: KW_WHILE expression code_block;

ctrl_stmt: KW_CONTINUE | KW_BREAK | KW_SKIP;

assert_stmt: KW_ASSERT expression;

destroy_action: KW_DESTROY expression SEMI;

report_action: KW_REPORT expression SEMI;

walker_action: ignore_action | take_action | KW_DISENGAGE SEMI;

ignore_action: KW_IGNORE expression SEMI;

take_action: KW_TAKE expression (SEMI | else_stmt);

expression: connect (assignment | copy_assign | inc_assign)?;

assignment: EQ expression;

copy_assign: CPY_EQ expression;

inc_assign: (PEQ | MEQ | TEQ | DEQ) expression;

connect: logical ( (NOT)? edge_ref expression)?;

logical: compare ((KW_AND | KW_OR) compare)*;

compare: NOT compare | arithmetic (cmp_op arithmetic)*;

cmp_op: EE | LT | GT | LTE | GTE | NE | KW_IN | nin;

nin: NOT KW_IN;

arithmetic: term ((PLUS | MINUS) term)*;

term: factor ((STAR_MUL | DIV | MOD) factor)*;

factor: (PLUS | MINUS) factor | power;

power: func_call (POW factor)*;

func_call:
	atom (LPAREN expr_list? RPAREN)?
	| atom? DBL_COLON NAME spawn_ctx?;

atom:
	INT
	| FLOAT
	| STRING
	| BOOL
	| NULL
	| NAME
	| node_edge_ref
	| list_val
	| dict_val
	| LPAREN expression RPAREN
	| spawn
	| atom DOT built_in
	| atom DOT NAME
	| atom index_slice
	| ref
	| deref
	| any_type;

ref: '&' expression;

deref: STAR_MUL expression;

built_in:
	cast_built_in
	| obj_built_in
	| dict_built_in
	| list_built_in
	| string_built_in;

cast_built_in: any_type;

obj_built_in: KW_CONTEXT | KW_INFO | KW_DETAILS;

dict_built_in: KW_KEYS | LBRACE name_list RBRACE;

list_built_in: KW_LENGTH;

string_built_in:
	TYP_STRING DBL_COLON NAME (LPAREN expr_list RPAREN)?;

node_edge_ref:
	node_ref filter_ctx?
	| edge_ref (node_ref filter_ctx?)?;

node_ref: KW_NODE DBL_COLON NAME;

walker_ref: KW_WALKER DBL_COLON NAME;

graph_ref: KW_GRAPH DBL_COLON NAME;

edge_ref: edge_to | edge_from | edge_any;

edge_to:
	'-->'
	| '-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '->';

edge_from:
	'<--'
	| '<-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '-';

edge_any:
	'<-->'
	| '<-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '->';

list_val: LSQUARE expr_list? RSQUARE;

index_slice:
	LSQUARE expression RSQUARE
	| LSQUARE expression COLON expression RSQUARE;

dict_val: LBRACE (kv_pair (COMMA kv_pair)*)? RBRACE;

kv_pair: STRING COLON expression;

spawn: KW_SPAWN expression? spawn_object;

spawn_object: node_spawn | walker_spawn | graph_spawn;

node_spawn: edge_ref? node_ref spawn_ctx?;

graph_spawn: edge_ref graph_ref;

walker_spawn: walker_ref spawn_ctx?;

spawn_ctx: LPAREN (spawn_assign (COMMA spawn_assign)*)? RPAREN;

filter_ctx:
	LPAREN (filter_compare (COMMA filter_compare)*)? RPAREN;

spawn_assign: NAME EQ expression;

filter_compare: NAME cmp_op expression;

any_type:
	TYP_STRING
	| TYP_INT
	| TYP_FLOAT
	| TYP_LIST
	| TYP_DICT
	| TYP_BOOL
	| KW_NODE
	| KW_EDGE
	| KW_TYPE;

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
TYP_STRING: 'str';
TYP_INT: 'int';
TYP_FLOAT: 'float';
TYP_LIST: 'list';
TYP_DICT: 'dict';
TYP_BOOL: 'bool';
KW_TYPE: 'type';
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
KW_CONTEXT: 'context';
KW_INFO: 'info';
KW_DETAILS: 'details';
KW_ACTIVITY: 'activity';
KW_IMPORT: 'import';
COLON: ':';
DBL_COLON: '::';
COLON_OUT: '::>';
LBRACE: '{';
RBRACE: '}';
KW_EDGE: 'edge';
KW_WALKER: 'walker';
KW_TEST: 'test';
KW_ASSERT: 'assert';
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
KW_TRY: 'try';
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
STAR_MUL: '*';
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
NULL: 'null';
NAME: [a-zA-Z_] [a-zA-Z0-9_]*;
COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
PY_COMMENT: '#' ~[\r\n]* -> skip;
WS: [ \t\r\n] -> skip;
ErrorChar: .;
