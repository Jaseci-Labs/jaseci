"""Test pass module."""

from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main.fuse_typeinfo_pass import FuseTypeInfoPass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.utils.test import TestCase


class TestFuseTypeInfo(TestCase):
    """Test FuseTypeInfoPass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_mod_type_assign(self) -> None:
        """Test module type assignment."""
        gen_ast = jac_file_to_pass(
            self.fixture_abs_path("mod_type_assign.jac"),
            FuseTypeInfoPass,
            schedule=py_code_gen_typed,
        ).ir.pp()
        type_info_list = [
            "kl - Type: types.ModuleType,  SymbolTable: blip",
            "l1 - Type: types.ModuleType,  SymbolTable: blip",
            "l2 - Type: types.ModuleType,  SymbolTable: blip",
        ]
        for type_info in type_info_list:
            self.assertIn(type_info, str(gen_ast))
