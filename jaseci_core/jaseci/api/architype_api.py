"""
Architype api functions as a mixin
"""
from jaseci.api.interface import interface
from jaseci.actor.architype import architype
from jaseci.actor.sentinel import sentinel
from jaseci.utils.utils import b64decode_str


class architype_api:
    """Architype APIs for creating and managing Jaseci architypes

    The architype set of APIs allow for the addition and removing of
    architypes. Given a Jac implementation of an architype these APIs are
    designed for creating, compiling, and managing architypes that can be
    used by Jaseci. There are two ways to add an architype to Jaseci, either
    through the management of sentinels using the sentinel API, or by
    registering independent architypes with these architype APIs. These
    APIs are also used for inspecting and managing existing arichtypes that
    a Jaseci instance is aware of.
    """

    @interface.private_api(cli_args=["code"])
    def architype_register(
        self, code: str, encoded: bool = False, snt: sentinel = None
    ):
        """Create an architype based on the code passed and return object.

        This register API allows for the creation or replacement/update of
        an architype that can then be used by walkers in their interactions
        of graphs. The code argument takes Jac source code for the single
        architype. To load multiple architypes and walkers at the same time,
        use sentinel register API.

        Args:
            code (str): The text (or filename) for an architypes Jac code
            encoded (bool): True/False flag as to whether code is encode
                in base64
            snt (uuid): The UUID of the sentinel to be the owner of this
                architype

        Returns:
            json: Fields include
                'architype': Architype object if created otherwise null
                'success': True/False whether register was successful
                'errors': List of errors if register failed
                'response': Message on outcome of register call
        """
        ret = {"architype": None, "success": False, "errors": []}
        if encoded:
            code = b64decode_str(code)
        arch = snt.register_architype(code)
        if arch:
            self.extract_arch_aliases(snt, arch)
            ret["architype"] = arch.serialize()
            ret["success"] = True
            ret["response"] = f"Successfully created {arch.name} architype"
        else:
            ret["errors"] = snt.errors
            ret["response"] = "Errors occured"
        return ret

    @interface.private_api()
    def architype_get(
        self, arch: architype, mode: str = "default", detailed: bool = False
    ):
        """Get an architype rendered with specific mode

        Args:
            arch (uuid): The architype being accessed
            mode (str): Valid modes: {default, code, ir, }
            detailed (bool): Flag to give summary or complete set of fields

        Returns:
            json: Fields include (depends on mode)
                'code': Formal source code for architype
                'ir': Intermediate representation of architype
                'architype': Architype object print
        """
        if mode == "code":
            return {"code": arch._jac_ast.get_text()}
        elif mode == "ir":
            return {"ir": arch.ir_dict()}
        else:
            return {"architype": arch.serialize(detailed=detailed)}

    @interface.private_api(cli_args=["code"])
    def architype_set(self, arch: architype, code: str, mode: str = "default"):
        """Set code/ir for a architype

        Args:
            arch (uuid): The architype being set
            code (str): The text (or filename) for an architypes Jac code/ir
            mode (str): Valid modes: {default, code, ir, }

        Returns:
            json: Fields include (depends on mode)
                'success': True/False whether set was successful
                'errors': List of errors if set failed
                'response': Message on outcome of set call
        """
        if mode == "code" or mode == "default":
            arch.register(code)
        elif mode == "ir":
            arch.apply_ir(code)
        else:
            return {
                "response": f"Invalid mode to set {arch}",
                "success": False,
                "errors": [],
            }
        if arch.is_active:
            return {
                "response": f"{arch} registered and active!",
                "success": True,
                "errors": [],
            }
        else:
            return {
                "response": f"{arch} registered and active!",
                "success": True,
                "errors": arch.errors,
            }

    @interface.private_api()
    def architype_list(self, snt: sentinel = None, detailed: bool = False):
        """List architypes known to sentinel

        Args:
            snt (uuid): The sentinel for which to list its architypes
            detailed (bool): Flag to give summary or complete set of fields

        Returns:
            json: List of architype objects
        """
        archs = []
        for i in snt.arch_ids.obj_list():
            archs.append(i.serialize(detailed=detailed))
        return archs

    @interface.private_api(cli_args=["arch"])
    def architype_delete(self, arch: architype, snt: sentinel = None):
        """Permanently delete sentinel with given id

        Args:
            arch (uuid): The architype being set
            snt (uuid): The sentinel for which to list its architypes

        Returns:
            json: Fields include (depends on mode)
                'success': True/False whether command was successful
                'response': Message on outcome of command
        """

        if arch.jid not in snt.arch_ids:
            return {
                "response": f"Architype {arch} not in sentinel {snt}",
                "success": False,
            }
        self.remove_arch_aliases(snt, arch)
        archid = arch.jid
        snt.arch_ids.destroy_obj(arch)
        return {"response": f"Architype {archid} successfully deleted", "success": True}
