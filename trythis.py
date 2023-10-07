from typing import List, Union, Optional


class ASTNode:
    def __init__(self):
        self.parent: Optional[ASTNode] = None
        self.children: List[ASTNode] = []

    def add_child(self, child: "ASTNode"):
        self.children.append(child)
        child.parent = self


class Expression(ASTNode):
    pass


class Statement(ASTNode):
    pass


class Number(Expression):
    def __init__(self, value: float):
        super().__init__()
        self.value = value


class Identifier(Expression):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class BinaryOperation(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

        self.add_child(left)
        self.add_child(right)
        self.children = [left, right]


class Assignment(Statement):
    def __init__(self, variable: Identifier, value: Expression):
        super().__init__()
        self.variable = variable
        self.value = value

        self.add_child(variable)
        self.add_child(value)


class IfStatement(Statement):
    def __init__(
        self,
        condition: Expression,
        body: List[Statement],
        else_body: Optional[List[Statement]] = None,
    ):
        super().__init__()
        self.condition = condition
        self.body = body
        self.else_body = else_body

        self.add_child(condition)
        for stmt in body:
            self.add_child(stmt)
        if else_body:
            for stmt in else_body:
                self.add_child(stmt)


class ForLoop(Statement):
    def __init__(
        self, variable: Identifier, iterable: Expression, body: List[Statement]
    ):
        super().__init__()
        self.variable = variable
        self.iterable = iterable
        self.body = body

        self.add_child(variable)
        self.add_child(iterable)
        for stmt in body:
            self.add_child(stmt)


class FunctionDefinition(Statement):
    def __init__(self, name: str, params: List[Identifier], body: List[Statement]):
        super().__init__()
        self.name = name
        self.params = params
        self.body = body

        for param in params:
            self.add_child(param)
        for stmt in body:
            self.add_child(stmt)


class Call(Expression):
    def __init__(self, function: Identifier, arguments: List[Expression]):
        super().__init__()
        self.function = function
        self.arguments = arguments

        self.add_child(function)
        for arg in arguments:
            self.add_child(arg)
