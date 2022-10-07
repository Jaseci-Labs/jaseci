"""
AST for Jac
"""
from jaseci.utils.utils import logger


class Ast:
    """
    AST Nodes
    """

    def __init__(
        self,
        mod_name,
    ):
        self.name = "unparsed"
        self.context = {}
        self.kid = []
        self.loc = [0, 0, mod_name if mod_name is not None else "@default"]

    def is_terminal(self):
        """Returns true if node is a terminal"""
        return len(self.context.keys())

    def token(self):
        if not self.is_terminal():
            logger.error(str(f"Non terminals (rules) don't have token info - {self}"))
            return None
        else:
            return self.context["token"]

    def token_text(self):
        if self.is_terminal():
            return self.token()["text"]

    def token_symbol(self):
        if self.is_terminal():
            return self.token()["symbol"]

    def __str__(self):
        res = f"{self.name}:{self.loc[2]}:{self.loc[0]}:{self.loc[1]}:"
        if self.is_terminal():
            res += f':{self.context["token"]["text"]}'
        return res

    def __repr__(self):
        return self.__str__()

    def get_tokens(self):
        """Return list of all tokens derived from this ast node"""
        tokens = []
        if "token" in self.context:
            tokens.append(self.context["token"])
            return tokens
        else:
            for i in self.kid:
                tokens = tokens + i.get_tokens()
        return tokens

    def get_text(self):
        """Get source text for this node"""
        ret = ""
        for i in self.get_tokens():
            ret += f"{i['text']} "
        return ret
