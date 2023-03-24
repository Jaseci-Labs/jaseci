"""
Jac tools api functions as a mixin
"""
from copy import deepcopy
import json
import os

from jaseci.extens.api.interface import Interface
from jaseci.jsorc.jsorc import JsOrc


class JacApi:
    """
    Jac tool APIs
    """

    @Interface.cli_api(cli_args=["file"])
    def jac_build(self, file: str, out: str = "", opt_level: int = 4):
        """
        Command line tooling for building executable jac ir
        """
        filename, dir = self.check_for_file(file)
        if not len(out):
            if file.endswith(".jac"):
                out = file.replace(".jac", ".jir")
            else:
                out = file + ".jir"
        faux = self.faux_master()
        with open(file, "r") as file:
            ret = faux.sentinel_register(
                code=file.read(),
                code_dir=dir,
                name=filename,
                auto_run="",
                opt_level=opt_level,
            )
            if "success" in ret and not ret["success"]:
                return ret
            with open(out, "w") as ofile:
                jir_out = json.dumps(
                    faux.sentinel_get(mode="ir", snt=faux.active_snt())
                )
                ofile.write(jir_out)
                ret = f"Build of {out} complete!"

                return ret

    @Interface.cli_api(cli_args=["file"])
    def jac_disas(self, file: str):
        """
        Command line tooling for print IR for both .jac code files
        and .jir executables
        """
        filename, dir = self.check_for_file(file)
        is_jir = file.endswith(".jir")
        faux = self.faux_master()
        with open(file, "r") as file:
            if is_jir:
                faux.sentinel_register(name=filename)
                ret = faux.sentinel_set(
                    snt=faux.active_snt(), code=file.read(), mode="ir"
                )
                faux.active_snt().print_ir()
            else:
                ret = faux.sentinel_register(
                    code=file.read(), code_dir=dir, name=filename, auto_run=""
                )
                faux.active_snt().print_ir()
            if "success" in ret and not ret["success"]:
                return ret

    @Interface.cli_api(cli_args=["file"])
    def jac_test(
        self,
        file: str,
        single: str = "",
        profiling: bool = False,
        detailed: bool = False,
    ):
        """
        Command line tooling for running all test in both .jac code files
        and .jir executables
        """
        filename, dir = self.check_for_file(file)
        is_jir = file.endswith(".jir")
        faux = self.faux_master()
        with open(file, "r") as file:
            if is_jir:
                faux.sentinel_register(name=filename)
                faux.sentinel_set(snt=faux.active_snt(), code=file.read(), mode="ir")
            else:
                ret = faux.sentinel_register(
                    code=file.read(), code_dir=dir, name=filename, auto_run=""
                )
                if "success" in ret and not ret["success"]:
                    return ret
        return faux.sentinel_test(
            snt=faux.active_snt(), single=single, profiling=profiling, detailed=detailed
        )

    @Interface.cli_api(cli_args=["file"])
    def jac_run(
        self, file: str, walk: str = "init", ctx: dict = {}, profiling: bool = False
    ):
        """
        Command line tooling for running all test in both .jac code files
        and .jir executables
        """
        filename, dir = self.check_for_file(file)
        is_jir = file.endswith(".jir")
        faux = self.faux_master()
        with open(file, "r") as file:
            if is_jir:
                faux.sentinel_register(name=filename)
                faux.sentinel_set(snt=faux.active_snt(), code=file.read(), mode="ir")
            else:
                ret = faux.sentinel_register(
                    code=file.read(), code_dir=dir, name=filename, auto_run=""
                )
                if "success" in ret and not ret["success"]:
                    return ret
        return faux.walker_run(
            name=walk,
            snt=faux.active_snt(),
            nd=faux.active_gph(),
            ctx=ctx,
            profiling=profiling,
        )

    @Interface.cli_api(cli_args=["file"])
    def jac_dot(
        self, file: str, walk: str = "init", ctx: dict = {}, detailed: bool = False
    ):
        """
        Command line tooling for a walker then output graph in both .jac code
        files and .jir executables
        """
        filename, dir = self.check_for_file(file)
        is_jir = file.endswith(".jir")
        faux = self.faux_master()
        with open(file, "r") as file:
            if is_jir:
                faux.sentinel_register(name=filename)
                faux.sentinel_set(snt=faux.active_snt(), code=file.read(), mode="ir")
            else:
                ret = faux.sentinel_register(
                    code=file.read(), name=filename, code_dir=dir, auto_run=""
                )
                if "success" in ret and not ret["success"]:
                    return ret
        faux.walker_run(
            name=walk,
            snt=faux.active_snt(),
            nd=faux.active_gph(),
            ctx=ctx,
            profiling=False,
        )
        return faux.graph_get(nd=faux.active_gph(), mode="dot", detailed=detailed)

    def faux_master(self):
        faux = JsOrc.super_master()
        faux._h.mem["global"] = deepcopy(self._h.mem["global"])
        return faux

    def check_for_file(self, file):
        if not os.path.isfile(file):
            ret = "File does not exsist!"
            return ret, ret
        filename = os.path.basename(file)
        dir = os.path.dirname(os.path.realpath(file))
        return filename, dir
