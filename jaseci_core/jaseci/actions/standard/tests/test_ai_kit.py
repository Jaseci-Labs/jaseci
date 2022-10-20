from jaseci.utils.test_core import CoreTest
from jaseci.actions.live_actions import load_module_actions


class AI_Kit_Test(CoreTest):
    fixture_src = __file__

    def test_actions_load(self):
        ret = load_module_actions("jaseci_ai_kit.use_enc")
        self.assertEqual(ret, True)

    def test_ai_kit(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("ai_kit.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "use_encoder"}])
        self.assertEqual(len(ret["report"][0][0]), 512)
