from jaseci.utils.test_core import CoreTest
from jaseci.jac.ir.passes.codegen_pass import CodeGenPass


class TestCodegen(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_walker_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("simple.jac")}],
        )
        CodeGenPass(self.mast.active_snt()._jac_ast).run()
