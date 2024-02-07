from __future__ import annotations
from jaclang import jac_import as __jac_import__
from enum import Enum as __jac_Enum__, auto as __jac_auto__

__jac_import__(target="enumeration_bodies", base_path=__file__)
from enumeration_bodies import *
import enumeration_bodies


class Color(__jac_Enum__):
    RED = 1
    pencil = __jac_auto__()
    print("text")


print(Color.RED.value)
