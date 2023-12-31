from jaclang import jac_import
import os
from math import sqrt as square_root
import datetime as dt

jac_import(target="base_module_structure", base_path=__file__)
from base_module_structure import add, subtract

for i in range(int(square_root(dt.datetime.now().year))):
    print(os.getcwd(), add(i, subtract(i, 1)))
