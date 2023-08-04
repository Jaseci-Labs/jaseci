"""Ast build pass for Jaseci Ast."""
from os import path

import jaclang.jac.absyntree as ast
from jaclang.jac.absyntree import replace_node
from jaclang.jac.constant import EdgeDir
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.passes import Pass


class AstBuildPass(Pass):
    """Jac Ast build pass."""

    def enter_module(self, node: ast.AstNode) -> None:
        """Grammar rule.

        module -> DOC_STRING element_list
        module -> DOC_STRING
        """
        mod_name = self.mod_path.split(path.sep)[-1].split(".")[0]
        mod = ast.Module(
            name=mod_name,
            doc=node.kid[0],
            body=node.kid[1] if len(node.kid) == 2 else None,
            mod_path=self.mod_path,
            rel_mod_path=self.rel_mod_path,
            is_imported=False,
            parent=None,
            mod_link=None,
            kid=node.kid,
            line=node.line,
        )
        mod.mod_link = mod
        self.mod_link = mod
        self.ir = replace_node(node, mod)

    def exit_module(self, node: ast.AstNode) -> None:
        """Grammar rule.

        module -> DOC_STRING element_list
        module -> DOC_STRING
        """
        if type(self.ir) == ast.Module:
            self.ir.doc = node.kid[0]
            self.ir.body = node.kid[1] if len(node.kid) == 2 else None
        else:
            self.ice("Self IR should be module!")

    def exit_element_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        element_list -> element_list element
        element_list -> element
        """
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        replace_node(
            node,
            ast.Elements(
                elements=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_element(self, node: ast.AstNode) -> None:
        """Grammar rule.

        element -> enum
        element -> ability
        element -> architype
        element -> include_stmt
        element -> import_stmt
        element -> mod_code
        element -> test
        element -> global_var
        """
        replace_node(node, node.kid[0])

    def exit_global_var(self, node: ast.AstNode) -> None:
        """Grammar rule.

        global_var -> doc_tag KW_FREEZE access_tag assignment_list SEMI
        global_var -> doc_tag KW_GLOBAL access_tag assignment_list SEMI
        """
        is_frozen = node.kid[1].name == Tok.KW_FREEZE
        node.kid = [node.kid[0], node.kid[2], node.kid[3]]
        replace_node(
            node,
            ast.GlobalVars(
                doc=node.kid[0],
                access=node.kid[1],
                assignments=node.kid[2],
                is_frozen=is_frozen,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_access(self, node: ast.AstNode) -> None:
        """Grammar rule.

        access -> KW_PROT
        access -> KW_PUB
        access -> KW_PRIV
        """
        replace_node(node, node.kid[0])

    def exit_access_tag(self, node: ast.AstNode) -> None:
        """Grammar rule.

        access_tag -> empty
        access_tag -> COLON access
        """
        replace_node(node, node.kid[-1])

    def exit_test(self, node: ast.AstNode) -> None:
        """Grammar rule.

        test -> doc_tag KW_TEST NAME multistring code_block
        """
        del node.kid[1]
        replace_node(
            node,
            ast.Test(
                doc=node.kid[0],
                name=node.kid[1],
                description=node.kid[2],
                body=node.kid[3],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_mod_code(self, node: ast.AstNode) -> None:
        """Grammar rule.

        mod_code -> doc_tag KW_WITH KW_ENTRY code_block
        """
        node.kid = [node.kid[0], node.kid[-1]]
        replace_node(
            node,
            ast.ModuleCode(
                doc=node.kid[0],
                body=node.kid[1],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_doc_tag(self, node: ast.AstNode) -> None:
        """Grammar rule.

        doc_tag -> DOC_STRING
        doc_tag -> empty
        """
        replace_node(node, node.kid[0])

    def exit_import_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        import_stmt -> KW_IMPORT sub_name KW_FROM import_path COMMA import_items SEMI
        import_stmt -> KW_IMPORT sub_name import_path KW_AS NAME SEMI
        import_stmt -> KW_IMPORT sub_name import_path SEMI
        """
        kid = node.kid
        meta = {
            "lang": kid[1],
            "path": kid[2],
            "alias": None,
            "items": None,
            "is_absorb": False,
        }
        if len(node.kid) == 7:
            meta["path"] = kid[3]
            meta["items"] = kid[5]
            node.kid = [kid[1], kid[3], kid[5]]
        elif len(node.kid) == 6:
            meta["alias"] = kid[4]
            node.kid = [kid[1], kid[2], kid[4]]
        else:
            node.kid = [kid[1], kid[2]]
        replace_node(
            node,
            ast.Import(
                lang=meta["lang"],
                path=meta["path"],
                alias=meta["alias"],
                items=meta["items"],
                is_absorb=meta["is_absorb"],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_include_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        include_stmt -> KW_INCLUDE sub_name import_path SEMI
        """
        kid = node.kid
        meta = {
            "lang": kid[1],
            "path": kid[2],
            "alias": None,
            "items": None,
            "is_absorb": True,
        }
        node.kid = [kid[1], kid[2]]
        replace_node(
            node,
            ast.Import(
                lang=meta["lang"],
                path=meta["path"],
                alias=meta["alias"],
                items=meta["items"],
                is_absorb=meta["is_absorb"],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_import_path(self, node: ast.AstNode) -> None:
        """Grammar rule.

        import_path -> import_path_prefix import_path_tail
        import_path -> import_path_prefix
        """
        if len(node.kid) == 1:
            node.kid = node.kid[0].kid
        else:
            node.kid = node.kid[0].kid + node.kid[1].kid
        replace_node(
            node,
            ast.ModulePath(
                path=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_import_path_prefix(self, node: ast.AstNode) -> None:
        """Grammar rule.

        import_path_prefix -> DOT DOT NAME
        import_path_prefix -> DOT NAME
        import_path_prefix -> NAME
        """

    def exit_import_path_tail(self, node: ast.AstNode) -> None:
        """Grammar rule.

        import_path_tail -> import_path_tail DOT NAME
        import_path_tail -> DOT NAME
        """
        if len(node.kid) > 2:
            node.kid = node.kid[0].kid + [node.kid[1], node.kid[2]]

    def exit_import_items(self, node: ast.AstNode) -> None:
        """Grammar rule.

        import_items -> import_items COMMA NAME KW_AS NAME
        import_items -> import_items COMMA NAME
        import_items -> NAME KW_AS NAME
        import_items -> NAME
        """
        this_item = None
        if type(node.kid[0]) == ast.Name:
            this_item = ast.ModuleItem(
                name=node.kid[0],
                alias=node.kid[2] if len(node.kid) == 3 else None,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=[node.kid[0], node.kid[2]] if len(node.kid) == 3 else [node.kid[0]],
                line=node.line,
            )
            node.kid = [this_item]
        else:
            this_item = ast.ModuleItem(
                name=node.kid[-3] if node.kid[-2].name == Tok.KW_AS else node.kid[-1],
                alias=node.kid[-1] if node.kid[-2].name == Tok.KW_AS else None,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=[node.kid[-3], node.kid[-1]]
                if node.kid[-2].name == Tok.KW_AS
                else [node.kid[-1]],
                line=node.line,
            )
            node.kid = node.kid[0].kid + [this_item]
        replace_node(
            node,
            ast.ModuleItems(
                items=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_architype(self, node: ast.AstNode) -> None:
        """Grammar rule.

        architype -> architype_def
        architype -> architype_decl
        architype -> architype_inline_spec
        """
        replace_node(node, node.kid[0])

    def exit_architype_decl(self, node: ast.AstNode) -> None:
        """Grammar rule.

        architype_decl -> doc_tag decorators arch_type access_tag NAME inherited_archs member_block
        architype_decl -> doc_tag arch_type access_tag NAME inherited_archs member_block
        architype_decl -> doc_tag decorators arch_type access_tag NAME inherited_archs SEMI
        architype_decl -> doc_tag arch_type access_tag NAME inherited_archs SEMI
        """
        replace_node(
            node,
            ast.Architype(
                doc=node.kid[0],
                decorators=node.kid[1] if len(node.kid) == 7 else None,
                arch_type=node.kid[2] if len(node.kid) == 7 else node.kid[1],
                access=node.kid[3] if len(node.kid) == 7 else node.kid[2],
                name=node.kid[4] if len(node.kid) == 7 else node.kid[3],
                base_classes=node.kid[5] if len(node.kid) == 7 else node.kid[4],
                body=node.kid[-1] if type(node.kid[-1]) == ast.ArchBlock else None,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )
        if type(node.kid[-1]) == ast.Token:
            del node.kid[-1]

    def exit_architype_def(self, node: ast.AstNode) -> None:
        """Grammar rule.

        architype_def -> doc_tag dotted_name strict_arch_ref member_block
        architype_def -> doc_tag strict_arch_ref member_block
        """
        replace_node(
            node,
            ast.ArchDef(
                doc=node.kid[0],
                mod=node.kid[1] if len(node.kid) == 4 else None,
                arch=node.kid[2] if len(node.kid) == 4 else node.kid[1],
                body=node.kid[-1],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_arch_type(self, node: ast.AstNode) -> None:
        """Grammar rule.

        arch_type -> KW_WALKER
        arch_type -> KW_OBJECT
        arch_type -> KW_EDGE
        arch_type -> KW_NODE
        """
        replace_node(node, node.kid[0])

    def exit_decorators(self, node: ast.AstNode) -> None:
        """Grammar rule.

        decorators -> decorators DECOR_OP atom
        decorators -> DECOR_OP atom
        """
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        else:
            node.kid = [node.kid[1]]
        replace_node(
            node,
            ast.Decorators(
                calls=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_inherited_archs(self, node: ast.AstNode) -> None:
        """Grammar rule.

        inherited_archs -> inherited_archs sub_name_dotted
        inherited_archs -> empty
        """
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        if not node.kid[0]:
            del node.kid[0]
        replace_node(
            node,
            ast.BaseClasses(
                base_classes=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_sub_name(self, node: ast.AstNode) -> None:
        """Grammar rule.

        sub_name -> COLON NAME
        """
        replace_node(node, node.kid[1])

    def exit_sub_name_dotted(self, node: ast.AstNode) -> None:
        """Grammar rule.

        sub_name_dotted -> COLON dotted_name
        """
        replace_node(node, node.kid[1])

    def exit_dotted_name(self, node: ast.AstNode) -> None:
        """Grammar rule.

        dotted_name -> dotted_name DOT all_refs
        dotted_name -> all_refs
        """
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        replace_node(
            node,
            ast.NameList(
                names=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_all_refs(self, node: ast.AstNode) -> None:
        """Grammar rule.

        all_refs -> named_refs
        all_refs -> special_refs
        """
        replace_node(node, node.kid[0])

    def exit_named_refs(self, node: ast.AstNode) -> None:
        """Grammar rule.

        named_refs -> NAME
        named_refs -> arch_ref
        """
        replace_node(node, node.kid[0])

    def exit_special_refs(self, node: ast.AstNode) -> None:
        """Grammar rule.

        special_refs -> INIT_OP
        special_refs -> ROOT_OP
        special_refs -> SUPER_OP
        special_refs -> SELF_OP
        special_refs -> HERE_OP
        """
        replace_node(
            node,
            ast.SpecialVarRef(
                var=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_ability(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ability -> ability_def
        ability -> KW_ASYNC ability_decl
        ability -> ability_decl
        """
        if len(node.kid) == 2:
            new_node = replace_node(node, node.kid[1])
            if type(new_node) == ast.Ability:
                new_node.is_async = True
        else:
            replace_node(node, node.kid[0])

    def exit_ability_decl(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ability_decl -> ability_decl_decor
        ability_decl -> doc_tag static_tag KW_CAN access_tag all_refs func_decl code_block
        ability_decl -> doc_tag static_tag KW_CAN access_tag all_refs event_clause code_block
        ability_decl -> doc_tag static_tag KW_CAN access_tag all_refs func_decl SEMI
        ability_decl -> doc_tag static_tag KW_CAN access_tag all_refs event_clause SEMI
        """
        if len(node.kid) == 1:
            replace_node(node, node.kid[0])
            return
        del node.kid[2]
        replace_node(
            node,
            ast.Ability(
                doc=node.kid[0],
                access=node.kid[2],
                is_static=node.kid[1],
                name_ref=node.kid[3],
                body=node.kid[-1] if type(node.kid[-1]) == ast.CodeBlock else None,
                signature=node.kid[-2],
                is_func=type(node.kid[-2]) == ast.FuncSignature,
                is_async=False,
                decorators=None,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )
        if type(node.kid[-1]) == ast.Token:
            del node.kid[-1]

    def exit_ability_decl_decor(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ability_decl_decor -> doc_tag decorators static_tag KW_CAN access_tag all_refs func_decl code_block
        ability_decl_decor -> doc_tag decorators static_tag KW_CAN access_tag all_refs event_clause code_block
        ability_decl_decor -> doc_tag decorators static_tag KW_CAN access_tag all_refs func_decl SEMI
        ability_decl_decor -> doc_tag decorators static_tag KW_CAN access_tag all_refs event_clause SEMI
        """
        del node.kid[3]
        replace_node(
            node,
            ast.Ability(
                doc=node.kid[0],
                decorators=node.kid[1],
                is_static=node.kid[2],
                access=node.kid[3],
                name_ref=node.kid[4],
                body=node.kid[-1] if type(node.kid[-1]) == ast.CodeBlock else None,
                signature=node.kid[-2],
                is_func=type(node.kid[-2]) == ast.FuncSignature,
                is_async=False,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )
        if type(node.kid[-1]) == ast.Token:
            del node.kid[-1]

    def exit_ability_def(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ability_def -> doc_tag dotted_name ability_ref func_decl code_block
        ability_def -> doc_tag ability_ref func_decl code_block
        ability_def -> doc_tag dotted_name ability_ref event_clause code_block
        ability_def -> doc_tag ability_ref event_clause code_block
        """
        replace_node(
            node,
            ast.AbilityDef(
                doc=node.kid[0],
                target=node.kid[1] if len(node.kid) == 5 else None,
                ability=node.kid[2] if len(node.kid) == 5 else node.kid[1],
                signature=node.kid[-2],
                body=node.kid[-1],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_event_clause(self, node: ast.AstNode) -> None:
        """Grammar rule.

        event_clause -> KW_WITH type_spec KW_EXIT return_type_tag
        event_clause -> KW_WITH type_spec KW_ENTRY return_type_tag
        event_clause -> KW_WITH KW_EXIT return_type_tag
        event_clause -> KW_WITH KW_ENTRY return_type_tag
        """
        if len(node.kid) == 3:
            node.kid = node.kid[1:]
            replace_node(
                node,
                ast.EventSignature(
                    event=node.kid[0],
                    arch_tag_info=None,
                    return_type=node.kid[-1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = node.kid[1:]
            replace_node(
                node,
                ast.EventSignature(
                    event=node.kid[1],
                    arch_tag_info=node.kid[0],
                    return_type=node.kid[-1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_func_decl(self, node: ast.AstNode) -> None:
        """Grammar rule.

        func_decl -> LPAREN func_decl_param_list RPAREN return_type_tag
        func_decl -> LPAREN RPAREN return_type_tag
        func_decl -> return_type_tag
        """
        if len(node.kid) <= 3:
            node.kid = [node.kid[-1]]
            replace_node(
                node,
                ast.FuncSignature(
                    params=None,
                    return_type=node.kid[0],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = [node.kid[1], node.kid[3]]
            replace_node(
                node,
                ast.FuncSignature(
                    params=node.kid[0],
                    return_type=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_func_decl_param_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        func_decl_param_list -> func_decl_param_list COMMA param_var
        func_decl_param_list -> param_var
        """
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        replace_node(
            node,
            ast.FuncParams(
                params=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_param_var(self, node: ast.AstNode) -> None:
        """Grammar rule.

        param_var -> STAR_POW NAME type_tag EQ expression
        param_var -> STAR_POW NAME type_tag
        param_var -> STAR_MUL NAME type_tag EQ expression
        param_var -> STAR_MUL NAME type_tag
        param_var -> NAME type_tag EQ expression
        param_var -> NAME type_tag
        """
        meta = {"unpack": None, "value": None}
        if node.kid[-2].name == Tok.EQ:
            del node.kid[-2]
            meta["value"] = node.kid[-1]
        if node.kid[0].name != "NAME":
            meta["unpack"] = node.kid[0]
            meta["name"] = node.kid[1]
            meta["type_tag"] = node.kid[2]
        else:
            meta["name"] = node.kid[0]
            meta["type_tag"] = node.kid[1]
        replace_node(
            node,
            ast.ParamVar(
                name=meta["name"],
                type_tag=meta["type_tag"],
                unpack=meta["unpack"],
                value=meta["value"],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_enum(self, node: ast.AstNode) -> None:
        """Grammar rule.

        enum -> enum_def
        enum -> enum_decl
        """
        replace_node(node, node.kid[0])

    def exit_enum_decl(self, node: ast.AstNode) -> None:
        """Grammar rule.

        enum_decl -> doc_tag decorators KW_ENUM access_tag NAME inherited_archs enum_block
        enum_decl -> doc_tag decorators KW_ENUM access_tag NAME inherited_archs SEMI
        enum_decl -> doc_tag KW_ENUM access_tag NAME inherited_archs enum_block
        enum_decl -> doc_tag KW_ENUM access_tag NAME inherited_archs SEMI
        """
        if type(node.kid[1]) == ast.Token:
            del node.kid[1]
            replace_node(
                node,
                ast.Enum(
                    doc=node.kid[0],
                    decorators=None,
                    access=node.kid[1],
                    name=node.kid[2],
                    base_classes=node.kid[3],
                    body=node.kid[-1] if type(node.kid[-1]) == ast.EnumBlock else None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            replace_node(
                node,
                ast.Enum(
                    doc=node.kid[0],
                    decorators=node.kid[1],
                    access=node.kid[2],
                    name=node.kid[3],
                    base_classes=node.kid[4],
                    body=node.kid[-1] if type(node.kid[-1]) == ast.EnumBlock else None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        if type(node.kid[-1]) == ast.Token:
            del node.kid[-1]

    def exit_enum_def(self, node: ast.AstNode) -> None:
        """Grammar rule.

        enum_def -> doc_tag dotted_name enum_ref enum_block
        enum_def -> doc_tag enum_ref enum_block
        """
        replace_node(
            node,
            ast.EnumDef(
                doc=node.kid[0],
                enum=node.kid[-2],
                mod=node.kid[1] if len(node.kid) == 4 else None,
                body=node.kid[-1],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_enum_block(self, node: ast.AstNode) -> None:
        """Grammar rule.

        enum_block -> LBRACE enum_stmt_list RBRACE
        enum_block -> LBRACE RBRACE
        """
        if len(node.kid) == 3:
            ret = replace_node(node, node.kid[1])
            node = ret if ret else node
        else:
            node.kid = []
        replace_node(
            node,
            ast.EnumBlock(
                stmts=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_enum_stmt_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        enum_stmt_list -> enum_stmt_list COMMA enum_op_assign
        enum_stmt_list -> enum_stmt_list COMMA NAME
        enum_stmt_list -> enum_op_assign
        enum_stmt_list -> NAME
        """
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]

    def exit_enum_op_assign(self, node: ast.AstNode) -> None:
        """Grammar rule.

        enum_op_assign -> NAME EQ expression
        """
        del node.kid[1]
        replace_node(
            node,
            ast.Assignment(
                target=node.kid[0],
                value=node.kid[1],
                mutable=False,
                is_static=False,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_member_block(self, node: ast.AstNode) -> None:
        """Grammar rule.

        member_block -> LBRACE member_stmt_list RBRACE
        member_block -> LBRACE RBRACE
        """
        if len(node.kid) == 3:
            ret = replace_node(node, node.kid[1])
            node = ret if ret else node
        else:
            node.kid = []
        replace_node(
            node,
            ast.ArchBlock(
                members=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_member_stmt_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        member_stmt_list -> member_stmt_list member_stmt
        member_stmt_list -> member_stmt
        """
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]

    def exit_member_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        member_stmt -> ability
        member_stmt -> has_stmt
        """
        replace_node(node, node.kid[0])

    def exit_has_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        has_stmt -> doc_tag static_tag KW_FREEZE access_tag has_assign_clause SEMI
        has_stmt -> doc_tag static_tag KW_HAS access_tag has_assign_clause SEMI
        """
        is_frozen = node.kid[2].name == Tok.KW_FREEZE
        node.kid = [node.kid[0], node.kid[1], node.kid[3], node.kid[4]]
        replace_node(
            node,
            ast.ArchHas(
                doc=node.kid[0],
                is_static=node.kid[1],
                access=node.kid[2],
                vars=node.kid[3],
                is_frozen=is_frozen,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_static_tag(self, node: ast.AstNode) -> None:
        """Grammar rule.

        static_tag -> KW_STATIC
        static_tag -> empty
        """
        replace_node(node, node.kid[0] if len(node.kid) else None)

    def exit_has_assign_clause(self, node: ast.AstNode) -> None:
        """Grammar rule.

        has_assign_clause -> has_assign_clause COMMA typed_has_clause
        has_assign_clause -> typed_has_clause
        """
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        replace_node(
            node,
            ast.HasVarList(
                vars=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_typed_has_clause(self, node: ast.AstNode) -> None:
        """Grammar rule.

        typed_has_clause -> NAME type_tag EQ expression
        typed_has_clause -> NAME type_tag
        """
        if node.kid[-2].name == Tok.EQ:
            del node.kid[-2]
        replace_node(
            node,
            ast.HasVar(
                name=node.kid[0],
                type_tag=node.kid[1],
                value=node.kid[2] if len(node.kid) == 3 else None,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_type_tag(self, node: ast.AstNode) -> None:
        """Grammar rule.

        type_tag -> COLON type_spec
        """
        replace_node(node, node.kid[1])

    def exit_return_type_tag(self, node: ast.AstNode) -> None:
        """Grammar rule.

        return_type_tag -> RETURN_HINT type_spec
        return_type_tag -> empty
        """
        if len(node.kid) == 2:
            replace_node(node, node.kid[1])
        else:
            replace_node(node, None)

    def exit_type_spec(self, node: ast.AstNode) -> None:
        """Grammar rule.

        type_spec -> type_spec BW_OR single_type
        type_spec -> type_spec NULL_OK
        type_spec -> single_type
        """
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        if len(node.kid) == 2:
            if type(node.kid[0]) == ast.TypeSpecList:
                node.kid[0].kid[0].null_ok = True
                node.kid = node.kid[0].kid
            elif type(node.kid[0]) == ast.TypeSpec:
                node.kid[0].null_ok = True
            else:
                raise Exception(f"Invalid type spec{type(node.kid[0])}")
        replace_node(
            node,
            ast.TypeSpecList(
                types=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_single_type(self, node: ast.AstNode) -> None:
        """Grammar rule.

        single_type -> TYP_DICT LSQUARE single_type COMMA single_type RSQUARE
        single_type -> TYP_SET LSQUARE single_type RSQUARE
        single_type -> TYP_TUPLE LSQUARE single_type RSQUARE
        single_type -> TYP_LIST LSQUARE single_type RSQUARE
        single_type -> dotted_name
        single_type -> NULL
        """
        meta = {
            "typ": node.kid[0],
            "list_nest": None,
            "dict_nest": None,
        }
        if len(node.kid) == 4:
            node.kid = [node.kid[0], node.kid[2]]
            meta["list_nest"] = node.kid[1]
        elif len(node.kid) == 6:
            node.kid = [node.kid[0], node.kid[2], node.kid[4]]
            meta["list_nest"] = node.kid[1]
            meta["dict_nest"] = node.kid[2]
        replace_node(
            node,
            ast.TypeSpec(
                spec_type=meta["typ"],
                list_nest=meta["list_nest"],
                dict_nest=meta["dict_nest"],
                null_ok=False,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_builtin_type(self, node: ast.AstNode) -> None:
        """Grammar rule.

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
        """
        replace_node(node, node.kid[0])

    def exit_code_block(self, node: ast.AstNode) -> None:
        """Grammar rule.

        code_block -> LBRACE statement_list RBRACE
        code_block -> LBRACE RBRACE
        """
        if len(node.kid) == 3:
            ret = replace_node(node, node.kid[1])
            node = ret if ret else node
        else:
            node.kid = []
        replace_node(
            node,
            ast.CodeBlock(
                stmts=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_statement_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        statement_list -> statement
        statement_list -> statement_list statement
        """
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]

    def exit_statement(self, node: ast.AstNode) -> None:
        """Grammar rule.

        statement -> walker_stmt
        statement -> await_stmt SEMI
        statement -> yield_stmt SEMI
        statement -> return_stmt SEMI
        statement -> report_stmt SEMI
        statement -> delete_stmt SEMI
        statement -> ctrl_stmt SEMI
        statement -> assert_stmt SEMI
        statement -> raise_stmt SEMI
        statement -> with_ctx_stmt
        statement -> while_stmt
        statement -> for_stmt
        statement -> try_stmt
        statement -> if_stmt
        statement -> expression SEMI
        statement -> static_assignment
        statement -> assignment SEMI
        statement -> ability_decl
        statement -> architype_decl
        """
        replace_node(node, node.kid[0])

    def exit_typed_ctx_block(self, node: ast.AstNode) -> None:
        """Grammar rule.

        typed_ctx_block -> RETURN_HINT type_spec code_block
        """
        del node.kid[0]
        replace_node(
            node,
            ast.TypedCtxBlock(
                type_ctx=node.kid[0],
                body=node.kid[1],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_if_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        if_stmt -> KW_IF expression code_block elif_list else_stmt
        if_stmt -> KW_IF expression code_block elif_list
        if_stmt -> KW_IF expression code_block else_stmt
        if_stmt -> KW_IF expression code_block
        """
        if len(node.kid) == 3:
            node.kid = [node.kid[1], node.kid[2]]
            replace_node(
                node,
                ast.IfStmt(
                    condition=node.kid[0],
                    body=node.kid[1],
                    elseifs=None,
                    else_body=None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        elif len(node.kid) == 4 and type(node.kid[3]) == ast.ElseIfs:
            node.kid = [node.kid[1], node.kid[2], node.kid[3]]
            replace_node(
                node,
                ast.IfStmt(
                    condition=node.kid[0],
                    body=node.kid[1],
                    elseifs=node.kid[2],
                    else_body=None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        elif len(node.kid) == 4:
            node.kid = [node.kid[1], node.kid[2], node.kid[3]]
            replace_node(
                node,
                ast.IfStmt(
                    condition=node.kid[0],
                    body=node.kid[1],
                    elseifs=None,
                    else_body=node.kid[2],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = [node.kid[1], node.kid[2], node.kid[3], node.kid[4]]
            replace_node(
                node,
                ast.IfStmt(
                    condition=node.kid[0],
                    body=node.kid[1],
                    elseifs=node.kid[2],
                    else_body=node.kid[3],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_elif_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        elif_list -> elif_list KW_ELIF expression code_block
        elif_list -> KW_ELIF expression code_block
        """
        cpy_node = ast.IfStmt(
            condition=node.kid[-2],
            body=node.kid[-1],
            elseifs=None,
            else_body=None,
            parent=node.parent,
            mod_link=self.mod_link,
            kid=[node.kid[-2], node.kid[-1]],
            line=node.line,
        )
        if len(node.kid) == 3:
            node.kid = [cpy_node]
        if len(node.kid) == 4:
            node.kid = node.kid[0].kid + [cpy_node]
        replace_node(
            node,
            ast.ElseIfs(
                elseifs=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_else_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        else_stmt -> KW_ELSE code_block
        """
        node.kid = [node.kid[1]]
        replace_node(
            node,
            ast.ElseStmt(
                body=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_try_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        try_stmt -> KW_TRY code_block except_list finally_stmt
        try_stmt -> KW_TRY code_block finally_stmt
        try_stmt -> KW_TRY code_block except_list
        try_stmt -> KW_TRY code_block
        """
        if len(node.kid) == 2:
            node.kid = [node.kid[1]]
            replace_node(
                node,
                ast.TryStmt(
                    body=node.kid[0],
                    excepts=None,
                    finally_body=None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        elif len(node.kid) == 3 and type(node.kid[2]) == ast.ExceptList:
            node.kid = [node.kid[1], node.kid[2]]
            replace_node(
                node,
                ast.TryStmt(
                    body=node.kid[0],
                    excepts=node.kid[1],
                    finally_body=None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        elif len(node.kid) == 3:
            node.kid = [node.kid[1], node.kid[2]]
            replace_node(
                node,
                ast.TryStmt(
                    body=node.kid[0],
                    excepts=None,
                    finally_body=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = [node.kid[1], node.kid[2], node.kid[3]]
            replace_node(
                node,
                ast.TryStmt(
                    body=node.kid[0],
                    excepts=node.kid[1],
                    finally_body=node.kid[2],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_except_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        except_list -> except_list except_def
        except_list -> except_def
        """
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        replace_node(
            node,
            ast.ExceptList(
                excepts=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_except_def(self, node: ast.AstNode) -> None:
        """Grammar rule.

        except_def -> KW_EXCEPT expression KW_AS NAME code_block
        except_def -> KW_EXCEPT expression code_block
        """
        if len(node.kid) == 3:
            node.kid = [node.kid[1], node.kid[2]]
            replace_node(
                node,
                ast.Except(
                    ex_type=node.kid[0],
                    name=None,
                    body=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = [node.kid[1], node.kid[3], node.kid[4]]
            replace_node(
                node,
                ast.Except(
                    ex_type=node.kid[0],
                    name=node.kid[1],
                    body=node.kid[2],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_finally_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        finally_stmt -> KW_FINALLY code_block
        """
        node.kid = [node.kid[1]]
        replace_node(
            node,
            ast.FinallyStmt(
                body=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_for_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        for_stmt -> KW_FOR NAME COMMA NAME KW_IN expression code_block
        for_stmt -> KW_FOR NAME KW_IN expression code_block
        for_stmt -> KW_FOR assignment KW_TO expression KW_BY expression code_block
        """
        if node.kid[2].name == Tok.KW_TO:
            node.kid = [node.kid[1], node.kid[3], node.kid[5], node.kid[6]]
            replace_node(
                node,
                ast.IterForStmt(
                    iter=node.kid[0],
                    condition=node.kid[1],
                    count_by=node.kid[2],
                    body=node.kid[3],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        elif node.kid[2].name == Tok.KW_IN:
            node.kid = [node.kid[1], node.kid[3], node.kid[4]]
            replace_node(
                node,
                ast.InForStmt(
                    name=node.kid[0],
                    collection=node.kid[1],
                    body=node.kid[2],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = [node.kid[1], node.kid[3], node.kid[5], node.kid[6]]
            replace_node(
                node,
                ast.DictForStmt(
                    k_name=node.kid[0],
                    v_name=node.kid[1],
                    collection=node.kid[2],
                    body=node.kid[3],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_while_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        while_stmt -> KW_WHILE expression code_block
        """
        node.kid = [node.kid[1], node.kid[2]]
        replace_node(
            node,
            ast.WhileStmt(
                condition=node.kid[0],
                body=node.kid[1],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_with_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        KW_WITH expr_as_list code_block
        """
        node.kid = [node.kid[1], node.kid[2]]
        replace_node(
            node,
            ast.WithStmt(
                exprs=node.kid[0],
                body=node.kid[1],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_expr_as_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        expr_as_list -> expr_as_list COMMA expression KW_AS NAME
        expr_as_list -> expr_as_list COMMA NAME
        expr_as_list -> expression KW_AS NAME
        expr_as_list -> expression
        """
        this_item = None
        if type(node.kid[0]) != ast.ExprAsItemList:
            this_item = ast.ExprAsItem(
                expr=node.kid[0],
                alias=node.kid[2] if len(node.kid) == 3 else None,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=[node.kid[0], node.kid[2]] if len(node.kid) == 3 else [node.kid[0]],
                line=node.line,
            )
            node.kid = [this_item]
        else:
            this_item = ast.ExprAsItem(
                expr=node.kid[-3] if node.kid[-2].name == Tok.KW_AS else node.kid[-1],
                alias=node.kid[-1] if node.kid[-2].name == Tok.KW_AS else None,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=[node.kid[-3], node.kid[-1]]
                if node.kid[-2].name == Tok.KW_AS
                else [node.kid[-1]],
                line=node.line,
            )
            node.kid = node.kid[0].kid + [this_item]
        replace_node(
            node,
            ast.ExprAsItemList(
                items=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_raise_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        raise_stmt -> KW_RAISE expression
        raise_stmt -> KW_RAISE
        """
        if len(node.kid) == 1:
            node.kid = []
            replace_node(
                node,
                ast.RaiseStmt(
                    cause=None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = [node.kid[1]]
            replace_node(
                node,
                ast.RaiseStmt(
                    cause=node.kid[0],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_assert_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        assert_stmt -> KW_ASSERT expression COMMA expression
        assert_stmt -> KW_ASSERT expression
        """
        if len(node.kid) == 4:
            node.kid = [node.kid[1], node.kid[3]]
            replace_node(
                node,
                ast.AssertStmt(
                    condition=node.kid[0],
                    error_msg=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = [node.kid[1]]
            replace_node(
                node,
                ast.AssertStmt(
                    condition=node.kid[0],
                    error_msg=None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_ctrl_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ctrl_stmt -> KW_SKIP
        ctrl_stmt -> KW_BREAK
        ctrl_stmt -> KW_CONTINUE
        """
        replace_node(
            node,
            ast.CtrlStmt(
                ctrl=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_delete_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        delete_stmt -> KW_DELETE expression
        """
        node.kid = [node.kid[1]]
        replace_node(
            node,
            ast.DeleteStmt(
                target=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_report_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        report_stmt -> KW_REPORT expression
        """
        node.kid = [node.kid[1]]
        replace_node(
            node,
            ast.ReportStmt(
                expr=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_return_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        return_stmt -> KW_RETURN expression
        return_stmt -> KW_RETURN
        """
        if len(node.kid) == 1:
            node.kid = []
            replace_node(
                node,
                ast.ReturnStmt(
                    expr=None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            node.kid = [node.kid[1]]
            replace_node(
                node,
                ast.ReturnStmt(
                    expr=node.kid[0],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_yield_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        yield_stmt -> KW_YIELD expression
        yield_stmt -> KW_YIELD
        """
        node.kid = [node.kid[1]]
        replace_node(
            node,
            ast.YieldStmt(
                expr=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_walker_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        walker_stmt -> disengage_stmt SEMI
        walker_stmt -> revisit_stmt
        walker_stmt -> visit_stmt
        walker_stmt -> ignore_stmt SEMI
        """
        replace_node(node, node.kid[0])

    def exit_ignore_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ignore_stmt -> KW_IGNORE expression
        """
        node.kid = [node.kid[1]]
        replace_node(
            node,
            ast.IgnoreStmt(
                target=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_visit_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        visit_stmt -> KW_VISIT sub_name_dotted expression else_stmt
        visit_stmt -> KW_VISIT expression else_stmt
        visit_stmt -> KW_VISIT sub_name_dotted expression SEMI
        visit_stmt -> KW_VISIT expression SEMI
        """
        meta = {"typ": None, "else_body": None}
        if type(node.kid[-1]) != ast.ElseStmt:
            if len(node.kid) == 4:
                node.kid = [node.kid[1], node.kid[2]]
                meta["typ"] = node.kid[0]
                meta["target"] = node.kid[1]
            else:
                node.kid = [node.kid[1]]
                meta["target"] = node.kid[0]
        elif len(node.kid) == 4:
            node.kid = [node.kid[1], node.kid[2], node.kid[3]]
            meta["typ"] = node.kid[0]
            meta["target"] = node.kid[1]
            meta["else_body"] = node.kid[2]
        else:
            node.kid = [node.kid[1], node.kid[2]]
            meta["target"] = node.kid[0]
            meta["else_body"] = node.kid[1]
        replace_node(
            node,
            ast.VisitStmt(
                vis_type=meta["typ"],
                target=meta["target"],
                else_body=meta["else_body"],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_revisit_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        revisit_stmt -> KW_REVISIT expression else_stmt
        revisit_stmt -> KW_REVISIT else_stmt
        revisit_stmt -> KW_REVISIT expression SEMI
        revisit_stmt -> KW_REVISIT SEMI
        """
        meta = {"hops": None, "else_body": None}
        if node.kid[-1].name == Tok.SEMI:
            if len(node.kid) == 3:
                node.kid = [node.kid[1]]
                meta["hops"] = node.kid[0]
        elif len(node.kid) == 3:
            node.kid = [node.kid[1], node.kid[2]]
            meta["hops"] = node.kid[0]
            meta["else_body"] = node.kid[1]
        else:
            node.kid = [node.kid[1], node.kid[2]]
            meta["hops"] = node.kid[0]
            meta["else_body"] = node.kid[1]
        replace_node(
            node,
            ast.RevisitStmt(
                hops=meta["hops"],
                else_body=meta["else_body"],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_disengage_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        disengage_stmt -> KW_DISENGAGE
        """
        node.kid = []
        replace_node(
            node,
            ast.DisengageStmt(
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_await_stmt(self, node: ast.AstNode) -> None:
        """Grammar rule.

        await_stmt -> KW_AWAIT expression
        """
        node.kid = [node.kid[1]]
        replace_node(
            node,
            ast.AwaitStmt(
                target=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_assignment(self, node: ast.AstNode) -> None:
        """Grammar rule.

        assignment -> KW_FREEZE atom EQ expression
        assignment -> atom EQ expression
        """
        frozen = len(node.kid) == 4
        node.kid = [node.kid[-3], node.kid[-1]]
        replace_node(
            node,
            ast.Assignment(
                is_static=False,
                target=node.kid[0],
                value=node.kid[1],
                mutable=not frozen,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_static_assignment(self, node: ast.AstNode) -> None:
        """Grammar rule.

        static_assignment -> KW_HAS assignment_list SEMI
        """
        ret = replace_node(node, node.kid[1])
        node = ret if ret else node
        for i in node.kid:
            i.is_static = True

    def binary_op_helper(self, node: ast.AstNode) -> None:
        """Grammar rule."""
        if len(node.kid) == 1:
            replace_node(node, node.kid[0])
        else:
            node.kid = [node.kid[0], node.kid[1], node.kid[2]]
            replace_node(
                node,
                ast.BinaryExpr(
                    left=node.kid[0],
                    op=node.kid[1],
                    right=node.kid[2],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_expression(self, node: ast.AstNode) -> None:
        """Grammar rule.

        expression -> walrus_assign KW_IF expression KW_ELSE expression
        expression -> walrus_assign
        """
        if len(node.kid) == 1:
            replace_node(node, node.kid[0])
        else:
            node.kid = [node.kid[0], node.kid[2], node.kid[4]]
            replace_node(
                node,
                ast.IfElseExpr(
                    value=node.kid[0],
                    condition=node.kid[1],
                    else_value=node.kid[2],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_walrus_assign(self, node: ast.AstNode) -> None:
        """Grammar rule.

        walrus_assign -> pipe walrus_op walrus_assign
        walrus_assign -> pipe
        """
        self.binary_op_helper(node)

    def exit_pipe(self, node: ast.AstNode) -> None:
        """Grammar rule.

        pipe -> pipe_back PIPE_FWD filter_compr
        pipe -> pipe_back PIPE_FWD pipe
        pipe -> pipe_back
        """
        self.binary_op_helper(node)

    def exit_pipe_back(self, node: ast.AstNode) -> None:
        """Grammar rule.

        pipe_back -> elvis_check PIPE_BKWD filter_compr
        pipe_back -> elvis_check PIPE_BKWD pipe_back
        pipe_back -> elvis_check
        """
        self.binary_op_helper(node)

    def exit_elvis_check(self, node: ast.AstNode) -> None:
        """Grammar rule.

        elvis_check -> bitwise_or ELVIS_OP elvis_check
        elvis_check -> bitwise_or
        """
        self.binary_op_helper(node)

    def exit_bitwise_or(self, node: ast.AstNode) -> None:
        """Grammar rule.

        bitwise_or -> bitwise_xor BW_OR bitwise_or
        bitwise_or -> bitwise_xor
        """
        self.binary_op_helper(node)

    def exit_bitwise_xor(self, node: ast.AstNode) -> None:
        """Grammar rule.

        bitwise_xor -> bitwise_and BW_XOR bitwise_xor
        bitwise_xor -> bitwise_and
        """
        self.binary_op_helper(node)

    def exit_bitwise_and(self, node: ast.AstNode) -> None:
        """Grammar rule.

        bitwise_and -> shift BW_AND bitwise_and
        bitwise_and -> shift
        """
        self.binary_op_helper(node)

    def exit_shift(self, node: ast.AstNode) -> None:
        """Grammar rule.

        shift -> logical RSHIFT shift
        shift -> logical LSHIFT shift
        shift -> logical
        """
        self.binary_op_helper(node)

    def exit_logical(self, node: ast.AstNode) -> None:
        """Grammar rule.

        logical -> NOT logical
        logical -> compare KW_OR logical
        logical -> compare KW_AND logical
        logical -> compare
        """
        if len(node.kid) == 2:
            node.kid = [node.kid[0], node.kid[1]]
            replace_node(
                node,
                ast.UnaryExpr(
                    op=node.kid[0],
                    operand=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            self.binary_op_helper(node)

    def exit_compare(self, node: ast.AstNode) -> None:
        """Grammar rule.

        compare -> arithmetic cmp_op compare
        compare -> arithmetic
        """
        self.binary_op_helper(node)

    def exit_arithmetic(self, node: ast.AstNode) -> None:
        """Grammar rule.

        arithmetic -> term MINUS arithmetic
        arithmetic -> term PLUS arithmetic
        arithmetic -> term
        """
        self.binary_op_helper(node)

    def exit_term(self, node: ast.AstNode) -> None:
        """Grammar rule.

        term -> factor MOD term
        term -> factor DIV term
        term -> factor FLOOR_DIV term
        term -> factor STAR_MUL term
        term -> factor
        """
        self.binary_op_helper(node)

    def exit_factor(self, node: ast.AstNode) -> None:
        """Grammar rule.

        factor -> power
        factor -> BW_NOT factor
        factor -> MINUS factor
        factor -> PLUS factor
        """
        if len(node.kid) == 2:
            node.kid = [node.kid[0], node.kid[1]]
            replace_node(
                node,
                ast.UnaryExpr(
                    op=node.kid[0],
                    operand=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            self.binary_op_helper(node)

    def exit_power(self, node: ast.AstNode) -> None:
        """Grammar rule.

        power -> connect STAR_POW power
        power -> connect
        """
        self.binary_op_helper(node)

    def exit_connect(self, node: ast.AstNode) -> None:
        """Grammar rule.

        connect -> atomic_pipe
        connect -> atomic_pipe connect_op connect
        connect -> atomic_pipe disconnect_op connect
        """
        self.binary_op_helper(node)

    def exit_atomic_pipe(self, node: ast.AstNode) -> None:
        """Grammar rule.

        atomic_pipe -> atomic_pipe_back
        atomic_pipe -> atomic_pipe spawn_pipe_op atomic_pipe_back
        """
        self.binary_op_helper(node)

    def exit_atomic_pipe_back(self, node: ast.AstNode) -> None:
        """Grammar rule.

        atomic_pipe -> unpack
        atomic_pipe -> atomic_pipe_back A_PIPE_BKWD unpack
        """
        self.binary_op_helper(node)

    def exit_unpack(self, node: ast.AstNode) -> None:
        """Grammar rule.

        unpack -> ref
        unpack -> STAR_MUL atom
        unpack -> STAR_POW atom
        """
        if len(node.kid) == 1:
            replace_node(node, node.kid[0])
        else:
            if node.kid[0].name == Tok.STAR_MUL:
                replace_node(
                    node,
                    ast.UnpackExpr(
                        target=node.kid[-1],
                        is_dict=False,
                        parent=node.parent,
                        mod_link=self.mod_link,
                        kid=[node.kid[-1]],
                        line=node.line,
                    ),
                )
            else:
                replace_node(
                    node,
                    ast.UnpackExpr(
                        target=node.kid[-1],
                        is_dict=True,
                        parent=node.parent,
                        mod_link=self.mod_link,
                        kid=[node.kid[-1]],
                        line=node.line,
                    ),
                )

    def exit_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ref -> ds_call
        ref -> KW_REF ds_call
        """
        if len(node.kid) == 2:
            node.kid = [node.kid[0], node.kid[1]]
            replace_node(
                node,
                ast.UnaryExpr(
                    op=node.kid[0],
                    operand=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

        else:
            self.binary_op_helper(node)

    def exit_ds_call(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ds_call -> walrus_assign
        ds_call -> PIPE_FWD walrus_assign
        ds_call -> spawn_pipe_op walrus_assign
        """
        if len(node.kid) == 2:
            node.kid = [node.kid[0], node.kid[1]]
            replace_node(
                node,
                ast.UnaryExpr(
                    op=node.kid[0],
                    operand=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            self.binary_op_helper(node)

    def exit_walrus_op(self, node: ast.AstNode) -> None:
        """Grammar rule.

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
        """
        replace_node(node, node.kid[0])

    def exit_cmp_op(self, node: ast.AstNode) -> None:
        """Grammar rule.

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
        """
        replace_node(node, node.kid[0])

    def exit_atom(self, node: ast.AstNode) -> None:
        """Grammar rule.

        atom -> edge_op_ref
        atom -> all_refs
        atom -> atomic_chain
        atom -> LPAREN expression RPAREN
        atom -> atom_collection
        atom -> atom_literal
        """
        if len(node.kid) == 3:
            node.kid = [node.kid[0], node.kid[1]]
            replace_node(
                node,
                ast.UnaryExpr(
                    op=node.kid[0],
                    operand=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        else:
            replace_node(node, node.kid[0])

    def exit_atom_literal(self, node: ast.AstNode) -> None:
        """Grammar rule.

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
        """
        replace_node(node, node.kid[0])

    def exit_atom_collection(self, node: ast.AstNode) -> None:
        """Grammar rule.

        atom_collection -> dict_compr
        atom_collection -> set_compr
        atom_collection -> gen_compr
        atom_collection -> list_compr
        atom_collection -> dict_val
        atom_collection -> set_val
        atom_collection -> tuple_val
        atom_collection -> list_val
        """
        replace_node(node, node.kid[0])

    def exit_multistring(self, node: ast.AstNode) -> None:
        """Grammar rule.

        multistring -> fstring multistring
        multistring -> STRING multistring
        multistring -> fstring
        multistring -> STRING
        """
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        replace_node(
            node,
            ast.MultiString(
                strings=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_list_val(self, node: ast.AstNode) -> None:
        """Grammar rule.

        list_val -> LSQUARE expr_list RSQUARE
        list_val -> LSQUARE RSQUARE
        """
        if len(node.kid) > 2:
            ret = replace_node(node, node.kid[1])
            node = ret if ret else node
        else:
            node.kid = []
        replace_node(
            node,
            ast.ListVal(
                values=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_tuple_val(self, node: ast.AstNode) -> None:
        """Grammar rule.

        tuple_val -> LPAREN tuple_list RPAREN
        tuple_val -> LPAREN RPAREN
        """
        if len(node.kid) > 2:
            replace_node(node, node.kid[1])
        else:
            node.kid = []
            replace_node(
                node,
                ast.TupleVal(
                    first_expr=None,
                    exprs=None,
                    assigns=None,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_set_val(self, node: ast.AstNode) -> None:
        """Grammar rule.

        set_val -> LBRACE expr_list RBRACE
        """
        ret = replace_node(node, node.kid[1])
        node = ret if ret else node
        replace_node(
            node,
            ast.SetVal(
                values=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_expr_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        expr_list -> expr_list COMMA expression
        expr_list -> expression
        """
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        replace_node(
            node,
            ast.ExprList(
                values=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_tuple_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        tuple_list -> expression COMMA expr_list COMMA assignment_list
        tuple_list -> expression COMMA assignment_list
        tuple_list -> assignment_list
        tuple_list -> expression COMMA expr_list
        tuple_list -> expression COMMA
        """
        first_expr = None
        exprs = None
        assigns = None
        if len(node.kid) == 1:
            assigns = node.kid[0]
        elif len(node.kid) == 2:
            del node.kid[1]
            first_expr = node.kid[0]
        elif len(node.kid) == 3:
            del node.kid[1]
            first_expr = node.kid[0]
            if isinstance(node.kid[1], ast.ExprList):
                exprs = node.kid[1]
            else:
                assigns = node.kid[1]
        elif len(node.kid) == 5:
            first_expr = node.kid[0]
            exprs = node.kid[2]
            assigns = node.kid[4]
            del node.kid[3]
            del node.kid[1]
        replace_node(
            node,
            ast.TupleVal(
                first_expr=first_expr,
                exprs=exprs,
                assigns=assigns,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_dict_val(self, node: ast.AstNode) -> None:
        """Grammar rule.

        dict_val -> LBRACE kv_pairs RBRACE
        dict_val -> LBRACE RBRACE
        """
        if len(node.kid) > 3:
            node.kid = node.kid[:-3]
        else:
            node.kid = []
        replace_node(
            node,
            ast.DictVal(
                kv_pairs=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_list_compr(self, node: ast.AstNode) -> None:
        """Grammar rule.

        list_compr -> LSQUARE inner_compr RSQUARE
        """
        ret = replace_node(node, node.kid[1])
        if type(ret) == ast.InnerCompr:
            ret.is_list = True
        else:
            self.ice("Expected InnerCompr")

    def exit_gen_compr(self, node: ast.AstNode) -> None:
        """Grammar rule.

        gen_compr -> LPAREN inner_compr RPAREN
        """
        ret = replace_node(node, node.kid[1])
        if type(ret) == ast.InnerCompr:
            ret.is_gen = True
        else:
            self.ice("Expected InnerCompr")

    def exit_set_compr(self, node: ast.AstNode) -> None:
        """Grammar rule.

        set_compr -> LBRACE inner_compr RBRACE
        """
        ret = replace_node(node, node.kid[1])
        if type(ret) == ast.InnerCompr:
            ret.is_set = True
        else:
            self.ice("Expected InnerCompr")

    def exit_inner_compr(self, node: ast.AstNode) -> None:
        """Grammar rule.

        inner_compr -> expression KW_FOR NAME KW_IN walrus_assign KW_IF expression
        inner_compr -> expression KW_FOR NAME KW_IN walrus_assign
        """
        meta = {
            "out_expr": node.kid[0],
            "name": node.kid[2],
            "collection": node.kid[4],
            "conditional": None,
        }
        if node.kid[-2].name == Tok.KW_IF:
            meta["conditional"] = node.kid[-1]
        if len(node.kid) == 5:
            node.kid = [node.kid[0], node.kid[2], node.kid[4]]
        elif len(node.kid) == 7:
            node.kid = [node.kid[0], node.kid[2], node.kid[4], node.kid[6]]
        replace_node(
            node,
            ast.InnerCompr(
                out_expr=meta["out_expr"],
                name=meta["name"],
                collection=meta["collection"],
                conditional=meta["conditional"],
                is_list=False,
                is_gen=False,
                is_set=False,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_dict_compr(self, node: ast.AstNode) -> None:
        """Grammar rule.

        dict_compr -> LBRACE expression COLON expression KW_FOR NAME COMMA NAME KW_IN walrus_assign KW_IF expression RBRACE # noqa
        dict_compr -> LBRACE expression COLON expression KW_FOR NAME COMMA NAME KW_IN walrus_assign RBRACE
        dict_compr -> LBRACE expression COLON expression KW_FOR NAME KW_IN walrus_assign KW_IF expression RBRACE
        dict_compr -> LBRACE expression COLON expression KW_FOR NAME KW_IN walrus_assign RBRACE
        """
        meta = {
            "outk_expr": node.kid[1],
            "outv_expr": node.kid[3],
            "k_name": node.kid[5],
            "conditional": None,
        }
        if node.kid[6].name == Tok.COMMA:
            meta["v_name"] = node.kid[7]
            meta["collection"] = node.kid[9]
        else:
            meta["v_name"] = None
            meta["collection"] = node.kid[7]
        if node.kid[-3].name == Tok.KW_IF:
            meta["conditional"] = node.kid[-2]
        if len(node.kid) == 9:
            node.kid = [node.kid[1], node.kid[3], node.kid[5], node.kid[7]]
        elif len(node.kid) == 11:
            node.kid = [node.kid[1], node.kid[3], node.kid[5], node.kid[7], node.kid[9]]
        elif len(node.kid) == 13:
            node.kid = [
                node.kid[1],
                node.kid[3],
                node.kid[5],
                node.kid[7],
                node.kid[9],
                node.kid[11],
            ]
        replace_node(
            node,
            ast.DictCompr(
                outk_expr=meta["outk_expr"],
                outv_expr=meta["outv_expr"],
                k_name=meta["k_name"],
                v_name=meta["v_name"],
                collection=meta["collection"],
                conditional=meta["conditional"],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_kv_pairs(self, node: ast.AstNode) -> None:
        """Grammar rule.

        kv_pairs -> kv_pairs COMMA expression COLON expression
        kv_pairs -> expression COLON expression
        """
        node = ast.KVPair(
            key=node.kid[-3],
            value=node.kid[-1],
            parent=node.parent,
            mod_link=self.mod_link,
            kid=node.kid,
            line=node.line,
        )
        if len(node.kid) == 3:
            if node.parent is not None:
                node.parent.kid = [node] + node.parent.kid
            node.kid = [node.kid[0], node.kid[2]]
        else:
            if node.parent is not None:
                node.parent.kid = [node] + node.kid[:-5] + node.parent.kid
            node.kid = [node.kid[-3], node.kid[-1]]

    def exit_atomic_chain(self, node: ast.AstNode) -> None:
        """Grammar rule.

        atomic_chain -> atomic_call
        atomic_chain -> atomic_chain_unsafe
        atomic_chain -> atomic_chain_safe
        """
        replace_node(node, node.kid[0])

    def exit_atomic_chain_unsafe(self, node: ast.AstNode) -> None:
        """Grammar rule.

        atomic_chain_unsafe -> atom filter_compr
        atomic_chain_unsafe -> atom arch_ref
        atomic_chain_unsafe -> atom index_slice
        atomic_chain_unsafe -> atom DOT NAME
        atomic_chain_unsafe -> atom DOT_FWD NAME
        atomic_chain_unsafe -> atom DOT_BKWD NAME
        """
        target = node.kid[0]
        right = node.kid[-1]
        if type(node.kid[1]) == ast.Token and node.kid[1].name == Tok.DOT_FWD:
            target = node.kid[-1]
            right = node.kid[0]
        if len(node.kid) == 3:
            del node.kid[1]
        replace_node(
            node,
            ast.AtomTrailer(
                target=target,
                right=right,
                null_ok=False,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_atomic_chain_safe(self, node: ast.AstNode) -> None:
        """Grammar rule.

        atomic_chain_safe -> atom NULL_OK filter_compr
        atomic_chain_safe -> atom NULL_OK arch_ref
        atomic_chain_safe -> atom NULL_OK index_slice
        atomic_chain_safe -> atom NULL_OK DOT NAME
        atomic_chain_safe -> atom NULL_OK DOT_FWD NAME
        atomic_chain_safe -> atom NULL_OK DOT_BKWD NAME
        """
        target = node.kid[0]
        right = node.kid[-1]
        if type(node.kid[1]) == ast.Token and node.kid[1].name == Tok.DOT_FWD:
            target = node.kid[-1]
            right = node.kid[0]
        if len(node.kid) == 3:
            del node.kid[1]
        replace_node(
            node,
            ast.AtomTrailer(
                target=target,
                right=right,
                null_ok=True,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_atomic_call(self, node: ast.AstNode) -> None:
        """Grammar rule.

        atomic_call -> atom func_call_tail
        """
        replace_node(
            node,
            ast.FuncCall(
                target=node.kid[0],
                params=node.kid[1],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_func_call_tail(self, node: ast.AstNode) -> None:
        """Grammar rule.

        func_call_tail -> LPAREN param_list RPAREN
        func_call_tail -> LPAREN RPAREN
        """
        if len(node.kid) == 2:
            replace_node(node, None)
        else:
            replace_node(node, node.kid[1])

    def exit_param_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        param_list -> expr_list COMMA assignment_list
        param_list -> assignment_list
        param_list -> expr_list
        """
        if len(node.kid) == 1:
            if type(node.kid[0]) == ast.ExprList:
                replace_node(
                    node,
                    ast.ParamList(
                        p_args=node.kid[0],
                        p_kwargs=None,
                        parent=node.parent,
                        mod_link=self.mod_link,
                        kid=node.kid,
                        line=node.line,
                    ),
                )
            else:
                replace_node(
                    node,
                    ast.ParamList(
                        p_args=None,
                        p_kwargs=node.kid[0],
                        parent=node.parent,
                        mod_link=self.mod_link,
                        kid=node.kid,
                        line=node.line,
                    ),
                )
        else:
            node.kid = [node.kid[0], node.kid[2]]
            replace_node(
                node,
                ast.ParamList(
                    p_args=node.kid[0],
                    p_kwargs=node.kid[1],
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_assignment_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        assignment_list -> assignment_list COMMA assignment
        assignment_list -> assignment
        """
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        replace_node(
            node,
            ast.AssignmentList(
                values=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_index_slice(self, node: ast.AstNode) -> None:
        """Grammar rule.

        index_slice -> LSQUARE COLON expression RSQUARE
        index_slice -> LSQUARE expression COLON RSQUARE
        index_slice -> LSQUARE expression COLON expression RSQUARE
        index_slice -> LSQUARE expression RSQUARE
        """
        if len(node.kid) == 3:
            node.kid = [node.kid[1]]
            replace_node(
                node,
                ast.IndexSlice(
                    start=node.kid[0],
                    stop=None,
                    is_range=False,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )
        elif len(node.kid) == 4:
            start = node.kid[1] if type(node.kid[1]) != ast.Token else None
            stop = node.kid[2] if type(node.kid[2]) != ast.Token else None
            node.kid = [start if start else stop]
            if not isinstance(node.kid[0], ast.AstNode):
                self.ice("Somethings wrong with the parser.")
            else:
                replace_node(
                    node,
                    ast.IndexSlice(
                        start=start,
                        stop=stop,
                        is_range=True,
                        parent=node.parent,
                        mod_link=self.mod_link,
                        kid=[node.kid[0]],
                        line=node.line,
                    ),
                )
        else:
            node.kid = [node.kid[1], node.kid[3]]
            replace_node(
                node,
                ast.IndexSlice(
                    start=node.kid[0],
                    stop=node.kid[1],
                    is_range=True,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_global_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        global_ref -> GLOBAL_OP NAME
        """
        replace_node(
            node,
            ast.ArchRef(
                name_ref=node.kid[-1],
                arch=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_arch_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        arch_ref -> ability_ref
        arch_ref -> object_ref
        arch_ref -> walker_ref
        arch_ref -> edge_ref
        arch_ref -> node_ref
        """
        replace_node(node, node.kid[0])

    def exit_strict_arch_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        strict_arch_ref -> object_ref
        strict_arch_ref -> walker_ref
        strict_arch_ref -> edge_ref
        strict_arch_ref -> node_ref
        """
        replace_node(node, node.kid[0])

    def exit_node_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        node_ref -> NODE_OP NAME
        """
        replace_node(
            node,
            ast.ArchRef(
                name_ref=node.kid[-1],
                arch=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_edge_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        edge_ref -> EDGE_OP NAME
        """
        replace_node(
            node,
            ast.ArchRef(
                name_ref=node.kid[-1],
                arch=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_walker_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        walker_ref -> WALKER_OP NAME
        """
        replace_node(
            node,
            ast.ArchRef(
                name_ref=node.kid[-1],
                arch=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_object_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        object_ref -> OBJECT_OP NAME
        """
        replace_node(
            node,
            ast.ArchRef(
                name_ref=node.kid[-1],
                arch=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_enum_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        object_ref -> ENUM_OP NAME
        """
        replace_node(
            node,
            ast.ArchRef(
                name_ref=node.kid[-1],
                arch=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_ability_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        ability_ref -> ABILITY_OP special_refs
        ability_ref -> ABILITY_OP NAME
        """
        replace_node(
            node,
            ast.ArchRef(
                name_ref=node.kid[-1],
                arch=node.kid[0],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_edge_op_ref(self, node: ast.AstNode) -> None:
        """Grammar rule.

        edge_op_ref -> edge_any
        edge_op_ref -> edge_from
        edge_op_ref -> edge_to
        """
        replace_node(node, node.kid[0])

    def exit_edge_to(self, node: ast.AstNode) -> None:
        """Grammar rule.

        edge_to -> ARROW_R_p1 expression COLON filter_compare_list ARROW_R_p2
        edge_to -> ARROW_R_p1 expression ARROW_R_p2
        edge_to -> ARROW_R
        """
        ftype = node.kid[1] if len(node.kid) >= 3 else None
        fcond = node.kid[3] if len(node.kid) >= 5 else None
        replace_node(
            node,
            ast.EdgeOpRef(
                filter_type=ftype,
                filter_cond=fcond,
                edge_dir=EdgeDir.OUT,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_edge_from(self, node: ast.AstNode) -> None:
        """Grammar rule.

        edge_from -> ARROW_L_p1 expression COLON filter_compare_list ARROW_L_p2
        edge_from -> ARROW_L_p1 expression ARROW_L_p2
        edge_from -> ARROW_L
        """
        ftype = node.kid[1] if len(node.kid) >= 3 else None
        fcond = node.kid[3] if len(node.kid) >= 5 else None
        replace_node(
            node,
            ast.EdgeOpRef(
                filter_type=ftype,
                filter_cond=fcond,
                edge_dir=EdgeDir.IN,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_edge_any(self, node: ast.AstNode) -> None:
        """Grammar rule.

        edge_any -> ARROW_L_p1 expression COLON filter_compare_list ARROW_R_p2
        edge_any -> ARROW_L_p1 expression ARROW_R_p2
        edge_any -> ARROW_BI
        """
        ftype = node.kid[1] if len(node.kid) >= 3 else None
        fcond = node.kid[3] if len(node.kid) >= 5 else None
        replace_node(
            node,
            ast.EdgeOpRef(
                filter_type=ftype,
                filter_cond=fcond,
                edge_dir=EdgeDir.ANY,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_connect_op(self, node: ast.AstNode) -> None:
        """Grammar rule.

        connect_op -> connect_from
        connect_op -> connect_to
        """
        replace_node(node, node.kid[0])

    def exit_disconnect_op(self, node: ast.AstNode) -> None:
        """Grammar rule.

        disconnect_op -> NOT edge_op_ref
        """
        ret = replace_node(node, node.kid[1])
        node = ret if ret else node
        if type(node) == ast.EdgeOpRef:
            replace_node(
                node,
                ast.DisconnectOp(
                    filter_type=node.filter_type,
                    filter_cond=node.filter_cond,
                    edge_dir=node.edge_dir,
                    parent=node.parent,
                    mod_link=self.mod_link,
                    kid=node.kid,
                    line=node.line,
                ),
            )

    def exit_connect_to(self, node: ast.AstNode) -> None:
        """Grammar rule.

        connect_to -> CARROW_R_p1 expression COLON assignment_list CARROW_R_p2
        connect_to -> CARROW_R_p1 expression CARROW_R_p2
        connect_to -> CARROW_R
        """
        ctype = node.kid[1] if len(node.kid) >= 3 else None
        cassig = node.kid[3] if len(node.kid) >= 5 else None
        replace_node(
            node,
            ast.ConnectOp(
                conn_type=ctype,
                conn_assign=cassig,
                edge_dir=EdgeDir.OUT,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_connect_from(self, node: ast.AstNode) -> None:
        """Grammar rule.

        connect_from -> CARROW_L_p1 expression COLON assignment_list CARROW_L_p2
        connect_from -> CARROW_L_p1 expression CARROW_L_p2
        connect_from -> CARROW_L
        """
        ctype = node.kid[1] if len(node.kid) >= 3 else None
        cassig = node.kid[3] if len(node.kid) >= 5 else None
        replace_node(
            node,
            ast.ConnectOp(
                conn_type=ctype,
                conn_assign=cassig,
                edge_dir=EdgeDir.IN,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_filter_compr(self, node: ast.AstNode) -> None:
        """Grammar rule.

        filter_compr -> LPAREN EQ filter_compare_list RPAREN
        """
        node.kid = node.kid[:-4]
        replace_node(
            node,
            ast.FilterCompr(
                compares=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_filter_compare_list(self, node: ast.AstNode) -> None:
        """Grammar rule.

        filter_compare_list -> filter_compare_list COMMA NAME cmp_op expression
        filter_compare_list -> NAME cmp_op expression
        """
        if len(node.kid) == 3:
            if node.parent is not None:
                node.parent.kid = [node] + node.parent.kid
        else:
            if node.parent is not None:
                node.parent.kid = [node] + node.kid[:-5] + node.parent.kid
            node.kid = [node.kid[-3], node.kid[-2], node.kid[-1]]
        replace_node(
            node,
            ast.BinaryExpr(
                op=node.kid[1],
                left=node.kid[0],
                right=node.kid[2],
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_empty(self, node: ast.AstNode) -> None:
        """Grammar rule.

        empty -> <empty>
        """
        replace_node(node, None)

    # FString Parser Rules
    # --------------------

    def exit_fstring(self, node: ast.AstNode) -> None:
        """Grammar rule.

        fstring -> STRING_START fstr_parts STRING_END
        """
        replace_node(node, node.kid[1])

    def exit_fstr_parts(self, node: ast.AstNode) -> None:
        """Grammar rule.

        fstr_parts -> fstring
        fstr_parts -> expression
        fstr_parts -> PIECE
        fstr_parts -> fstr_parts PIECE
        fstr_parts -> fstr_parts expression
        """
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        else:
            node.kid = [node.kid[0]]
        replace_node(
            node,
            ast.FString(
                parts=node.kid,
                parent=node.parent,
                mod_link=self.mod_link,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_fstr_expr(self, node: ast.AstNode) -> None:
        """Grammar rule.

        Should not exist; replaced with expression
        """
        self.error("fstr_expr should not exist in parse tree; replaced with expression")
        raise ValueError(
            "fstr_expr should not exist in parse tree; replaced with expression"
        )
