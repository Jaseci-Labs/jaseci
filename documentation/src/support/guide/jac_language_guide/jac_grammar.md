# JAC Grammar



    program     : element*



    element     : architype

                : walker



    architype   : KW:NODE (COLON INT)? ID LBRACE attr_stmts RBRACE

                : KW:EDGE ID LBRACE attr_stmts RBRACE



    walker      : KW:WALKER ID code_block



    statements  : statement*



    statement   : architype

                : walker

                : code_block

                : node_code

                : expression SEMI

                : if_stmt

                : for_stmt

                : while_stmt



    code_block  : LBRACE statements RBRACE

                : COLON statement SEMI



    node_code   : dotted_name code_block



    expression  : dotted_name EQ expression

                : compare (KW:AND|KW:OR compare)*



    if_stmt     : KW:IF expr code_block (elif_stmt)* (else_stmt)*



    for_stmt    : KW:FOR expression KW:TO experssion KY:BY expression code_block



    while_stmt  : KW:WHILE expression code_block



    attr_stmts  : attr_stmt*



    dotted_name : ID (DOT ID)*



    compare     : NOT compare

                : arithmetic ((EE|LT|GT|LTE|GTE) arithmetic)*



    attr_stmt   : KW:HAS ID (, ID)* SEMI

                : KW:CAN dotted_name (, dotted_name)* SEMI

                : arch_set SEMI



    arch_set    : KW:NAME EQ expression

                : KW:KIND EQ expression



    arithmetic  : term ((PLUS|MINUS) term)*



    term        : factor ((MUL|DIV) factor)*



    factor      : (PLUS|MINUS) factor

                : power



    power       : func_call (POW factor)*



    func_call   : atom (LPAREN (expression (COMMA expression)*)? RPAREN)?



    atom        : INT|FLOAT|STRING

                : dotted_name (LSQUARE expression RSQUARE)*

                : LPAREN expr RPAREN

                : list
