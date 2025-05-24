from jaclang.compiler.jtyping.types.jtype import JType

class JTypeVar(JType):
    _id_counter = 0

    def __init__(self, name: str):
        if name is None:
            name = f"T{JTypeVar._id_counter}"
            JTypeVar._id_counter += 1
        self.name = name
        self.resolved: JType | None = None  # after unification

    def __repr__(self):
        if self.resolved:
            return f"{self.name}={self.resolved}"
        return f"TypeVar[{self.name}]"
    
    def is_instantiable(self) -> bool:
        """
        Indicates whether the type can be directly instantiated at runtime.

        For example, abstract classes or interfaces would return False,
        while concrete classes and primitives would return True.

        Returns:
            bool: True if instantiable, False otherwise.
        """
        return False

    def get_members(self) -> dict:
        """
        Returns the accessible members of the type (e.g., methods, fields, properties).

        This is used to validate member access like `obj.foo` or to inspect operator support.

        Returns:
            dict: A dictionary mapping member names to JClassMember objects (or equivalent).
        """
        return {}
    
    def supports_binary_op(self, op: str) -> bool:
        """
        Checks whether a binary operator is supported by this type.

        The operator is internally mapped to its corresponding magic method (e.g., '+' to '__add__').
        The type is considered to support the operator if the corresponding method is present
        in its member list.

        Args:
            op (str): The operator symbol (e.g., '+', '*', '==').

        Returns:
            bool: True if the operator is supported; False otherwise.
        """
        return False