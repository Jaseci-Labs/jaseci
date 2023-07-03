"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such production Jac program.
"""

import:py inspect;
import:py argparse;
import:py cmd;

object Command {
    has func: callable,
        sig: inspect.Signature;

    can:priv init(func: callable) {
        <h>.func = func;
        <h>.sig = func |> inspect.signature;
    }

    can call(*args: list, **kwargs: dict) {
        {*args, **kwargs} |> <h>.func;
    }
}

