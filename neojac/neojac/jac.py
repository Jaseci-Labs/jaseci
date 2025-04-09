import larkparse

comments: list[str] = []


def comment_callback(token: str) -> None:
    """
    Callback function to handle comment tokens.
    """
    comments.append(token)


with open("./examples/circle/circle_pure.jac") as f:
    jacfile = f.read()

parser = larkparse.Lark_StandAlone(lexer_callbacks={"COMMENT": comment_callback})
tree = parser.parse(jacfile)


print(tree)
