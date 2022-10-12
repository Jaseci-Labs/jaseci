from jaseci.utils.test_core import CoreTest
from jaseci.jac.ir.passes.codegen_pass import CodeGenPass
from jaseci.jac.jsci_vm.machine import BytecodeMachine
from jaseci.jac.jsci_vm.disasm import DisAsm


class TestCodegen(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_walker_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("simple.jac")}],
        )
        bc_ir = CodeGenPass(self.mast.active_snt()._jac_ast).run()
        DisAsm().disassemble(bc_ir.bytecode)
        BytecodeMachine().run(bc_ir.bytecode)
