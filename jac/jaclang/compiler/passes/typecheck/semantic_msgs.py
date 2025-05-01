"""Jac semantic messages."""

from enum import Enum


class JacSemanticMessages(Enum):
    """Messages enum for jac semantic analysis."""

    # Abilities semantics
    MISSING_RETURN_STATEMENT = "Missing return statement"
    RETURN_FOR_NONE_ABILITY = (
        "Ability has a return type however it's defined as None type"
    )
    CONFLICTING_RETURN_TYPE = "Ability have a return type {actual_return_type} but got assigned a type {formal_return_type}"  # noqa E501

    # Ability calls semantics
    POSITIONAL_ARG_AFTER_KWARG = "Can't use positional argument after kwargs"
    ARG_NAME_NOT_FOUND = "No argument named '{param_name}' in function '{arg_name}()'"
    REPEATED_ARG = "'{param_name}' argument is repeated"
    CONFLICTING_ARG_TYPE = "Error: Can't assign a value {actual_type} to a parameter '{param_name}' of type {formal_type}"  # noqa E501
    PARAM_NUMBER_MISMATCH = (
        "Required number of params {actual_number}, passed number is {passed_number}"
    )
    UNDEFINED_FUNCTION_NAME = "No function called {func_name} available"

    # Var Declarations
    VAR_REDEFINITION = "Can't redefine {var_name} to be {new_type}"
    CONFLICTING_VAR_TYPE = (
        "Error: Can't assign a value {val_type} to a {var_type} object"
    )
    ASSIGN_TO_RTYPE = "Expression '{expr}' can't be assigned (not a valid ltype)"

    # Misc.
    UNSUPPORTED_TYPE_ANNOTATION = (
        "Type annotations is not supported for '{expr}' expression"
    )
