"""A class whose base is `Protocol[...]` is a protocol: a class with the members
conforms to it structurally. `AbstractContextManager[_T_co, _ExitT_co]` and
`os.PathLike[AnyStr_co]` are declared `(ABC, Protocol[...])` in typeshed."""

import contextlib;
import os;
import from unittest.mock { patch }

obj Session {
    def __enter__ -> int {
        return 1;
    }

    def __exit__(kind: object, value: object, trace: object) -> None {
        return None;
    }
}

obj Location {
    def __fspath__ -> str {
        return "/tmp";
    }
}

obj NoExit {
    def __enter__ -> int {
        return 1;
    }
}

def manage(path: str) -> int {
    stack = contextlib.ExitStack();
    stack.enter_context(patch.object(os, "getcwd", return_value="/x"));
    stack.enter_context(open(path));
    entered: int = stack.enter_context(Session());
    where: os.PathLike[str] = Location();
    wrong: str = stack.enter_context(Session());
    stack.enter_context(NoExit());
    stack.close();
    return entered + len(os.fspath(where)) + len(wrong);
}
