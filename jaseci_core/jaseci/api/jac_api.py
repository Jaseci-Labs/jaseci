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
    @interface.cli_api
    def jac_build(self, input: str, output: str = ""):
        """
        Command line tooling for building executable jac ir
        """
        if(not os.path.isfile(input)):
            return "File does not exsist!"
        if(not len(output)):
            if(input.endswith(".jac")):
                output = input.replace(".jac", ".jir")
            else:
                output = input+'.jir'
        faux = self.faux_master()
        with open(input, 'r') as file:
            faux.sentinel_register(code=file.read())
            with open(output, 'w') as ofile:
                out = json.dumps(
                    faux.sentinel_get(mode='ir',
                                      snt=faux.active_snt()))
                ofile.write(out)
                return f"Build of {output} complete!"

    @interface.cli_api
    def jac_test(self, file: str, detailed=False):
        pass

    @interface.cli_api
    def jac_run(self, file: str):
        pass

    def faux_master(self):
        from jaseci.element.super_master import super_master
        from jaseci.utils.mem_hook import mem_hook
        return super_master(h=mem_hook())
