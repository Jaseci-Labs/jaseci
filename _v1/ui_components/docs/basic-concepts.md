### Creating a Component

Each component in Jaseci UI Kit is rendered within a `jsc-app`. After setting up your code, and assuming your `jsc-app` component is placed somewhere in your html tree, the next step is to create the markup. We won't be using HTML to create the structure of our webpage, however, in this case, we will use our `jsc-app` component to generate the markup using JSON.

Creating a component is simple: at the bare minimum we need to create an object with a _component_, _props_, and _sections_ properties. Here's an example of how we can render a Navbar component.

```JSON
	[
		{
			"component": "Navbar",
			"sections": {
				"links": [
					{
						"component": 'NavLink',
						"props": {"label": "Home"}
					}
				]
			},
			"props": {
				"label": "Jaseci",
				"background": "red"
			},
		}
	]
```

In the code above we asked for a Navbar component with a single link element, we set the label of our navbar to 'Jaseci' and the background to 'red'. We also asked for a link within the navbar and for it to be rendered within the _links_ section.

### Names

Names are unique values we attach to a component that will allow us to reference it in the future to get the value of its properties.

### Sections

Sections allow us to place components within another component. It also allows us to place components at specific locations within another component. In our example above, with the navbar component, links is a section specific to the navbar component that allows us to add _Link_ components within the navbar. Some components have sections and some do not, so be sure to review the available sections for each component to know when and where you can place components within another.

### Events

Events allow us to interact with our markup. Just like we can generate the _structure_ of our webpage using _props_ to control the styling and content of our components we can use _events_ to add logic and functionality to make our site interactive. Let's have a look at how we can add an event to our navbar component.

Let's assume we want to display an alert message when a link is clicked: we can modify our link component to listen to an _onClick_ event we can perform an action when we click on the link component.

Taking the code from our example above, let's modify it, we'll start by adding an _events_ property to our link component, and within that events property, our action. Let's do it.

```JSON
	[
		{
			"name": "nav",
			"component": "Navbar",
			"sections": {
				"links": [
					{
						"component": 'NavLink',
						"props": { "label": 'Home' }
						"events": {
							"onClick": [
								{
									"fn": "alert",
									"args": ["Jaseci"]
								}
							]
						}
					}
				]
			},
			"props": {
				"label": "Jaseci"
			},
		}
	]
```

After adding the code above, whenever we click on the _Home_ link we are going see the message "Jaseci" printed in an alert dialog.

### Actions

Actions allow us to run arbitrary javascript functions and built-in functions provided by the ui kit in response to certain events. You can perform multiple actions, one after the other, or compose actions to perform an action after another completes, or fails.

In the example above we created an alert action in response to an `onClick` event. Let's take a closer look at what we did.

To create an action we need to create an object with the `fn` property and the `args` property.

- _fn_ - the name of the function we want to call
- _args_ - the values we pass to the function as arguments

Here what our action looked like.

```JSON
"onClick": [
	{
		"fn": "alert",
		"args": ["Jaseci"]
	}
]
```

What if we wanted to _update_ a property instead? We can changing our action function to `update` along provide its two args: the property we want to update and the value of the property.

Here what our action looks like now.

```JSON
"onClick": [
	{
		"fn": "update",
		"args": ["nav.label", "Jaseci 2.0"]
	}
]
```

Assuming this `onClick` event is still attached to our nav link component, whenever we click on this link the label of the navbar will change from `Jaseci` to `Jaseci 2.0`.

#### Action conditions

Consider the following code.

```JSON
"onClick": [
	{
		"fn": "update",
		"args": ["nav.label", "Jaseci 2.0"],
		"cond": ['var(nav.label)::#neq::Jaseci 2.0'],
	}
]
```

What have you noticed? It works the same as before, however, there's now a `cond` property, this property allow us to prevent the execution of some actions unless a certain condition is satisfied. Each condition is a string. In this example, if we click update and the label is not already `Jaseci 2.0` the action will run, if is `Jaseci 2.0`, it remain the same.

We can provide multiple conditions to an action and the action will only run if all conditions are satisfied.

#### Chaining Actions

We can run until another is executed. We can do so by providing an action as the value to the `onCompleted` property of another action. Here's an example using the code above:

```JSON
"onClick": [
	{
		"fn": "update",
		"args": ["nav.label", "Jaseci 2.0"],
		"cond": ['var(nav.label)::#neq::Jaseci 2.0'],
		"onCompleted": {
			"fn": "alert",
			"args": ["Navbar title updated."]
		}
	}
]
```

Also consider the following code.

```JSON
"onClick": [
	{
		"fn": "update",
		"args": ["nav.label", "Jaseci 2.0"],
		"cond": ['var(nav.label)::#neq::Jaseci 2.0']
	},
	{
		"fn": "alert",
		"args": ["Navbar title updated."]
	}
]
```

In the first code above, we ask for an alert dialog to display after the `update` action is finished. But what about the second code, doesn't it work the same? In this case, yes, but also no. Taking a closer lock at the `update` action of the first code, it has a `cond`, this condition will also prevent the `onCompleted` action from running if the `update` function did not run. The second code will give us an alert dialog even if the update function did not run.

### Operations

Operations are "custom actions" that we can create that will allow us to reuse a particular sequence of actions across components. Each operation has a name and can optionally accept a number of arguments.

Take a look at the following example:

```JSON
[
    {
        "component": "Container",
        "name": "container1",
        "operations": {
            "sayHi": {
                "args": [
                    "message"
                ],
                "run": [
                    {
                        "fn": "alert",
                        "args": [
                            "arg(message) cool!"
                        ]
                    }
                ]
            }
        }
    },
    {
        "component": "Button",
        "events": {
            "onClick": [
                {
                    "fn": "runOperation",
                    "operation": "container1.sayHi",
                    "args": [
                        "Hello world!"
                    ]
                }
            ]
        },
        "props": {
            "name": "btn1",
            "label": "Say Hello"
        }
    }
]
```

In the example above, we defined an operation within the `container1` component then we called this operation in the `btn1` component. Each operation is called using the `callOperation` action. The `callOperation` action requires the `operation` property to be defined with a valid operation as its value. An operation is referenced using the format `[Component Name].[Operation Name]` which translates to `container1.sayHi` in this case.

#### Operation Args

When defining an operation we can set the `args` property to a list of strings. This can be used to accept args to your operation. Each arg can be used in the actions within an operation and will be replaced by the values passed in the args of the `callOperation` action. In the example above, `arg(message)` is replaced with 'Hello world!' and the message alerted is 'Hello world! cool'.

### Property References

Property references allow us to get the value of the property of a component. This allows us to move across components. For example, let's say you have an `Inputbox` component and you want to `alert` the value of the input box whenever the user presses the `Enter` button. How would we do that? Let's explore.

Let's start by taking a look at the following code:

```JSON
[
		{
			"name": "inputbox1",
			"component": "Inputbox",
			"sections": []
			"events": {
				"onEnter": [
					{
						fn: "alert",
						args: "Hello, var(inputbox1.value)!"
					}
				]
			},
			"props": {
				"placeholder": "Enter your name..."
			},
		}
]
```

The above code will render an `Inputbox` component with a placeholder of `Enter your name...`. If we enter our name in the box and press the `Enter` button on the keyboard an alert dialog is shown and `var(inputbox1.value)` is replaced with the value of the input box.
