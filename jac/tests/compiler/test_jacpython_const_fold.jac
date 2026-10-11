"""Constant folding through the shipped Python compiler boundary."""
import from builtins { compile as pycompile, exec as pyexec }

test "unary plus on bool constants folds to int" {
    namespace: dict[str, any] = {};
    pyexec(
        pycompile(
            (
                "pos_false = +False\npos_true = +True\nneg = -False\n"
                "pos_false_is_int = not isinstance(+False, bool)\n"
            ),
            "fold_unary.py",
            "exec"
        ),
        namespace
    );
    assert namespace["pos_false_is_int"];
    # CPython folds +False to int 0, not False (PyNumber_Positive promotes).
    assert namespace["pos_false"] == 0;
    assert namespace["pos_false"] is not False;
    assert namespace["pos_true"] == 1;
    assert namespace["pos_true"] is not True;
    assert namespace["neg"] == 0;
}

test "bool bitwise ops keep bool results" {
    namespace: dict[str, any] = {};
    pyexec(
        pycompile(
            (
                "a = isinstance(True & True, bool) and (True & True) == True\n"
                "b = isinstance(False | True, bool) and (False | True) == True\n"
                "c = isinstance(True ^ True, bool) and (True ^ True) == False\n"
                "d = not isinstance(True & 1, bool) and True & 1 == 1\n"
            ),
            "fold_bool.py",
            "exec"
        ),
        namespace
    );
    assert namespace["a"];
    assert namespace["b"];
    assert namespace["c"];
    assert namespace["d"];
}

test "sequence repeat and concat fold to constant tuples" {
    namespace: dict[str, any] = {};
    pyexec(
        pycompile(
            "t = (1, 2) * 5\nu = (1, 2) + (3,)\ns = 'ab' * 3\nv = 3 * (1, 2)\n",
            "fold_seq.py",
            "exec"
        ),
        namespace
    );
    assert namespace["t"] == (1, 2, 1, 2, 1, 2, 1, 2, 1, 2);
    assert namespace["u"] == (1, 2, 3);
    assert namespace["s"] == "ababab";
    assert namespace["v"] == (1, 2, 1, 2, 1, 2);
}

test "class bodies read module globals with LOAD_NAME" {
    namespace: dict[str, any] = {};
    pyexec(
        pycompile(
            "x = 5\nclass C:\n    y = x + 1\n",
            "class_scope.py",
            "exec"
        ),
        namespace
    );
    assert namespace["C"].y == 6;
}
