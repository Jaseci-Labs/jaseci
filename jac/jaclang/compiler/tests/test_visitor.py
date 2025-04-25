"""Tests for the 'visitor' keyword parsing in Jac."""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.absyntree import Module, Source, SpecialVarRef
from jaclang.compiler.parser import JacParser
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCaseMicroSuite


class TestVisitorKeyword(TestCaseMicroSuite):
    """Test Jac Parser specifically for the 'visitor' keyword."""

    def test_visitor_keyword_parses_like_here(self) -> None:
        """Test that the 'visitor' keyword parses identically to 'here'."""

        # Minimal Jac code using 'visitor'
        jac_code_visitor = """
        node A{
            has val:int =0;
        }

        edge a{
        }

        walker W1{
            can create with `root entry;
        }

        :walker:W1:can:create{
            One = A(5);
            Two = A(30);
            visitor +>:a:+> Two;
            One +>:a:+> A(10) +>:a:+> A(15);
            One +>:a:+> A(20) +>:a:+> A(25);
            Two +>:a:+> A(40) +>:a:+> A(50);
            visitor +>:a:+> One;

        }

        with entry{
            root spawn W1();
            print([root-->-->(`?A)]);
            print([root--> --> -->(`?A)]);
        }
        """
        # Minimal Jac code using 'here'
        jac_code_here = """
        node A{
            has val:int =0;
        }

        edge a{
        }

        walker W1{
            can create with `root entry;
        }

        :walker:W1:can:create{
            One = A(5);
            Two = A(30);
            here +>:a:+> Two;
            One +>:a:+> A(10) +>:a:+> A(15);
            One +>:a:+> A(20) +>:a:+> A(25);
            Two +>:a:+> A(40) +>:a:+> A(50);
            here +>:a:+> One;
        }

        with entry{
            root spawn W1();
            print([root-->-->(`?A)]);
            print([root--> --> -->(`?A)]);
        }
        """

        source_here = Source(jac_code_here, mod_path="here_test.jac")
        parser_here = JacParser(root_ir=source_here, prog=JacProgram())
        self.assertFalse(parser_here.errors_had, "Parser errors found for 'here' code.")
        ast_here: Module = parser_here.ir_out
        self.assertIsNotNone(ast_here, "AST for here code is None.")

        source_visitor = Source(jac_code_visitor, mod_path="visitor_test.jac")
        parser_visitor = JacParser(root_ir=source_visitor, prog=JacProgram())
        self.assertFalse(
            parser_visitor.errors_had, "Parser errors found for 'visitor' code."
        )
        ast_visitor: Module = parser_visitor.ir_out
        self.assertIsNotNone(ast_visitor, "AST for visitor code is None.")

        try:
            visitor_ability_def = next(
                item for item in ast_visitor.body if isinstance(item, ast.AbilityDef)
            )

            visitor_expr_stmt = visitor_ability_def.body.items[2]
            self.assertIsInstance(
                visitor_expr_stmt, ast.ExprStmt, "Expected ExprStmt for visitor line"
            )
            visitor_binary_expr = visitor_expr_stmt.expr
            self.assertIsInstance(
                visitor_binary_expr,
                ast.BinaryExpr,
                "Expected BinaryExpr for visitor line",
            )
            visitor_keyword_node = visitor_binary_expr.left
            self.assertIsInstance(
                visitor_keyword_node,
                SpecialVarRef,
                "LHS of visitor BinaryExpr is not SpecialVarRef",
            )

            here_ability_def = next(
                item for item in ast_here.body if isinstance(item, ast.AbilityDef)
            )

            here_expr_stmt = here_ability_def.body.items[2]
            self.assertIsInstance(
                here_expr_stmt, ast.ExprStmt, "Expected ExprStmt for here line"
            )

            here_binary_expr = here_expr_stmt.expr
            self.assertIsInstance(
                here_binary_expr, ast.BinaryExpr, "Expected BinaryExpr for here line"
            )

            here_keyword_node = here_binary_expr.left
            self.assertIsInstance(
                here_keyword_node,
                SpecialVarRef,
                "LHS of here BinaryExpr is not SpecialVarRef",
            )

            self.assertEqual(
                type(visitor_keyword_node),
                type(here_keyword_node),
                f"AST node types differ: "
                f"'visitor' produced {type(visitor_keyword_node).__name__}, "
                f"'here' produced {type(here_keyword_node).__name__}. "
                f"They should be the same.",
            )

            self.assertIsInstance(
                visitor_keyword_node,
                SpecialVarRef,
                f"Expected 'visitor' to produce a SpecialVarRef node, but got {type(visitor_keyword_node).__name__}",
            )
            self.assertIsInstance(
                here_keyword_node,
                SpecialVarRef,
                f"Expected 'here' to produce a SpecialVarRef node, but got {type(here_keyword_node).__name__}",
            )

        except (IndexError, AttributeError, StopIteration) as e:
            print(
                "\nAST for Visitor Code:\n", ast_visitor.pp() if ast_visitor else "None"
            )
            print("\nAST for Here Code:\n", ast_here.pp() if ast_here else "None")
            self.fail(
                f"Failed to navigate the AST structure to find 'visitor'/'here' nodes. "
                f"Check the assumed AST path in the test. Error: {e}"
            )
        except AssertionError as ae:
            print(
                "\nAST for Visitor Code:\n", ast_visitor.pp() if ast_visitor else "None"
            )
            print("\nAST for Here Code:\n", ast_here.pp() if ast_here else "None")
            self.fail(f"Assertion failed during AST navigation or check: {ae}")
