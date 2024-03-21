"""Workspace file ."""

# from __future__ import annotations
# from jaclang.plugin.feature import JacFeature as _Jac
# from jaclang.plugin.builtin import *
# from dataclasses import dataclass as __jac_dataclass__
# from icecream import ic


# # @_Jac.make_obj(on_entry=[], on_exit=[])
# # @__jac_dataclass__(eq=False)
# class model:

#     def __infer__(self, meaning_in: str, **kwargs: dict) -> None:
#         return "The calculated age is 145"


# llm = model()
# theresa: list[str, str] = ["Mother Theresa", "1910-08-26"]

# module_registry = {
#     "aott_raise(Module)": {
#         "model": ["obj", ""],
#         "llm": [None, ""],
#         "theresa": ["list[str,str]", "mother theresa"],
#         "Person": ["obj", "Person"],
#         "Einstein": [None, ""],
#         "age": [None, ""],
#         "": [None, ""],
#         "emoji_examples": ["list[dict[str,str]]", "Examples of Text to Emoji"],
#     },
#     "aott_raise(Module).Person(obj)": {
#         "name": ["str", "Name"],
#         "dob": ["str", "Date of Birth"],
#         "age": ["int", "Age"],
#     },
# }


# def get_semstring(var, scope) -> str:
#     for i_scope in [scope, scope.split(".")[0]]:
#         if var in module_registry[i_scope]:
#             return module_registry[i_scope][var][1]


# from typing import Any


# def get_type_annotation(data: Any) -> str:
#     # Check if the input is a dictionary
#     if isinstance(data, dict):
#         # Get the class name of the first non-None value in the dictionary
#         class_name = next(
#             (value.__class__.__name__ for value in data.values() if value is not None),
#             None,
#         )

#         if class_name:
#             return f"dict[str, {class_name}]"
#         else:
#             return "dict[str, Any]"
#     # If the input is not a dictionary, return its type
#     else:
#         return type(data).__name__


# def get_object_string(obj):
#     if isinstance(obj, str):
#         return f'"{obj}"'
#     elif isinstance(obj, (int, float, bool)):
#         return str(obj)
#     elif isinstance(obj, list):
#         return "[" + ", ".join(get_object_string(item) for item in obj) + "]"
#     elif isinstance(obj, tuple):
#         return "(" + ", ".join(get_object_string(item) for item in obj) + ")"
#     elif isinstance(obj, dict):
#         return (
#             "{"
#             + ", ".join(
#                 f"{get_object_string(key)}: {get_object_string(value)}"
#                 for key, value in obj.items()
#             )
#             + "}"
#         )
#     elif hasattr(obj, "__dict__"):
#         args = ", ".join(
#             f"{key}={get_object_string(value)}" for key, value in vars(obj).items()
#         )
#         return f"{obj.__class__.__name__}({args})"
#     else:
#         return str(obj)


# def get_variable_name(var):
#     """
#     Returns the name of a variable.

#     Args:
#         var (any): The variable whose name needs to be retrieved.

#     Returns:
#         str: The name of the variable.
#     """
#     # Get the global and local variable names
#     global_names = list(globals().keys())
#     local_names = list(locals().keys())

#     # Check if the variable is in the global scope
#     for name in global_names:
#         if id(globals()[name]) == id(var):
#             return name

#     # Check if the variable is in the local scope
#     for name in local_names:
#         if id(locals()[name]) == id(var):
#             return name

#     # If the variable was not found, return None
#     return None


# def with_llm(
#     model: model,
#     model_params: dict,
#     scope: str,
#     incl_info: list[tuple],
#     excl_info: list[tuple],
#     inputs: list[tuple],
#     outputs: tuple,
#     action: str,
# ) -> int:
#     ic(model, model_params, scope, incl_info, excl_info, inputs, outputs, action)
#     included_info = []
#     for var_name, i in incl_info:
#         type_ann = get_type_annotation(i)
#         obj_val_str = get_object_string(i)
#         if hasattr(i, "__dict__"):
#             semstr = get_semstring(type_ann, scope)
#             var_name = get_variable_name(i)
#         else:
#             semstr = get_semstring(var_name, scope)
#         included_info.append((semstr, type_ann, var_name, obj_val_str))
#     for info in included_info:
#         semstr, type_ann, var_name, obj_val_str = info
#         print(f"{semstr} ({type_ann}) {var_name} = {obj_val_str}")


# # @_Jac.make_obj(on_entry=[], on_exit=[])
# @__jac_dataclass__(eq=False)
# class Person:
#     name: str
#     dob: str
#     age: int = None

#     def calculate(self, cur_year: int) -> int:
#         return with_llm(
#             model=llm,
#             model_params={"temperature": 0.7, "reason": True},
#             scope="aott_raise(Module).Person(obj)",
#             incl_info=[
#                 ("self", self),
#                 ("name", self.name),
#                 ("dob", self.dob),
#                 ("theresa", theresa),
#             ],
#             excl_info=[],
#             inputs=[("Current Year", int, "cur_year", cur_year)],
#             outputs=("Calculated Age", int),
#             action="Calculate the Age of a Person",
#         )


# Einstein = Person(name="Einstein", dob="1879-03-14")
# age = Einstein.calculate(cur_year=2024)
# Einstein.age = age
# print(Einstein.age)


# emoji_examples = [
#     {"input": "I love football", "output": "â\x9a½"},
#     {"input": "Lets eat pizza", "output": "ð\x9f\x8d\x95"},
# ]


# def get_emoji(input: str) -> str:
#     return with_llm(
#         model=llm,
#         model_params={},
#         scope="aott_raise(Module)",
#         incl_info=[("emoji_examples", emoji_examples)],
#         excl_info=[],
#         inputs=[("Input", str, "input", input)],
#         outputs=("Emoji Representation", str),
#         action="Get Emoji Representation",
#     )


# print(get_emoji("Lets move to paris"))
