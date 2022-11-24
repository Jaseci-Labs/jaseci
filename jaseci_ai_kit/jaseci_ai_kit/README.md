## **Test creation guidelines for Jaseci-AI-Kit**
This document defines the process to create test cases for Jaseci-Ai-Kit module. For creating this test we'll make use of Jaseci CoreTest Class and pytest framework. Let's walk through the test kit creation by following the steps below.

1. Defining the [folder](#1-defining-the-folder-structure) structure
2. Creating the [jac](#2-creating-the-jac-file) file
3. Creating the python [test](#3-creating-the-python-test-file) file
4. [Running](#4-running-the-test) the test

### **1. Defining the folder structure**
In the main module we'll need to create a `tests`  folder within test folder we'll need to have a `fixtures` folder
```bash
    mkdir tests
    mkdir tests/fixtures
```
### **2. Creating the jac file**
We'll need to create a jac file inside the fixtures folder.
```bash
    touch tests/fixtures/<file_name>.jac
```
The above jac file would contain the walkers to test all the functional flow of the AI module.
```jac
    walker test_bi_enc_get_model_config{
    can bi_enc.get_model_config;
    report bi_enc.get_model_config();
    }
```
### **3. Creating the python test file**
We'll need to create a python file inside the tests folder for the testcases.
```bash
    touch tests/<file_name>.py
```
1. **Relevant imports**

   We'll need to import CoreTest class and jac_testcase function from the test_core module.
   ```python
    from jaseci.utils.test_core import CoreTest, jac_testcase
   ```
   We'll also need to import load and unload actions module to load and unload the actions
   ```python
    from jaseci.actions.live_actions import load_module_actions, unload_module
   ```
   we'll need the pytest import for ordering the test cases
   ```python
    import pytest
   ```
2. Creating the Test Class

   We'll need a main Test class that would contain all the test cases.
   ```python
   class BiEncTest(CoreTest):
        fixture_src = __file__
   ```
   1. **Defining Setup and Tear down classes**

        The `Setup` and `TearDown` classes are used to load and unload the module before and after executing the test cases
        ```python
            @classmethod
            def setUpClass(cls):
                super(BiEncTest, cls).setUpClass()
                ret = load_module_actions("jaseci_ai_kit.bi_enc")
                assert ret is True
            @classmethod
            def tearDownClass(cls):
                super(BiEncTest, cls).tearDownClass()
                ret = unload_module("jaseci_ai_kit.modules.encoders.bi_enc")
                assert ret is True
        ```
   2. **Creating testcase**

        Defining each testcase has 3 steps

        1. Marking the order of excution
        ```python
            @pytest.mark.order(1)
        ```
        2. Passing the jac file and the walker name to the jac_testcase decorator to regiter the code and excute the walker
        ```python
            @jac_testcase("bi_enc.jac", "test_bi_enc_get_model_config")
        ```
        3. Create the testcase to manipulate and validate the return value
        ```python
            def test_biencoder_get_model_config(self, ret):
                self.assertEqual(ret["success"], True)
        ```
        Each test case in the class would look something similar to
        ```python
            @pytest.mark.order(1)
            @jac_testcase("bi_enc.jac", "test_bi_enc_get_model_config")
            def test_biencoder_get_model_config(self, ret):
                self.assertEqual(ret["success"], True)
        ```

### **4. Running the test**
To run the test file we'll use the pytest command to execute the all test cases
```python
    pytest tests/<file_name>.py
```