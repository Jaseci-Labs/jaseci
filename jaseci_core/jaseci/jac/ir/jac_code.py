"""
Mix in for jac code object in Jaseci
"""
import json
from jaseci.utils.utils import logger
from jaseci.jac.ir.ast_builder import JacAstBuilder
from jaseci.jac.ir.passes.schedule import multi_pass_optimizer
from jaseci.jac.ir.ast import Ast
import hashlib
from pathlib import Path
from os.path import dirname

from jaseci.jac.ir.passes.printer_pass import PrinterPass

# Used to check ir matches grammar of current Jaseci instance
grammar_hash = hashlib.md5(
    Path(dirname(__file__) + "/../jac.g4").read_text().encode()
).hexdigest()


class JacJsonEnc(json.JSONEncoder):
    """Custom Json encoder for Jac ASTs"""

    def default(self, obj):
        if isinstance(obj, Ast):
            retd = {}
            for i in obj.__dict__.keys():
                if not i.startswith("_"):
                    retd[i] = obj.__dict__[i]
            return retd
        return super().default(obj)


class JacJsonDec(json.JSONDecoder):
    """Custom hook for decoding Jac ASTs"""

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict) and "loc" in obj and "kid" in obj:
            ret = Ast(mod_name=obj["loc"][2])
            for i in obj.keys():
                setattr(ret, i, obj[i])
            return ret
        return obj


def jac_ast_to_ir(jac_ast: Ast):
    """Convert AST to IR string"""
    return json.dumps(cls=JacJsonEnc, obj={"gram_hash": grammar_hash, "ir": jac_ast})


def jac_ir_to_ast(ir: str):
    """Convert IR string to AST"""
    ir_load = json.loads(cls=JacJsonDec, s=ir)
    if (
        not isinstance(ir_load, dict)
        or "gram_hash" not in ir_load
        or ir_load["gram_hash"] != grammar_hash
        or (not isinstance(ir_load["ir"], Ast) and not ir_load["ir"] is None)
    ):
        logger.error(
            "Jac IR invalid or incompatible with current Jaseci "
            f"(valid gram_hash: {grammar_hash}!"
        )
    return ir_load["ir"]


class JacCode:
    """Obj mixin to code pickling"""

    def __init__(self, code_ir=None):
        self.is_active = False
        self.code_ir = None
        self.code_sig = None
        self._jac_ast = None
        self.errors = []
        self.apply_ir(code_ir)

    def reset(self):
        JacCode.__init__(self)

    def refresh(self):
        self._jac_ast = jac_ir_to_ast(self.code_ir) if self.code_ir else None
        if self._jac_ast:
            self.is_active = True
        else:
            self.is_active = False

    def apply_ir(self, ir):
        """Apply's IR to object"""
        self.code_ir = (
            ir.strip()
            if (isinstance(ir, str))
            else json.dumps(ir)
            if (isinstance(ir, dict))
            else jac_ast_to_ir(ir)
        )
        self.code_sig = hashlib.md5(self.code_ir.encode()).hexdigest()
        JacCode.refresh(self)  # should disregard overloaded versions

    def compile_jac(self, code, dir, start_rule="start", opt_level=4):
        """Generate AST tree from Jac code text"""
        tree = JacAstBuilder(
            jac_text=code, start_rule=start_rule, mod_name=self.name, mod_dir=dir
        )
        # Must clear this state across compiles (so fresh imports dont use stale data)
        JacAstBuilder._ast_head_map = {}

        self.errors = tree._parse_errors
        if tree._parse_errors:
            logger.error(str(f"{self.name}: Invalid syntax in Jac code!"))
            for i in tree._parse_errors:
                logger.error(i)
            return None

        multi_pass_optimizer(
            tree.root, opt_level=opt_level
        )  # run analysis and optimizers

        return tree.root

    def get_jac_ast(self):
        if not self._jac_ast:
            self.refresh()
        return self._jac_ast

    def print_ir(self, to_screen=True):
        irout = PrinterPass(ir=self.get_jac_ast(), to_screen=to_screen)
        irout.run()
        return irout.output

    def register(self, code, dir, opt_level=4):
        """
        Parses Jac code and saves IR
        """
        start_rule = "start" if self.j_type == "sentinel" else self.j_type
        tree = self.compile_jac(code, dir, start_rule=start_rule, opt_level=opt_level)

        if not tree:
            self.is_active = False
        else:
            self.apply_ir(tree)

        if not self.is_active:
            logger.error(str(f"{self.name}: Code not registered"))
        return self.is_active

    def ir_dict(self):
        """Return IR as dictionary"""
        return json.loads(self.code_ir)
