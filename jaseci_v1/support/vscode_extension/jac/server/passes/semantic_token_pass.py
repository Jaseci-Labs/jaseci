from lsprotocol.types import SemanticTokenTypes
from jaseci.jac.ir.passes import IrPass


class SemanticTokenPass(IrPass):
    """Processes the ast to generate semantic tokens"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # {doc_uri: [{name: str, type: str}]}
        self.tokens = []
        self.last_line = 0
        self.last_col = 0

    def add_token(
        self,
        line: int,
        col: int,
        length: int,
        token_type: SemanticTokenTypes,
    ):
        self.tokens.extend(
            [
                token_type,
                0,
            ]
        )

    def process_keyword(self, node):
        if node.name in [
            "KW_EDGE",
            "KW_WALKER",
            "KW_REPORT",
            "KW_ASYNC",
            "KW_TRY",
            "KW_REPORT",
            "KW_GRAPH",
            "KW_DISENGAGE",
        ]:
            self.add_token(
                node.loc[0] - self.last_line - 1,
                node.loc[1] - self.last_col,
                len(node.token()["text"]),
                SemanticTokenTypes.Keyword,
            )

            self.last_line = node.loc[0]
            self.last_col = node.loc[1]

    def enter_node(self, node):
        self.process_keyword(node)
