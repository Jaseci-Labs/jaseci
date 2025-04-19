"""Sample Runner."""

from os.path import split
from pickle import load

from jac_cloud import FastAPI

from jaclang import jac_import
from jaclang.runtimelib.context import ExecutionContext
from jaclang.runtimelib.machine import JacMachine, JacProgram

filename = "./jac_cloud/tests/websocket.jac"
base, mod = split(filename)
base = base if base else "./"
mod = mod[:-4]

FastAPI.enable()
jctx = ExecutionContext.create()

if filename.endswith(".jac"):
    jac_import(
        target=mod,
        base_path=base,
        cachable=True,
        override_name="__main__",
    )
elif filename.endswith(".jir"):
    with open(filename, "rb") as f:
        JacMachine(base).attach_program(JacProgram(mod_bundle=load(f), bytecode=None))
        jac_import(
            target=mod,
            base_path=base,
            cachable=True,
            override_name="__main__",
        )
else:
    jctx.close()
    JacMachine.detach_machine()
    raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

app = FastAPI.get()

jctx.close()
JacMachine.detach_machine()
