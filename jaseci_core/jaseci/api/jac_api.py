"""
Jac tools api functions as a mixin
"""
from jaseci.api.interface import interface
import os
import json


class jac_api():
    """
    Jac tool APIs
    """
    @interface.cli_api(cli_args=['file'])
    def jac_build(self, file: str, out: str = ""):
        """
        Command line tooling for building executable jac ir
        """
        if(not os.path.isfile(file)):
            ret = "File does not exsist!"
            return ret
        if(not len(out)):
            if(file.endswith(".jac")):
                out = file.replace(".jac", ".jir")
            else:
                out = file+'.jir'
        faux = self.faux_master()
        with open(file, 'r') as file:
            faux.sentinel_register(code=file.read())
            with open(out, 'w') as ofile:
                jir_out = json.dumps(
                    faux.sentinel_get(mode='ir',
                                      snt=faux.active_snt()))
                ofile.write(jir_out)
                ret = f"Build of {out} complete!"

                return ret

    @interface.cli_api(cli_args=['file'])
    def jac_test(self, file: str, detailed: bool = False):
        """
        Command line tooling for running all test in both .jac code files
        and .jir executables
        """
        if(not os.path.isfile(file)):
            ret = "File does not exsist!"
            return ret
        is_jir = file.endswith(".jir")
        faux = self.faux_master()
        with open(file, 'r') as file:
            if(is_jir):
                faux.sentinel_register()
                faux.sentinel_set(snt=faux.active_snt(),
                                  code=file.read(), mode='ir')
            else:
                faux.sentinel_register(code=file.read())
        return faux.sentinel_test(snt=faux.active_snt(), detailed=detailed)

    @interface.cli_api(cli_args=['file'])
    def jac_run(self, file: str, walk: str = 'init', ctx: dict = {},
                profiling: bool = False):
        """
        Command line tooling for running all test in both .jac code files
        and .jir executables
        """
        if(not os.path.isfile(file)):
            ret = "File does not exsist!"
            return ret
        is_jir = file.endswith(".jir")
        faux = self.faux_master()
        with open(file, 'r') as file:
            if(is_jir):
                faux.sentinel_register()
                faux.sentinel_set(snt=faux.active_snt(),
                                  code=file.read(), mode='ir')
            else:
                faux.sentinel_register(code=file.read(), auto_run='')
        return faux.walker_run(name=walk, snt=faux.active_snt(),
                               nd=faux.active_gph(), ctx=ctx,
                               profiling=profiling)

    def faux_master(self):
        from jaseci.element.super_master import super_master
        from jaseci.utils.mem_hook import mem_hook
        return super_master(h=mem_hook())
