grammar jac;

start: ver_label? import_module* element* EOF;

ver_label: 'version' COLON STRING SEMI?;

import_module:
	KW_IMPORT LBRACE (import_items | STAR_MUL) RBRACE KW_WITH STRING SEMI;

import_items:
	WALKER_DBL_COLON (STAR_MUL | import_names) (
		COMMA import_items
	)?
	| NODE_DBL_COLON (STAR_MUL | import_names) (
		COMMA import_items
	)?
	| EDGE_DBL_COLON (STAR_MUL | import_names) (
		COMMA import_items
	)?
	| GRAPH_DBL_COLON (STAR_MUL | import_names) (
		COMMA import_items
	)?
	| KW_GLOBAL DBL_COLON (STAR_MUL | import_names) (
		COMMA import_items
	)?
	| TYPE_DBL_COLON (STAR_MUL | import_names) (
		COMMA import_items
	)?;

import_names: NAME | LBRACE name_list RBRACE;

element: global_var | architype | test;

global_var:
	KW_GLOBAL NAME EQ expression (COMMA NAME EQ expression)* SEMI;

architype:
	KW_NODE NAME (COLON NAME)* attr_block
	| KW_EDGE NAME (COLON NAME)* attr_block
	| KW_TYPE NAME struct_block
	| KW_GRAPH NAME graph_block
	| KW_ASYNC? KW_WALKER NAME namespaces? walker_block;

walker_block:
	LBRACE attr_stmt* walk_entry_block? (
		statement
		| walk_activity_block
	)* walk_exit_block? RBRACE;

test:
	KW_TEST NAME? multistring KW_WITH (
		graph_ref
		| KW_GRAPH graph_block
	) KW_BY (
		(walker_ref spawn_ctx? (code_block | SEMI))
		| KW_WALKER walker_block
	);

namespaces: COLON name_list;

walk_entry_block: KW_WITH KW_ENTRY code_block;

walk_exit_block: KW_WITH KW_EXIT code_block;

walk_activity_block: KW_WITH KW_ACTIVITY code_block;

attr_block: LBRACE (attr_stmt)* RBRACE | COLON attr_stmt | SEMI;

attr_stmt: has_stmt | can_stmt;

struct_block: LBRACE (has_stmt)* RBRACE | COLON has_stmt | SEMI;

can_block: (can_stmt)*;

graph_block:
	LBRACE has_root can_block KW_SPAWN code_block RBRACE
	| COLON has_root can_block KW_SPAWN code_block SEMI;

has_root: KW_HAS KW_ANCHOR NAME SEMI;

has_stmt: KW_HAS has_assign (COMMA has_assign)* SEMI;

has_assign: KW_PRIVATE? KW_ANCHOR? (NAME | NAME EQ expression);

can_stmt:
	KW_CAN dotted_name (preset_in_out event_clause)? (
		COMMA dotted_name (preset_in_out event_clause)?
	)* SEMI
	| KW_CAN NAME event_clause? code_block;

event_clause:
	KW_WITH name_list? (KW_ENTRY | KW_EXIT | KW_ACTIVITY);

preset_in_out:
	DBL_COLON param_list? (DBL_COLON | COLON_OUT expression);

dotted_name: NAME DOT NAME;

name_list: NAME (COMMA NAME)*;

param_list:
	expr_list
	| kw_expr_list
	| expr_list COMMA kw_expr_list;

expr_list: connect (COMMA connect)*;

kw_expr_list: NAME EQ connect (COMMA NAME EQ connect)*;

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
	| KW_FOR NAME (COMMA NAME)? KW_IN expression code_block;

while_stmt: KW_WHILE expression code_block;

ctrl_stmt: KW_CONTINUE | KW_BREAK | KW_SKIP;

assert_stmt: KW_ASSERT expression;

destroy_action: KW_DESTROY expression SEMI;

report_action:
	KW_REPORT expression SEMI
	| KW_REPORT COLON NAME EQ expression SEMI;

walker_action:
	ignore_action
	| take_action
	| disengage_action
	| yield_action;

ignore_action: KW_IGNORE expression SEMI;

take_action:
	KW_TAKE (COLON NAME)? expression (SEMI | else_stmt);

disengage_action: KW_DISENGAGE (report_action | SEMI);

yield_action:
	KW_YIELD (
		report_action
		| disengage_action
		| take_action
		| SEMI
	);

expression: connect (assignment | copy_assign | inc_assign)?;

assignment: EQ expression;

copy_assign: CPY_EQ expression;

inc_assign: (PEQ | MEQ | TEQ | DEQ) expression;

connect: logical ( (NOT edge_ref | connect_op) expression)?;

logical: compare ((KW_AND | KW_OR) compare)*;

compare: NOT compare | arithmetic (cmp_op arithmetic)*;

cmp_op: EE | LT | GT | LTE | GTE | NE | KW_IN | nin;

nin: NOT KW_IN;

arithmetic: term ((PLUS | MINUS) term)*;

term: factor ((STAR_MUL | DIV | MOD) factor)*;

factor: (PLUS | MINUS) factor | power;

power: atom (POW factor)*;

global_ref: KW_GLOBAL DOT (obj_built_in | NAME);

atom:
	INT
	| FLOAT
	| multistring
	| BOOL
	| NULL
	| NAME
	| global_ref
	| node_edge_ref
	| list_val
	| dict_val
	| LPAREN expression RPAREN
	| ability_op NAME spawn_ctx?
	| atom atom_trailer
	| KW_SYNC atom
	| spawn
	| ref
	| deref
	| any_type;

atom_trailer:
	DOT built_in
	| DOT NAME
	| index_slice
	| ability_call;

ability_call:
	LPAREN param_list? RPAREN
	| ability_op NAME spawn_ctx?;

ability_op: DBL_COLON | DBL_COLON NAME COLON;

ref: KW_REF atom;

deref: STAR_MUL atom;

built_in:
	| string_built_in
	| dict_built_in
	| list_built_in
	| obj_built_in
	| cast_built_in;

cast_built_in: any_type;

obj_built_in: KW_CONTEXT | KW_INFO | KW_DETAILS;

dict_built_in:
	KW_KEYS
	| LBRACE name_list RBRACE
	| (TYP_DICT DBL_COLON | DICT_DBL_COLON) (NAME | KW_KEYS) (
		LPAREN expr_list RPAREN
	)?;

list_built_in:
	KW_LENGTH
	| (TYP_LIST DBL_COLON | LIST_DBL_COLON) NAME (
		LPAREN expr_list RPAREN
	)?;

string_built_in:
	(TYP_STRING DBL_COLON | STR_DBL_COLON) NAME (
		LPAREN expr_list RPAREN
	)?;

node_edge_ref:
	node_ref filter_ctx? node_edge_ref?
	| edge_ref node_edge_ref?;

node_ref: NODE_DBL_COLON NAME;

walker_ref: WALKER_DBL_COLON NAME;

graph_ref: GRAPH_DBL_COLON NAME;

type_ref: TYPE_DBL_COLON NAME;

edge_ref: edge_to | edge_from | edge_any;

edge_to: '-->' | '-' ('[' NAME filter_ctx? ']')? '->';

edge_from: '<--' | '<-' ('[' NAME filter_ctx? ']')? '-';

edge_any: '<-->' | '<-' ('[' NAME filter_ctx? ']')? '->';

connect_op: connect_to | connect_from | connect_any;

connect_to: '++>' | '+' ('[' NAME spawn_ctx? ']')? '+>';

connect_from: '<++' | '<+' ('[' NAME spawn_ctx? ']')? '+';

connect_any: '<++>' | '<+' ('[' NAME spawn_ctx? ']')? '+>';

list_val: LSQUARE expr_list? RSQUARE;

index_slice:
	LSQUARE expression RSQUARE
	| LSQUARE expression COLON expression RSQUARE;

dict_val: LBRACE (kv_pair (COMMA kv_pair)*)? RBRACE;

kv_pair: expression COLON expression;

spawn: KW_SPAWN spawn_object;

spawn_object:
	node_spawn
	| walker_spawn
	| graph_spawn
	| type_spawn;

spawn_edge: expression connect_op;

node_spawn: spawn_edge? node_ref spawn_ctx?;

graph_spawn: spawn_edge? graph_ref;

walker_spawn: expression KW_SYNC? walker_ref spawn_ctx?;

type_spawn: type_ref spawn_ctx?;

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

multistring: STRING+;

/* Lexer rules */
TYP_STRING: 'str';
TYP_INT: 'int';
TYP_FLOAT: 'float';
TYP_LIST: 'list';
TYP_DICT: 'dict';
TYP_BOOL: 'bool';
KW_TYPE: 'type';
KW_GRAPH: 'graph';
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
STR_DBL_COLON: 's::';
LIST_DBL_COLON: 'l::';
DICT_DBL_COLON: 'd::';
NODE_DBL_COLON: 'n::' | KW_NODE DBL_COLON;
EDGE_DBL_COLON: 'e::' | KW_EDGE DBL_COLON;
WALKER_DBL_COLON: 'w::' | KW_WALKER DBL_COLON;
GRAPH_DBL_COLON: 'g::' | KW_GRAPH DBL_COLON;
TYPE_DBL_COLON: 't::' | KW_TYPE DBL_COLON;
COLON_OUT: '::>';
LBRACE: '{';
RBRACE: '}';
KW_EDGE: 'edge';
KW_WALKER: 'walker';
KW_ASYNC: 'async';
KW_SYNC: 'sync';
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
KW_YIELD: 'yield';
KW_SKIP: 'skip';
KW_REPORT: 'report';
KW_DESTROY: 'destroy';
KW_TRY: 'try';
KW_REF: '&';
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
KW_GLOBAL: 'global';
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
