from jaclang import jac_import as __jac_import__
import os
import datetime as dt
from math import sqrt as square_root, log

(add, subtract) = __jac_import__(
    target="base_module_structure",
    base_path=__file__,
    items={"add": None, "subtract": None},
)

for i in range(int(square_root(dt.datetime.now().year))):
    print(os.getcwd(), add(i, subtract(i, 1)), int(log(i + 1)))
