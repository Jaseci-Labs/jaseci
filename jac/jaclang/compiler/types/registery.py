import os
import json
from pathlib import Path
from typing import Dict
from jaclang.compiler.types import JClassType, JType


BUILTIN_PATH = Path(os.path.dirname(__file__)) / "builtins.json"

class JTypeRegistry:
    """
    Global registry for all user-defined and built-in types in the Jac type system.

    Types are indexed by their fully qualified name (e.g., 'builtins.int', 'mymod.MyClass').
    """

    def __init__(self) -> None:
        self._types: dict[str, JType] = {}
        self.__load_builtin_types()

    def register(self, type_obj: JClassType) -> None:
        """
        Register a type in the global registry.

        Args:
            type_obj (JType): The type to register.
        """
        self._types[type_obj.full_name] = type_obj

    def get(self, full_name: str) -> JType | None:
        """
        Retrieve a type by its fully qualified name.

        Args:
            full_name (str): The full name (e.g., 'builtins.str').

        Returns:
            JType | None: The registered type, or None if not found.
        """
        return self._types.get(full_name)

    def get_full_name(self, type_obj: JType) -> str:
        """
        Compute the fully qualified name for a type.

        Args:
            type_obj (JType): The type whose name to compute.

        Returns:
            str: Fully qualified name like 'builtins.int'.
        """
        mod = type_obj.module.name if type_obj.module else "unknown"
        return f"{mod}.{type_obj.name}"

    def all_types(self) -> list[JType]:
        return list(self._types.values())

    def __load_builtin_types(self) -> None:
        """
        Load built-in types into the registry.

        This method is called during initialization to ensure that all built-in types
        are available for type checking and other operations.
        """
        with open(BUILTIN_PATH, "r") as file:
            builtin_types = json.load(file)
            for type_name, type_info in builtin_types.items():
                class_type = JClassType(
                    name=type_name,
                    full_name=f"builtins.{type_name}",
                    module=None,
                    is_abstract=False,
                    instance_members={},
                    class_members={},
                )
                self.register(class_type)
