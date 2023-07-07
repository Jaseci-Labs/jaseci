# Language Syntax Specification

```
S' -> module
module -> DOC_STRING element_list
module -> DOC_STRING
element_list -> element_list element
element_list -> element
element -> ability
element -> architype
element -> include_stmt
element -> import_stmt
element -> mod_code
element -> test
element -> global_var
```
```
global_var -> doc_tag KW_FREEZE access_tag assignment_list SEMI
global_var -> doc_tag KW_GLOBAL access_tag assignment_list SEMI
access -> KW_PROT
access -> KW_PUB
access -> KW_PRIV
access_tag -> empty
access_tag -> COLON access
```
```
test -> doc_tag KW_TEST NAME multistring code_block
```
```
mod_code -> doc_tag KW_WITH KW_ENTRY code_block
```
```
doc_tag -> DOC_STRING
doc_tag -> empty
```
```
import_stmt -> KW_IMPORT sub_name KW_FROM import_path COMMA name_as_list SEMI
import_stmt -> KW_IMPORT sub_name import_path KW_AS NAME SEMI
import_stmt -> KW_IMPORT sub_name import_path SEMI
include_stmt -> KW_INCLUDE sub_name import_path SEMI
import_path -> import_path_prefix import_path_tail
import_path -> import_path_prefix
import_path_prefix -> DOT DOT NAME
import_path_prefix -> DOT NAME
import_path_prefix -> NAME
import_path_tail -> import_path_tail DOT NAME
import_path_tail -> DOT NAME
name_as_list -> name_as_list COMMA NAME KW_AS NAME
name_as_list -> name_as_list COMMA NAME
name_as_list -> NAME KW_AS NAME
name_as_list -> NAME
```
```
architype -> architype_def
architype -> architype_decl
architype_decl -> doc_tag decorators arch_type access_tag NAME inherited_archs member_block
architype_decl -> doc_tag arch_type access_tag NAME inherited_archs member_block
architype_decl -> doc_tag decorators arch_type access_tag NAME inherited_archs SEMI
architype_decl -> doc_tag arch_type access_tag NAME inherited_archs SEMI
```
```
architype_def -> doc_tag dotted_name strict_arch_ref member_block
architype_def -> doc_tag strict_arch_ref member_block
```
```
arch_type -> KW_WALKER
arch_type -> KW_OBJECT
arch_type -> KW_EDGE
arch_type -> KW_NODE
```
```
decorators -> decorators DECOR_OP atom
decorators -> DECOR_OP atom
inherited_archs -> inherited_archs sub_name_dotted
inherited_archs -> empty
sub_name -> COLON NAME
sub_name_dotted -> COLON dotted_name
dotted_name -> dotted_name DOT NAME
dotted_name -> dotted_name DOT all_refs
dotted_name -> NAME
dotted_name -> all_refs
all_refs -> global_ref
all_refs -> visitor_ref
all_refs -> here_ref
all_refs -> arch_ref
```
```
ability -> ability_def
ability -> KW_ASYNC ability_decl
ability -> ability_decl
ability_decl -> ability_decl_decor
ability_decl -> doc_tag KW_CAN access_tag NAME func_decl code_block
ability_decl -> doc_tag KW_CAN access_tag NAME event_clause code_block
ability_decl -> doc_tag KW_CAN access_tag NAME func_decl SEMI
ability_decl -> doc_tag KW_CAN access_tag NAME event_clause SEMI
ability_decl_decor -> doc_tag decorators KW_CAN access_tag NAME func_decl code_block
ability_decl_decor -> doc_tag decorators KW_CAN access_tag NAME event_clause code_block
ability_decl_decor -> doc_tag decorators KW_CAN access_tag NAME func_decl SEMI
ability_decl_decor -> doc_tag decorators KW_CAN access_tag NAME event_clause SEMI
```
```
ability_def -> doc_tag dotted_name ability_ref func_decl code_block
ability_def -> doc_tag ability_ref func_decl code_block
ability_def -> doc_tag dotted_name ability_ref event_clause code_block
ability_def -> doc_tag ability_ref event_clause code_block
```
```
event_clause -> KW_WITH name_list KW_EXIT return_type_tag
event_clause -> KW_WITH name_list KW_ENTRY return_type_tag
event_clause -> KW_WITH STAR_MUL KW_EXIT return_type_tag
event_clause -> KW_WITH STAR_MUL KW_ENTRY return_type_tag
event_clause -> KW_WITH KW_EXIT return_type_tag
event_clause -> KW_WITH KW_ENTRY return_type_tag
event_clause -> return_type_tag
```
```
name_list -> name_list COMMA dotted_name
name_list -> dotted_name
```
```
func_decl -> LPAREN func_decl_param_list RPAREN return_type_tag
func_decl -> LPAREN RPAREN return_type_tag
func_decl_param_list -> func_decl_param_list COMMA param_var
func_decl_param_list -> param_var
param_var -> STAR_POW NAME type_tag EQ expression
param_var -> STAR_POW NAME type_tag
param_var -> STAR_MUL NAME type_tag EQ expression
param_var -> STAR_MUL NAME type_tag
param_var -> NAME type_tag EQ expression
param_var -> NAME type_tag
```
```
member_block -> LBRACE member_stmt_list RBRACE
member_block -> LBRACE RBRACE
member_stmt_list -> member_stmt_list member_stmt
member_stmt_list -> member_stmt
member_stmt -> ability
member_stmt -> has_stmt
```
```
has_stmt -> doc_tag static_tag KW_FREEZE access_tag has_assign_clause SEMI
has_stmt -> doc_tag static_tag KW_HAS access_tag has_assign_clause SEMI
static_tag -> KW_STATIC
static_tag -> empty
```
```
has_assign_clause -> has_assign_clause COMMA typed_has_clause
has_assign_clause -> typed_has_clause
typed_has_clause -> NAME type_tag EQ expression
typed_has_clause -> NAME type_tag
type_tag -> COLON type_name
return_type_tag -> RETURN_HINT type_name
return_type_tag -> empty
```
```
type_name -> type_name NULL_OK
type_name -> TYP_DICT LSQUARE type_name COMMA type_name RSQUARE
type_name -> TYP_LIST LSQUARE type_name RSQUARE
type_name -> dotted_name
type_name -> NULL
type_name -> builtin_type
```
```
builtin_type -> TYP_TYPE
builtin_type -> TYP_ANY
builtin_type -> TYP_BOOL
builtin_type -> TYP_DICT
builtin_type -> TYP_SET
builtin_type -> TYP_TUPLE
builtin_type -> TYP_LIST
builtin_type -> TYP_FLOAT
builtin_type -> TYP_INT
builtin_type -> TYP_BYTES
builtin_type -> TYP_STRING
```
```
code_block -> LBRACE statement_list RBRACE
code_block -> LBRACE RBRACE
```
```
statement_list -> statement
statement_list -> statement_list statement
statement -> walker_stmt
statement -> await_stmt SEMI
statement -> yield_stmt SEMI
statement -> return_stmt SEMI
statement -> report_stmt SEMI
statement -> delete_stmt SEMI
statement -> ctrl_stmt SEMI
statement -> assert_stmt SEMI
statement -> raise_stmt SEMI
statement -> with_stmt
statement -> while_stmt
statement -> for_stmt
statement -> try_stmt
statement -> if_stmt
statement -> expression SEMI
statement -> static_assignment
statement -> assignment SEMI
statement -> ability_decl
statement -> architype_decl
```
```
if_stmt -> KW_IF expression code_block elif_list else_stmt
if_stmt -> KW_IF expression code_block elif_list
if_stmt -> KW_IF expression code_block else_stmt
if_stmt -> KW_IF expression code_block
elif_list -> elif_list KW_ELIF expression code_block
elif_list -> KW_ELIF expression code_block
else_stmt -> KW_ELSE code_block
```
```
try_stmt -> KW_TRY code_block except_list finally_stmt
try_stmt -> KW_TRY code_block finally_stmt
try_stmt -> KW_TRY code_block except_list
try_stmt -> KW_TRY code_block
except_list -> except_list except_def
except_list -> except_def
except_def -> KW_EXCEPT expression KW_AS NAME code_block
except_def -> KW_EXCEPT expression code_block
finally_stmt -> KW_FINALLY code_block
```
```
for_stmt -> KW_FOR NAME COMMA NAME KW_IN expression code_block
for_stmt -> KW_FOR NAME KW_IN expression code_block
for_stmt -> KW_FOR assignment KW_TO expression KW_BY expression code_block
```
```
while_stmt -> KW_WHILE expression code_block
```
```
with_stmt -> KW_WITH expr_as_list code_block
expr_as_list -> expr_as_list COMMA expression KW_AS NAME
expr_as_list -> expr_as_list COMMA NAME
expr_as_list -> expression KW_AS NAME
expr_as_list -> expression
```
```
raise_stmt -> KW_RAISE expression
raise_stmt -> KW_RAISE
```
```
assert_stmt -> KW_ASSERT expression COMMA expression
assert_stmt -> KW_ASSERT expression
```
```
ctrl_stmt -> KW_SKIP
ctrl_stmt -> KW_BREAK
ctrl_stmt -> KW_CONTINUE
```
```
delete_stmt -> KW_DELETE expression
```
```
report_stmt -> KW_REPORT expression
```
```
return_stmt -> KW_RETURN expression
return_stmt -> KW_RETURN
```
```
yield_stmt -> KW_YIELD expression
yield_stmt -> KW_YIELD
```
```
walker_stmt -> disengage_stmt SEMI
walker_stmt -> revisit_stmt
walker_stmt -> visit_stmt
walker_stmt -> ignore_stmt SEMI
```
```
ignore_stmt -> KW_IGNORE expression
```
```
visit_stmt -> KW_VISIT sub_name_dotted expression else_stmt
visit_stmt -> KW_VISIT expression else_stmt
visit_stmt -> KW_VISIT sub_name_dotted expression SEMI
visit_stmt -> KW_VISIT expression SEMI
```
```
revisit_stmt -> KW_REVISIT expression else_stmt
revisit_stmt -> KW_REVISIT else_stmt
revisit_stmt -> KW_REVISIT expression SEMI
revisit_stmt -> KW_REVISIT SEMI
```
```
disengage_stmt -> KW_DISENGAGE
```
```
await_stmt -> KW_AWAIT expression
```
```
assignment -> KW_FREEZE atom EQ expression
assignment -> atom EQ expression
```
```
static_assignment -> KW_HAS assignment_list SEMI
```
```
expression -> pipe KW_IF expression KW_ELSE expression
expression -> pipe
```
```
pipe -> spawn_ctx PIPE_FWD pipe
pipe -> pipe_back PIPE_FWD spawn_ctx
pipe -> pipe_back PIPE_FWD filter_ctx
pipe -> pipe_back PIPE_FWD pipe
pipe -> pipe_back
```
```
pipe_back -> spawn_ctx PIPE_BKWD pipe_back
pipe_back -> elvis_check PIPE_BKWD spawn_ctx
pipe_back -> elvis_check PIPE_BKWD filter_ctx
pipe_back -> elvis_check PIPE_BKWD pipe_back
pipe_back -> elvis_check
```
```
elvis_check -> bitwise_or ELVIS_OP elvis_check
elvis_check -> bitwise_or
```
```
bitwise_or -> bitwise_xor BW_OR bitwise_or
bitwise_or -> bitwise_xor
bitwise_xor -> bitwise_and BW_XOR bitwise_xor
bitwise_xor -> bitwise_and
bitwise_and -> shift BW_AND bitwise_and
bitwise_and -> shift
```
```
shift -> logical RSHIFT shift
shift -> logical LSHIFT shift
shift -> logical
```
```
logical -> NOT logical
logical -> compare KW_OR logical
logical -> compare KW_AND logical
logical -> compare
```
```
compare -> arithmetic cmp_op compare
compare -> arithmetic
```
```
arithmetic -> term MINUS arithmetic
arithmetic -> term PLUS arithmetic
arithmetic -> term
```
```
term -> factor MOD term
term -> factor DIV term
term -> factor FLOOR_DIV term
term -> factor STAR_MUL term
term -> factor
```
```
factor -> power
factor -> BW_NOT factor
factor -> MINUS factor
factor -> PLUS factor
```
```
power -> connect STAR_POW power
power -> connect
```
```
connect -> spawn_object
connect -> spawn_object connect_op connect
connect -> spawn_object disconnect_op connect
```
```
spawn_object -> unpack
spawn_object -> spawn_op atom
```
```
unpack -> ref
unpack -> STAR_MUL atom
unpack -> STAR_POW atom
```
```
ref -> ds_call
ref -> BW_AND ds_call
```
```
ds_call -> walrus_assign
ds_call -> PIPE_FWD walrus_assign
```
```
walrus_assign -> atom walrus_op walrus_assign
walrus_assign -> atom
walrus_op -> RSHIFT_EQ
walrus_op -> LSHIFT_EQ
walrus_op -> BW_NOT_EQ
walrus_op -> BW_XOR_EQ
walrus_op -> BW_OR_EQ
walrus_op -> BW_AND_EQ
walrus_op -> MOD_EQ
walrus_op -> DIV_EQ
walrus_op -> FLOOR_DIV_EQ
walrus_op -> MUL_EQ
walrus_op -> SUB_EQ
walrus_op -> ADD_EQ
walrus_op -> WALRUS_EQ
```
```
cmp_op -> KW_ISN
cmp_op -> KW_IS
cmp_op -> KW_NIN
cmp_op -> KW_IN
cmp_op -> NE
cmp_op -> GTE
cmp_op -> LTE
cmp_op -> GT
cmp_op -> LT
cmp_op -> EE
```
```
spawn_op -> SPAWN_OP
spawn_op -> KW_SPAWN
```
```
atom -> edge_op_ref
atom -> all_refs
atom -> atomic_chain
atom -> LPAREN expression RPAREN
atom -> atom_collection
atom -> atom_literal
```
```
atom_literal -> builtin_type
atom_literal -> NAME
atom_literal -> NULL
atom_literal -> BOOL
atom_literal -> multistring
atom_literal -> FLOAT
atom_literal -> OCT
atom_literal -> BIN
atom_literal -> HEX
atom_literal -> INT
```
```
atom_collection -> dict_compr
atom_collection -> list_compr
atom_collection -> dict_val
atom_collection -> list_val
```
```
multistring -> FSTRING multistring
multistring -> STRING multistring
multistring -> FSTRING
multistring -> STRING
```
```
list_val -> LSQUARE expr_list RSQUARE
list_val -> LSQUARE RSQUARE
```
```
expr_list -> expr_list COMMA expression
expr_list -> expression
```
```
dict_val -> LBRACE kv_pairs RBRACE
dict_val -> LBRACE RBRACE
```
```
list_compr -> LSQUARE expression KW_FOR NAME KW_IN walrus_assign KW_IF expression RSQUARE
list_compr -> LSQUARE expression KW_FOR NAME KW_IN walrus_assign RSQUARE
```
```
dict_compr -> LBRACE expression COLON expression KW_FOR NAME COMMA NAME KW_IN walrus_assign KW_IF expression RBRACE
dict_compr -> LBRACE expression COLON expression KW_FOR NAME COMMA NAME KW_IN walrus_assign RBRACE
dict_compr -> LBRACE expression COLON expression KW_FOR NAME KW_IN walrus_assign KW_IF expression RBRACE
dict_compr -> LBRACE expression COLON expression KW_FOR NAME KW_IN walrus_assign RBRACE
```
```
kv_pairs -> kv_pairs COMMA expression COLON expression
kv_pairs -> expression COLON expression
```
```
atomic_chain -> atomic_call
atomic_chain -> atomic_chain_unsafe
atomic_chain -> atomic_chain_safe
atomic_chain_unsafe -> atom arch_ref
atomic_chain_unsafe -> atom index_slice
atomic_chain_unsafe -> atom DOT NAME
atomic_chain_safe -> atom NULL_OK arch_ref
atomic_chain_safe -> atom NULL_OK index_slice
atomic_chain_safe -> atom NULL_OK DOT NAME
```
```
atomic_call -> atom func_call_tail
func_call_tail -> LPAREN param_list RPAREN
func_call_tail -> LPAREN RPAREN
param_list -> expr_list COMMA assignment_list
param_list -> assignment_list
param_list -> expr_list
```
```
assignment_list -> assignment_list COMMA assignment
assignment_list -> assignment
```
```
index_slice -> LSQUARE COLON expression RSQUARE
index_slice -> LSQUARE expression COLON RSQUARE
index_slice -> LSQUARE expression COLON expression RSQUARE
index_slice -> LSQUARE expression RSQUARE
```
```
global_ref -> GLOBAL_OP NAME
here_ref -> HERE_OP
visitor_ref -> VISITOR_OP
arch_ref -> ability_ref
arch_ref -> object_ref
arch_ref -> walker_ref
arch_ref -> edge_ref
arch_ref -> node_ref
```
```
strict_arch_ref -> object_ref
strict_arch_ref -> walker_ref
strict_arch_ref -> edge_ref
strict_arch_ref -> node_ref
```
```
node_ref -> NODE_OP NAME
edge_ref -> EDGE_OP NAME
walker_ref -> WALKER_OP NAME
object_ref -> OBJECT_OP NAME
ability_ref -> ABILITY_OP NAME
```
```
edge_op_ref -> edge_any
edge_op_ref -> edge_from
edge_op_ref -> edge_to
edge_to -> ARROW_R_p1 expression ARROW_R_p2
edge_to -> ARROW_R
edge_from -> ARROW_L_p1 expression ARROW_L_p2
edge_from -> ARROW_L
edge_any -> ARROW_L_p1 expression ARROW_R_p2
edge_any -> ARROW_BI
```
```
connect_op -> connect_any
connect_op -> connect_from
connect_op -> connect_to
disconnect_op -> NOT edge_op_ref
connect_to -> CARROW_R_p1 expression CARROW_R_p2
connect_to -> CARROW_R
connect_from -> CARROW_L_p1 expression CARROW_L_p2
connect_from -> CARROW_L
connect_any -> CARROW_L_p1 expression CARROW_R_p2
connect_any -> CARROW_BI
```
```
filter_ctx -> LBRACE EQ filter_compare_list RBRACE
```
```
spawn_ctx -> LBRACE param_list RBRACE
```
```
filter_compare_list -> filter_compare_list COMMA NAME cmp_op expression
filter_compare_list -> NAME cmp_op expression
empty -> <empty>
```
