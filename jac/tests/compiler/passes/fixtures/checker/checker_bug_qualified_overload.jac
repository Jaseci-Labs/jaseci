"""Regression fixture: overload stubs spelled through a module (`@typing.overload`, or an
alias such as `@t.overload`) are not duplicate methods, exactly like a bare `@overload`.
"""
import typing;
import typing as t;

obj Keys {
    @typing.overload
    def get(name: int) -> int;

    @typing.overload
    def get(name: str) -> str;

    def get(name: int | str) -> int | str {
        return name;
    }

    @t.overload
    def op(kind: int) -> int;

    @t.overload
    def op(kind: str) -> str;

    def op(kind: int | str) -> int | str {
        return kind;
    }
}
