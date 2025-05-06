"""
Defines `JGenericType`, which represents a concrete instantiation of a generic
class or type constructor with specific type arguments in the Jac type system.

This allows modeling types like `List[int]`, `Dict[str, float]`, etc.,
where the generic logic is defined in the base `JClassType` and specialized
with type arguments at the call site.
"""

from jaclang.compiler.types import JType, JClassType, JClassMember


class JGenericType(JType):
    """
    Represents a generic type with concrete type arguments in the Jac type system.

    A `JGenericType` models the instantiation of a generic class with specific type arguments,
    such as `List[int]`, `Dict[str, float]`, or `Optional[MyClass]`.

    Attributes:
        base (JClassType): The generic class or type constructor.
        args (list[JType]): The type arguments applied to the generic.

    Behavior:
        - Delegates instantiability and member resolution to the base class.
        - Enforces assignability based on both the base type and type argument compatibility.
    """

    def __init__(self, base: JClassType, args: list[JType]):
        """
        Initializes a generic type instance with a given base and type arguments.

        Args:
            base (JClassType): The generic class type to instantiate.
            args (list[JType]): A list of concrete types used as arguments.

        Raises:
            AssertionError: If the base type's name is not a valid identifier.
        """
        assert base.name.isidentifier(), "Generic base must be a class-like type"
        self.base = base
        self.args = args
        name = f"{base.name}[{', '.join(arg.name for arg in args)}]"
        super().__init__(name=name, module=base.module)

    def is_instantiable(self) -> bool:
        """
        Returns whether this generic type can be instantiated.

        Delegates to the base class's instantiability.

        Returns:
            bool: True if instantiable; False otherwise.
        """
        return self.base.is_instantiable()

    def can_assign_from(self, other: JType) -> bool:
        """
        Checks whether a value of `other` can be assigned to this generic type.

        Assignment is allowed only if:
          - `other` is also a `JGenericType`,
          - the base types are compatible,
          - the type arguments match (via `can_assign_from`).

        Args:
            other (JType): The type being assigned.

        Returns:
            bool: True if assignable; False otherwise.
        """
        if not isinstance(other, JGenericType):
            return False
        if not self.base.can_assign_from(other.base):
            return False
        if len(self.args) != len(other.args):
            return False
        return all(a.can_assign_from(b) for a, b in zip(self.args, other.args))

    def get_members(self) -> dict[str, JClassMember]:
        """
        Returns the members accessible through this generic type.

        Currently delegates directly to the base type's members.
        Type argument substitution (e.g., replacing type variables with concrete types)
        may be added in the future.

        Returns:
            dict[str, JClassMember]: A mapping of member names to their definitions.
        """
        return self.base.get_members()
