"""
App api functions as a mixin
"""


class app_api():
    """
    App APIs
    """

    def api_app_load(self, name: str, code: str, encoded: bool = False):
        """
        Get or create then return application sentinel and graph pairing
        Code must be encoded in base64
        """
        snt = self.sentinel_ids.get_obj_by_name(name, True)
        gph = self.graph_ids.get_obj_by_name(name, True)
        if (not snt):
            self.api_sentinel_create(name)
            snt = self.sentinel_ids.get_obj_by_name(name)
        if (not gph):
            self.api_create_graph(name)
            gph = self.graph_ids.get_obj_by_name(name)
        self.api_sentinel_code_set(code=code, snt=snt, encoded=encoded)
        return {'sentinel': snt.id.urn, 'graph': gph.id.urn,
                'active': snt.is_active}
