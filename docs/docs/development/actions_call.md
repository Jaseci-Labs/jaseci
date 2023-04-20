# Actions Call
Action call allows the user to call a loaded action from the JSCTL. This is useful when you need to test out a action without writing a JAC file. You can just pass the context(parameters) with the command and the action will be called.
```jsctl
action call <action_name> -ctx <context>
```

example using the standard actions rand.integer to get a random integer between 0 and 10 (you can list the actions using the `actions list` command)
```jsctl
actions call rand.integer -ctx '{"start":0, "end":10}'
```

You can perform this command on your local actions, rmeote actions or even actions you loaded from a python file.
This is especially useful when you want to change the model of a particular jaseci ai kit module to something else. You can refer the parameters of the setup actions of the module in the docs and then call the setup action with the new parameters.

# Actions Load with context
Normally when you load an action library (Jaseci AI Kit Library), It automatically initialize the model with the default model parameters. But if you want to load the module with different parameters you have to use the `actions call <module_name>.setup -ctx <context>` command. This will load the module with the new parameters. But if you want to override the default parameters of the module you can use the this command.
```jsctl
actions load <module_name> -ctx <context>
```

example using the jac_nlp's gpt2 model to load the model with a different model variant (gpt2-medium) from the default (gpt2) variant, you can use the following command.
```jsctl
actions load jac_nlp.gpt2 -ctx '{"model_name":"gpt2-medium"}'
```