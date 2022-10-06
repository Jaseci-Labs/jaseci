class PassAstPreProc:
    _ast_head_map = {}

    def __init__(self, ast):
        PassAstPreProc._ast_head_map[ast.mod_name] = ast
