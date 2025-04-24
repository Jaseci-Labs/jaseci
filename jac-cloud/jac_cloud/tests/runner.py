"""Sample Runner."""

from os.path import split
from pickle import load

from jac_cloud import FastAPI

from jaclang import jac_import
from jaclang.runtimelib.machinestate import ExecutionContext, JacMachineState

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
        JacMachineState(base).attach_program(load(f))
        jac_import(
            target=mod,
            base_path=base,
            cachable=True,
            override_name="__main__",
        )
else:
    jctx.close()
    raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

app = FastAPI.get()

jctx.close()
