"""A `for` whose tuple target rebinds a name the function already holds with
another type (`for (side, sign) in ...` after `for (name, side) in ...`)
gets a slot of its own natively, as a plain loop target does, instead of
the native backend failing with "cannot store i8* to double*" and sending
the function to Python. Identity with the Python backend also proves the
native path was taken."""
import from pathlib { Path }
import from tests.support { assert_native_identity }

test "tuple loop targets that rebind a name to another type agree with Python" {
    source = str(
        Path(__file__).resolve().parent / "fixtures" / "unpack_target_rebinds.jac"
    );
    # The headerless (nogc) profile refuses a tuple holding a string in a
    # list literal outright (E1406), so it is left out.
    out = assert_native_identity(source, profiles=["managed", "rc"]);
    lines = out.splitlines();
    assert lines[0] == "[-2.5, 3.0]" , out;
    assert lines[1] == "25" , out;
    assert lines[2] == "18.5" , out;
}
