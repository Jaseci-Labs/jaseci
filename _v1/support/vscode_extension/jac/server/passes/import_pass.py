from jaseci.jac.ir.passes import IrPass


class ImportPass(IrPass):
    """Resolves symbols from the imports in an ast"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # {doc_uri: [{name: str, type: str}]}
        import_table = {}

    def enter_node(self, node):
        if node.name == "import_module":
            try:
                if node.kid[5].name == "STRING":
                    import_path = node.kid[5].token()["text"]
            except IndexError:
                pass
