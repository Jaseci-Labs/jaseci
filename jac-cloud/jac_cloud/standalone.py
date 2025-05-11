"""Sample Runner."""

from os import getenv
from os.path import split
from pickle import load

from jac_cloud.jaseci.main import FastAPI

from jaclang import JacMachine as Jac
from jaclang.runtimelib.machine import JacMachineState

if not (filename := getenv("APP_PATH")):
    raise ValueError("APP_PATH is required")
base, mod = split(filename)
base = base if base else "./"
mod = mod[:-4]

FastAPI.enable()
mach = JacMachineState(base)
if filename.endswith(".jac"):
    Jac.jac_import(
        mach=mach,
        target=mod,
        base_path=base,
        override_name="__main__",
    )
elif filename.endswith(".jir"):
    with open(filename, "rb") as f:
        Jac.attach_program(mach, load(f))
        Jac.jac_import(
            mach=mach,
            target=mod,
            base_path=base,
            override_name="__main__",
        )
else:
    mach.close()
    raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

app = FastAPI.get()
