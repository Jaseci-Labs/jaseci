# Tips and Tricks

Here are some general tips, tricks, and how-tos for Jac.

## Running Streamlit in Jac

In pure python, say you have the following streamlit app

=== "streamlit_demo.py"
    ```python linenums="1"
    --8<-- "examples/myca/streamlit_demo.py"
    ```

Now typically you'd have to run this with a command like `streamlit run demo.py`.

Here is how you can have a Jac program with the same functionality.
=== "streamlit_demo.jac"
    ```jac linenums="1"
    --8<-- "examples/myca/streamlit_demo.jac"
    ```

Now you can simply use `jac run streamlit_demo.jac` as normal. Basically, you can take that `sl_start` ability and add it to any streamlit jac project. Note that there is a hardcoded value in the function for the name of your app (though it doesn't have to be). I'll leave it as a challenge to you on how to have that automatically resolve the file name. *sneeze* `__file__` *sneeze*

Note that If you are unable to run the pure python one, you have to get over that milestone before thinking about the Jac version.