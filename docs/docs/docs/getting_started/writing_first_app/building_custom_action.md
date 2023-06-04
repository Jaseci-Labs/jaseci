---
sidebar_position: 4
title: Building a Custom Action
description: A simple guide to create and use custom action.
---

Certainly! So far, you have learned how to execute Jaseci's built-in features. However In Jaseci, you can create custom actions using Python and integrate them into your Jaseci programs. Custom actions allow you to extend Jaseci's built-in functionality and perform specialized tasks. Here's an example of how you can create and use a custom action in Jaseci using Python;

## Create custom action using python

Lets start by creating a Python module that defines your custom action. Let's say you want to create an action called `fruit_details` that returns all details about a fruit. As a demonstration, we are utilizing a publicly available API endpoint to retrieve a response. Please note that this example is purely for illustrative purposes.

```jac
import requests

from jaseci.jsorc.live_actions import jaseci_action

@jaseci_action(act_group=["fruit_details"], allow_remote=True)
def fruit_details(fruit: str):
    fruit = fruit.lower()
    URL = "https://www.fruityvice.com/api/fruit/" + fruit
    r = requests.get(url=URL)
    return r.json()
```

If you run this as a usual python script you will see following response as the output;

```json
{"name": "Apple",
 "id": 6,
 "family": "Rosaceae",
 "order": "Rosales",
 "genus": "Malus",
 "nutritions": {"calories": 52,
  "fat": 0.4,
  "sugar": 10.3,
  "carbohydrates": 11.4,
  "protein": 0.3}}
```

## Integrate  custom action into Jaseci Shell

Please save the Python script above as a regular Python program by giving it the file name `description.py`.

To load the custom action module into the Jaseci terminal, please follow these instructions:

1. Open the Jaseci shell or terminal.
2. Execute the following command in the Jaseci terminal:

```bash
action load local description.py
```
By executing this command, the action module will be loaded locally into the Jaseci shell, enabling you to utilize the actions created within the module in your JAC program. Once successfully loaded the action you will see following message.

```json
{
  "success": true
}
```

## Updating Jac program to use custom action

Now let's create a walker to get the product details using the custom action module.

```jac
walker product_details {
    has product_name;
    can custom_action.fruit_details;

    report custom_action.fruit_details(product_name);
}
```
As in previous examples you have to register a walker archetype with the above code in Jaseci Studio. and to run the walker use the following payload input as a example.

```json
{
    "product_name":"apple"
}
```