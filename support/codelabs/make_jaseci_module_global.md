# How to make an Action module default/global in Jaseci


#### Introduction
For this tutorial, we will be walking you through how we added the zlib module as a default or global action.

#### Step 1: Creating Jaseci Action Module
Create your jaseci action module in the `jaseci_core/jaseci/actions/standard/` folder in the Jaseci repository. In this example, we will create a file to that path called `zlib.py`.

``` py
"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action
from base64 import b64decode, b64encode
import zlib


@jaseci_action()
def compress(data_b64: str = ""):
    """
    Compress data
    Param 1 - data in base64
    Return - compressed data in base64
    """
    data_bytes = b64decode(data_b64.encode("ascii"))
    data_compressed_bytes = zlib.compress(data_bytes)
    data_compressed_b64 = b64encode(data_compressed_bytes).decode("ascii")
    return data_compressed_b64


@jaseci_action()
def decompress(data_b64: str = ""):
    """
    Decompress data
    Param 1 - data in base64
    Return - decompressed data in base64
    """
    data_bytes = b64decode(data_b64.encode("ascii"))
    data_decompressed_bytes = zlib.decompress(data_bytes)
    data_decompressed_b64 = b64encode(data_decompressed_bytes).decode("ascii")
    return data_decompressed_b64
```

### Step 2: Add Test to the Jaseci Action Module
It's very important to add test to these module especially when you are adding it to the Jaseci Standard Module. You will create your test in the `jaseci_core/jaseci/actions/standard/tests/` repository for Jaseci and we will be adding `test_zlib.py` to the path. 

``` py
from jaseci.utils.test_core import CoreTest, jac_testcase


class ZlibTest(CoreTest):

    fixture_src = __file__

    data_uncompressed = "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII="
    data_compressed = "eJzrDPBz5+WS4mJgYOD19HAJAtIcIMzIDCT/HdQ5AaTYAnxCXP///79///7FzmWWQBE+TxfHEI7ryT8YWv8IcDDoMTD/XZyZdxEow+Dp6ueyzimhCQDLCRkd"

    @jac_testcase("zlib.jac", "compress_test")
    def test_compress(self, ret):
        print(ret["report"])
        self.assertEqual(
            ret["report"][0],
            self.data_compressed,
        )

    @jac_testcase("zlib.jac", "decompress_test")
    def test_decompress(self, ret):
        print(ret["report"])
        self.assertEqual(
            ret["report"][0],
            self.data_uncompressed,
        )
```

### Step 3: Initialize the new global/default module
For Jaseci to recognize the newly added global module you will have to point it to the module you have just created in the `jaseci_core/jaseci/__init__.py`. In this example, we will show you how we did it in the zlib action module.

```py
    import jaseci.actions.standard.mail  # noqa
    import jaseci.actions.standard.task  # noqa
    import jaseci.actions.standard.internal  # noqa
    import jaseci.actions.standard.zlib  # < HERE WE ADDED THE ZLIB ACTION MODULE


load_standard()
```

### Step 4: Add the module to live actions
Finally, we will add the module you have created to jaseci live actions. In this case we will be adding zlib. 

```py
            or i.startswith("date.")
            or i.startswith("jaseci.")
            or i.startswith("internal.")
            or i.startswith("zlib.") # < Here we added zlib to the jaseci live actions.
        ):
            global_action_list.append(
                Action(
```
