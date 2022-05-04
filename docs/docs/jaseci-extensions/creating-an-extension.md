---
sidebar_position: 2
---

# Creating an extension

Extensions are housed in the `jaseci_core/jaseci/actions` directory of the Jaseci repo. They are composed of an index file which exposes a list of public functions accessible in Jac code and a module file which contains the implementation of those functions.

Example directory structure of a Jaseci extension

```python
jaseci_core/jaseci/actions
|- module
|   |- my_module_actions.py # implementation
|- my_module.py # index
|- ...
```

Let's say we want to extend Jaseci some useful string manipulation functions. The implementation would be something like this:

```python
jaseci_core/jaseci/actions
|- module
|   |- str_actions.py
|- str.py
|- ...
```

`str_actions.py`

```python
def capitalize(param_list):
    """Converts the first character to upper case"""
    if len(param_list) and type(param_list[0]) is str:
        return param_list[0].capitalize()

    raise Exception('Invalid arguments')

def title(param_list):
    """Converts the first character of each word to upper case"""
    if len(param_list) and type(param_list[0]) is str:
        return param_list[0].title()

    raise Exception('Invalid arguments')

def isnumeric(param_list):
    """Returns True if all characters in the string are numeric"""
    if len(param_list) and type(param_list[0]) is str:
        return param_list[0].isnumeric()

    raise Exception('Invalid arguments')

```

`str.py`

```python
from .module.str_actions import capitalize, title, isnumeric
```

Now to ensure everything is working as expected we add unit tests for the action:

```python
jaseci_core/jaseci/tests
|- test_str.py
|- ...
```

`test_str.py`

```python
from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph

from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase

class str_tests(TestCaseHelper, TestCase):
    """Unit tests for str action"""

    def setUp(self):
        super().setUp()
        self.gph = graph(h=mem_hook())
        self.sent = sentinel(h=self.gph._h)

    def tearDown(self):
        super().tearDown()

    def test_str_functionality(self):
        """test functionality of str module"""

        jac_code = """
        walker capitalize {
            can str.capitalize;
            has input;

            report str.capitalize(input);
        }
        """
        self.sent.register_code(jac_code)
        self.assertTrue(self.sent.is_active)

        walker = self.sent.walker_ids.get_obj_by_name('capitalize')
        self.assertIsNotNone(walker)

        walker.prime(self.gph, {'input': 'hello'})
        result = walker.run()
        self.assertEqual(result[0], 'Hello')
```

To test everything out we need to update the code in the Jaseci pod.

```
for podname in $(kubectl get pods -l pod=jaseci -o json| jq -r '.items[].metadata.name'); do kubectl cp jaseci_serv ${podname}:/; echo "Copy code to pod"; kubectl cp jaseci_core ${podname}:/;  kubectl exec -it ${podname} -- bash -c "cd jaseci_core; source install.sh"; done
```

Then run the Jaseci core tests.

```
kubectl exec <jaseci pod name> -- bash -c "cd jaseci_core && source test.sh"
```
