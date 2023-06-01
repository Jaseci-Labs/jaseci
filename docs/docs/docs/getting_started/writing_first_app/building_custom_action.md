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
def fruit_details(fruit):
  URL = "https://www.fruityvice.com/api/fruit/" + str(fruit)
  r = requests.get(url = URL)
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

## Integrate  custom action into Jaseci