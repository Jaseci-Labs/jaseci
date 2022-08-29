# How to set up jaseci for actions load local



##### Table of Contents  

- [Introduction](#introduction)

- [Build A Custom Jaseci Module](#step-1-build-a-custom-jaseci-module)

- [Load a Custom Jaseci Module](#step-2-load-a-custom-jaseci-module)

- [Test a Custom Jaseci Module](#step-3-test-a-custom-jaseci-module)



# Introduction

In this tutorial we will guide you through on how to set up jaseci for actions load local. We will create a simple calculation module and load it locally.



# Step 1 - Build A Custom Jaseci Module: 

We will create a folder name calculator and in the folder create a file name calculator.py.



In the file import jaseci_action module, this will give us power to all jaseci action functionality.



ADD: ``` from jaseci.actions.live_actions import jaseci_action ```



``` 

from jaseci.actions.live_actions import jaseci_action



```



Then, we will proceed to add a function called ```add```. Which will add two numbers.



``` 

from jaseci.actions.live_actions import jaseci_action



@jaseci_action(act_group=["calc"], allow_remote=True)

def add(

    first_number: int, second_number: int

):

answer = first_number + second_number

return answer

```



Lastly, we will create a port (8000) where we will use to launch the server for jaseci action.



```

from jaseci.actions.live_actions import jaseci_action



@jaseci_action(act_group=["calc"], allow_remote=True)

def add(

    first_number: int, second_number: int

):

answer = first_number + second_number

return answer



if __name__ == "__main__":

    from jaseci.actions.remote_actions import launch_server



    launch_server(port=8000)

```



# Step 2 - Load a Custom Jaseci Module:

In this step we will show you how to load this module we created from the jaseci console (jsctl)



The steps are as follows:

* jsctl -m

* actions load local ``PATH_TO_PYTHON_FILE``



After running that it should be loaded to the console.



# Step 3 - Test a Custom Jaseci Module: 

In this step we will test via browser to see if the module you created works.



The steps are as follows:

* In the terminal, cd into the directory where the calculator.py file is

* then run python calculator.py, you should see `` Application startup complete ``

* Go to the browser and type localhost:8000/docs and you should be redirected to fast api frontend application

* click on ``/add/`` 

* click `` try it out ``

* Enter a value for first_number and second_number

* click ``execute``



Now you should see the results. That is the entire process on how to build a custom module, load and test.
