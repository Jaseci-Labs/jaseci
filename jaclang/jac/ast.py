"""Abstract class for IR Passes for Jac."""
import pprint


class AstNode:
    """Abstract syntax tree node for Jac."""

    def __init__(self: "AstNode", parent: "AstNode", kid: list, line: int) -> None:
        """Initialize ast."""
        self.parent = parent
        self.kid = kid if kid else []
        self.line = line

    def __str__(self: "AstNode") -> str:
        """Return string representation of node."""
        return f"{str(type(self).__name__)}->[{self.line},{len(self.kid)} kids]"

    def __repr__(self: "AstNode") -> str:
        """Return string representation of node."""
        return str(self)

    def to_dict(self: "AstNode") -> dict:
        """Return dict representation of node."""
        return {
            "node": str(type(self).__name__),
            "kid": [x.to_dict() for x in self.kid],
            "line": self.line,
        }

    def print(self: "AstNode", depth: int = None) -> None:
        """Print ast."""
        pprint.PrettyPrinter(depth=depth).pprint(self.to_dict())


class Token(AstNode):
    """Token node type for Jac Ast."""

    def __init__(
        self: "Token", name: str, value: str, *args: list, **kwargs: dict
    ) -> None:
        """Initialize token."""
        self.name = name
        self.value = value
        super().__init__(*args, **kwargs)


class Parse(AstNode):
    """Parse node type for Jac Ast."""

    def __init__(self: "Parse", name: str, *args: list, **kwargs: dict) -> None:
        """Initialize parse."""
        self.name = name
        super().__init__(*args, **kwargs)


class WholeBuild(AstNode):
    """Whole Program node type for Jac Ast."""

    def __init__(
        self: "WholeBuild", elements: list, *args: list, **kwargs: dict
    ) -> None:
        """Initialize whole program node."""
        self.elements = elements
        super().__init__(*args, **kwargs)


class DocString(AstNode):
    """DocString node type for Jac Ast."""

    def __init__(
        self: "DocString", value: AstNode, *args: list, **kwargs: dict
    ) -> None:
        """Initialize docstring node."""
        self.value = value
        super().__init__(*args, **kwargs)


class GlobalVars(AstNode):
    """GlobalVars node type for Jac Ast."""

    def __init__(self: "GlobalVars", values: list, *args: list, **kwargs: dict) -> None:
        """Initialize global var node."""
        self.values = values
        super().__init__(*args, **kwargs)


class NamedAssign(AstNode):
    """NamedAssign node type for Jac Ast."""

    def __init__(
        self: "NamedAssign", name: AstNode, value: AstNode, *args: list, **kwargs: dict
    ) -> None:
        """Initialize named assign node."""
        self.name = name
        self.value = value
        super().__init__(*args, **kwargs)


class Test(AstNode):
    """Test node type for Jac Ast."""

    def __init__(
        self: "Test",
        name: AstNode,
        description: AstNode,
        body: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize test node."""
        self.name = name
        self.description = description
        self.body = body
        super().__init__(*args, **kwargs)


class Import(AstNode):
    """Import node type for Jac Ast."""

    def __init__(
        self: "Import",
        lang: AstNode,
        path: AstNode,
        alias: AstNode,
        items: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize import node."""
        self.lang = lang
        self.path = path
        self.alias = alias
        self.items = items
        super().__init__(*args, **kwargs)


class ModulePath(AstNode):
    """ModulePath node type for Jac Ast."""

    def __init__(self: "ModulePath", path: list, *args: list, **kwargs: dict) -> None:
        """Initialize module path node."""
        self.path = path
        super().__init__(*args, **kwargs)


class ModuleItem(AstNode):
    """ModuleItem node type for Jac Ast."""

    def __init__(
        self: "ModuleItem", name: AstNode, alias: AstNode, *args: list, **kwargs: dict
    ) -> None:
        """Initialize module item node."""
        self.name = name
        self.alias = alias
        super().__init__(*args, **kwargs)


class NodeArch(AstNode):
    """NodeArch node type for Jac Ast."""

    def __init__(
        self: "NodeArch",
        name: AstNode,
        base_classes: AstNode,
        body: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize node arch node."""
        self.name = name
        self.base_classes = base_classes
        self.body = body
        super().__init__(*args, **kwargs)


class EdgeArch(AstNode):
    """EdgeArch node type for Jac Ast."""

    def __init__(
        self: "EdgeArch",
        name: AstNode,
        base_classes: AstNode,
        body: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize edge arch node."""
        self.name = name
        self.base_classes = base_classes
        self.body = body
        super().__init__(*args, **kwargs)


class ObjectArch(AstNode):
    """ObjectArch node type for Jac Ast."""

    def __init__(
        self: "ObjectArch",
        name: AstNode,
        base_classes: AstNode,
        body: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.base_classes = base_classes
        self.body = body
        super().__init__(*args, **kwargs)


class WalkerArch(AstNode):
    """WalkerArch node type for Jac Ast."""

    def __init__(
        self: "WalkerArch",
        name: AstNode,
        base_classes: AstNode,
        body: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize walker arch node."""
        self.name = name
        self.base_classes = base_classes
        self.body = body
        super().__init__(*args, **kwargs)


class SpawnerArch(AstNode):
    """SpawnerArch node type for Jac Ast."""

    def __init__(
        self: "SpawnerArch",
        name: AstNode,
        body: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize spawner arch node."""
        self.name = name
        self.body = body
        super().__init__(*args, **kwargs)


class BaseClasses(AstNode):
    """BaseArch node type for Jac Ast."""

    def __init__(
        self: "BaseClasses", base_classes: list, *args: list, **kwargs: dict
    ) -> None:
        """Initialize base classes node."""
        self.base_classes = base_classes
        super().__init__(*args, **kwargs)


class AbilitySpec(AstNode):
    """ArchBlock node type for Jac Ast."""

    def __init__(
        self: "ArchBlock",
        name: AstNode,
        arch: AstNode,
        mod: AstNode,
        signature: AstNode,
        body: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize arch block node."""
        self.name = name
        self.arch = arch
        self.mod = mod
        self.signature = signature
        self.body = body
        super().__init__(*args, **kwargs)


class ArchBlock(AstNode):
    """ArchBlock node type for Jac Ast."""

    def __init__(
        self: "ArchBlock",
        body: AstNode,
        *args: list,
        **kwargs: dict,
    ) -> None:
        """Initialize arch block node."""
        self.body = body
        super().__init__(*args, **kwargs)
