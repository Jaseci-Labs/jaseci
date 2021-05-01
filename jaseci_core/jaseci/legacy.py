"""
Legacy Master api function as a mixin should be Deprecated
"""


class master_legacy_api():
    def api_load_app(self, name: str, code: str):
        """
        Short for api_load_application
        """
        return self.api_load_application(name, code)

    def api_load_application(self, name: str, code: str):
        """
        Get or create then return application sentinel and graph pairing
        Code must be encoded in base64
        """
        snt = self.sentinel_ids.get_obj_by_name(name, True)
        gph = self.graph_ids.get_obj_by_name(name, True)
        if (not snt):
            self.api_create_sentinel(name)
            snt = self.sentinel_ids.get_obj_by_name(name)
        if (not gph):
            self.api_create_graph(name)
            gph = self.graph_ids.get_obj_by_name(name)
        self.api_set_jac_code(snt, code, True)
        return {'sentinel': snt.id.urn, 'graph': gph.id.urn,
                'active': snt.is_active}
