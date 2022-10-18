from jaseci.utils.test_core import CoreTest


class TestCodegen(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_simple_codegen(self):
        self.logger_on()
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("simple.jac")}],
        )
        # self.log(ret)
        ret = self.call(self.mast, ["walker_run", {"name": "most_basic"}])
        # self.log(ret)
        # from jaseci.jac.ir.passes import PrinterPass
        # PrinterPass(self.mast.active_snt()._jac_ast).run()
        self.assertEqual(ret["report"][0], 5004)
        self.assertEqual(ret["report"][1], 1)
        self.assertEqual(ret["report"][2], "ab")
        self.assertEqual(ret["report"][3], {"base": 5, "test": 5})
