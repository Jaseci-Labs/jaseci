"""Test pass module."""

from jaclang.compiler.passes.main.fuse_typeinfo_pass import FuseTypeInfoPass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class TestFuseTypeInfo(TestCase):
    """Test FuseTypeInfoPass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_mod_type_assign(self) -> None:
        """Test module type assignment."""
        prog = JacProgram(main_file=self.fixture_abs_path("mod_type_assign.jac"))
        prog.jac_file_to_pass(
            target=FuseTypeInfoPass,
            schedule=py_code_gen_typed,
        )
        gen_ast = prog.modules[self.fixture_abs_path("mod_type_assign.jac")].pp()
        type_info_list = [
            "kl - Type: types.ModuleType,  SymbolTable: blip",
            "l1 - Type: types.ModuleType,  SymbolTable: blip",
            "l2 - Type: types.ModuleType,  SymbolTable: blip",
        ]
        for type_info in type_info_list:
            self.assertIn(type_info, str(gen_ast))
