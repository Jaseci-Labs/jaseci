"""Test pass module."""

from jaclang.compiler.passes.main import CompilerMode as CMode
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class TestCFGBuildPass(TestCase):
    """Test FuseTypeInfoPass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_cfg_branches_and_loops(self) -> None:
        """Test basic blocks."""
        file_name = self.fixture_abs_path("cfg_gen.jac")

        from jaclang.compiler.passes.main.cfg_build_pass import CoalesceBBPass

        with open(file_name, "r") as f:
            file_source = f.read()

        ir = (prog := JacProgram()).compile_from_str(
            source_str=file_source, file_path=file_name, mode=CMode.COMPILE
        )

        cfg_pass = CoalesceBBPass(
            ir_in=ir,
            prog=prog,
        )

        dot = cfg_pass.dotgen_cfg()

        expected_dot = (
            "digraph G {\n"
            '  0 [label="BB0\\nx = 5 ;\\ny = 3 ;\\nif x > 3", shape=box];\n'
            '  1 [label="BB1\\nz = x + y ;", shape=box];\n'  # Note double backslash
            '  2 [label="BB2\\nelif x == 0", shape=box];\n'
            '  3 [label="BB3\\nz = y ;", shape=box];\n'
            '  4 [label="BB4\\nz = x - y ;", shape=box];\n'
            '  5 [label="BB5\\nfor i in range ( 0 , 10 )", shape=box];\n'
            '  6 [label="BB6\\nz = z + 1 ;", shape=box];\n'
            '  7 [label="BB7\\nwhile z < 10\\nz = z + 2 ;", shape=box];\n'
            '  8 [label="BB8\\nz = z + 2 ;", shape=box];\n'
            "  0 -> 1;\n"
            "  0 -> 2;\n"
            "  1 -> 5;\n"
            "  2 -> 3;\n"
            "  2 -> 4;\n"
            "  3 -> 5;\n"
            "  4 -> 5;\n"
            "  5 -> 6;\n"
            "  5 -> 7;\n"
            "  6 -> 5;\n"
            "  7 -> 7;\n"
            "  8 -> 7;\n"
            "}\n"
        )

        self.assertEqual(dot, expected_dot)

    def test_cfg_abilities_and_objects(self) -> None:
        """Test basic blocks."""
        file_name = self.fixture_abs_path("cfg_ability_test.jac")

        from jaclang.compiler.passes.main.cfg_build_pass import CoalesceBBPass

        with open(file_name, "r") as f:
            file_source = f.read()

        ir = (prog := JacProgram()).compile_from_str(
            source_str=file_source, file_path=file_name, mode=CMode.COMPILE
        )

        cfg_pass = CoalesceBBPass(
            ir_in=ir,
            prog=prog,
        )

        dot = cfg_pass.dotgen_cfg()

        expected_dot = (
            "digraph G {\n"
            '  0 [label="BB0\\nobj math_mod", shape=box];\n'
            '  1 [label="BB1\\ncan divide( x : int , y : int )\\nif y == 0", shape=box];\n'
            '  2 [label="BB2\\nreturn 0 ;", shape=box];\n'
            '  3 [label="BB3\\nreturn x / y ;", shape=box];\n'
            '  4 [label="BB4\\ncan multiply( x : int , y : int )\\nreturn x * y ;", shape=box];\n'
            '  5 [label="BB5\\nx = 5 ;\\ny = 0 ;\\nmath = math_mod ( ) ;\\nz = math . divide ( x , y ) '
            ';\\nprint ( z ) ;", shape=box];\n'
            "  0 -> 1;\n"
            "  0 -> 4;\n"
            "  1 -> 2;\n"
            "  1 -> 3;\n"
            "}\n"
        )

        self.assertEqual(dot, expected_dot)
