# Tips and Tricks for Jac

Jac is all of pythons goodness wrapped in a language that gives the coder wings. Lets jump right in!

## Running Streamlit in Jac

In pure python, say you have the following streamlit app

```python linenums="1"
--8<-- "examples/myca/streamlit_demo.py"
```

Now typically you'd have to run this with a command like `streamlit run demo.py`.

Here is how you can have a Jac program with the same functionality.

```jac linenums="1"
--8<-- "examples/myca/streamlit_demo.jac"
```

Now you can use `jac run demo.jac`.

Note that If you are unable to run the pure python one, you have to get over that milestone before thinking about the Jac version.