"""Test pass module."""

from jaclang.compiler.passes.main.schedules import CompilerMode as CMode
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class TestFuseTypeInfo(TestCase):
    """Test FuseTypeInfoPass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_mod_type_assign(self) -> None:
        """Test module type assignment."""
        gen_ast = (
            JacProgram()
            .compile(
                self.fixture_abs_path("mod_type_assign.jac"),
                mode=CMode.TYPECHECK,
            )
            .pp()
        )
        type_info_list = [
            "kl - Type: types.ModuleType,  SymbolTable: blip",
            "l1 - Type: types.ModuleType,  SymbolTable: blip",
            "l2 - Type: types.ModuleType,  SymbolTable: blip",
        ]
        for type_info in type_info_list:
            self.assertIn(type_info, str(gen_ast))
