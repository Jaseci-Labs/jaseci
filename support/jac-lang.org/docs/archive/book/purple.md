# Purple Pill: New Language Features to Improve Traditional Programming

This section describes the cutting-edge features introduced by Jac that enhance and refine traditional programming concepts. This section is designed to offer you an in-depth exploration of these novel features, their syntactical implementation, and the added benefits they bring to the coding experience. By leveraging these features, you can develop efficient, robust, and maintainable software solutions. Here we give Python wings!

In this Purple Pill spec, a range of innovative features including the Pipe Forward Operator, Null Safe Operators, the Elvis Operator, Freestyle Abilities, Freestyle Spawn and Filter Contexts, Enhanced Walrus Operations, and advancements in Dict and Duck Typing. Each feature is designed to build upon traditional programming paradigms, integrating seamlessly with the existing Jac language structure, while offering improved readability, functionality, brevity and performance. Let's delve into these features one by one.

We start with the most basic improvements and gradually go down the rabbit hole towards the Red Pill section (thats where you learn about your new super powers young neophyte).

### Enhanced Walrus Operations

In the Jac programming language, we have taken inspiration from Python's "walrus operator" (`:=`), a nickname for the assignment expressions feature. The walrus operator allows you to assign and return a value in the same expression. But why stop there - we have extended this concept to include augmented assignment statements such as `+=`, `-=`, `/=`, `*=`, and `%=`.

In Python, these operators perform an operation on a variable and assign the result back to that variable. In Jac, these operators behave like walrus assignments, meaning that they perform the operation, assign the result back to the variable, and then return the new value, within the single statement.

Let's take a closer look at a few examples:

#### `+=`

The `+=` operator in Jac will add the right operand to the left operand, assign the result back to the left operand, and return the new value of the left operand.

```jac
if (x += 5) > 10 {
    print(x);
}
```

In the example above, `x += 5` will add `5` to `x`, assign the result back to `x`, and return the new value. If the new value of `x` is greater than `10`, it will print `x`.

#### `-=`, `*=`, `/=`, and `%=`

The `-=` operator behaves similarly. It subtracts the right operand from the left operand, assigns the result back to the left operand, and returns the new value. The `*=` operator multiplies, the `/=` operator divides and the `%=` operator finds the modulus of the left operand divided by the right operand, all assigning the result back to the left operand, and returning the new value.

Here are examples of how they can be used:

```jac
while (y -= 2) >= 0 {
    print(y);
}

if (z *= 3) < 100 {
    print(z);
}

while (a /= 2) > 1 {
    print(a);
}

var = [b %= 7 for b in my_array];
```

These enhancements to the augmented assignment statements in Jac facilitate succinct expressions and efficient programming especially in loops and conditionals.

### Null Safe Operators

Dealing with null values is a common pain point in many programming languages. Jac introduces Null Safe Operators as an effective solution to mitigate potential null reference exceptions, which helps make your code more robust and readable.

Null Safe Operators, also known as 'safe navigation operators', allow you to access methods and properties of an object that may potentially be `null` or `None`. When the operator is used, the system checks whether the object is `null`. If it is, the operation is not performed, and `null` is returned instead, preventing a potential null reference exception.

Let's consider an example. Suppose you want to access a property of an object. In traditional programming, you might write:

```python
value = None
if obj and hasattr(obj, "property"):
    value = obj.property
```

With Jac's Null Safe Operator, this could be significantly simplified:

```jac
value = obj?.property;
```

In this code snippet, if `obj` is `null`, the Null Safe Operator (`?.`) short-circuits the operation, and `value` is set to `null`. If `obj` is not `null`, `value` is set to `obj.property` only if obj has the property. This mechanism ensures that you never try to access a property or method on a `null` object, thereby avoiding runtime errors.

Null Safe Operators also work with function and method calls. If `obj` is `null`, a call like `obj?.method()` simply returns `null` instead of throwing an error.

By employing Null Safe Operators, you can write safer, cleaner code with less boilerplate, contributing to a better and more effective programming experience with Jac.

### Elvis Operator

The Elvis Operator, represented as `?:`, is a binary operator that provides a shorthand syntax for handling default values. Its function is to return the first operand if it is not `null` or `None`, otherwise, it returns the second operand. The operator gets its name from its visual resemblance to Elvis Presley's iconic hairdo when turned sideways.

This operator is especially handy when you need to assign default values to variables or need a fallback for potentially `null` or `None` expressions.

Here's how you can use the Elvis Operator in Jac:

```jac
value = potentiallyNullValue ?: defaultValue;
```

In this example, `value` is assigned the value of `potentiallyNullValue` if it's not `null`. If `potentiallyNullValue` is `null`, `value` is assigned `defaultValue`.

This concise syntax drastically simplifies and cleans up your code by removing the need for verbose `if-else` constructs to handle `null` cases. Without the Elvis Operator, the same operation would look something like this:

```python
if potentiallyNullValue is not None:
    value = potentiallyNullValue
else:
    value = defaultValue
```

and at best
```python
value = potentiallyNullValue if potentiallyNullValue is not None else defaultValue
```

As seen from this comparison, the Elvis Operator is a powerful tool to make your code more readable and succinct, reducing unnecessary verbosity while maintaining clear intent. It's one of the many features that contribute to Jac's goal of creating an enjoyable and efficient programming experience.

Next lets increase the heat and introduce some deeper Jactastic concepts.

### Pipe Forwarding

The Pipe Forward Operator, denoted as `|>`, is an elegant addition to Jac that facilitates a intuitive style of programming and improves code readability. It also serves as a unifying bridge between traditional and data spatial programming concepts and constructs (more on that later.)

The basic pipe forward operator allows the result of an expression to be 'piped forward' into a function or method. It essentially streamlines the process of passing a value or set of values from one function to the next, making code more intuitive and decluttered.

Here's how it works: the expression on the left-hand side of the operator serves as an input to the function on the right-hand side. The operator takes the result of the left-hand expression and inserts it as the first argument of the right-hand function. This feature is especially useful when you have a sequence of functions where the output of one function is the input to the next.

Consider the following Python code:

```python
result = f(g(h(x)))
```

Using the Pipe Forward Operator in Jac, the above can be written as:

```jac
result = x |> h |> g |> f;
```

In this scenario, `x` is passed as an argument to the function `h()`, the result of which is then passed to `g()`, and so on, until it finally feeds into `f()`. This arrangement of code not only increases readability but also follows a more logical, left-to-right flow, closely mirroring the way the data 'moves' through the transformations.

The Pipe Forward Operator is generally preferred in Jac as it embodies the expressive and readable nature of Jac, empowering you to write clean, efficient, and 'Jactastic' code.

#### Enhanced Pipe Fowarding

Jac introduces an ehanced versatile usage model for the pipe forward operator (`|>`), extending beyond the traditional single output, single input paradigm. This enhanced semantic allows the passing of an arbitrary amount of parameters by employing a unique notation leveraging _spawn contexts_ (more on these later).

This notation is denoted by `{}` and can contain multiple parameters. These parameters will be mapped to the arguments of a function when used in conjunction with the pipe forward operator. The syntax is as follows:

```jac
result = {param1, param2, param3} |> foo;
```

In the example above, `param1`, `param2`, and `param3` will be applied to the first three arguments of the `foo` function.

The spawn context notation also supports named arguments similar to Python's _kwargs_ functionality. Here's how you can use it:

```jac
result = {param1, in_param=param2} |> foo;
```

In the above example, `param1` will be passed as the first argument to the `foo` function and `param2` will be passed to the argument named `in_param` in the `foo` function.

#### Chaining Spawn Contexts and Pipes

Pipes through spawn contexts can be chained together. This enables more complex parameter passing and function chaining:

```jac
{bar() |> baz(), param2} |> foo |> qux
```

In this example, the result of `bar() |> baz()` is passed as the first argument to `foo` and `param2` is passed as the second argument. The result of `foo` is then piped forward to the `qux` function.
#### A Foundational Construct and Conceptual Insight

As you may have realized, in Jac, any traditional style function or method call can be replaced with a pipe forward construct for passing parameters. We highly recommend using this notation for improving both readability and intuitiveness of your code. However, this is not the only reason we make this recommendation.

Beyond providing a powerful mechanism to make your code more readable and intuitive, the use of the pipe forward operator also serves as an important conceptual bridge for understanding the relationship between traditional programming and data spatial programming. Function calls can be seen as, and indeed is, a process of sending data, through parameters, to compute units.

Data spatial programming flips this thought process on its head by allowing you to send compute to data and to have compute travel through data. This important insight forms the foundation of the innovative data spatial programming model, which will be explored in more detail in the Red Pill section.

### Freestyle Spawn Contexts

While we've previously seen spawn contexts utilized as a means to send parameters to functions, the role of spawn contexts in Jac is far more expansive. At its core, a spawn context is an impromptu transient expression that describes a collection of data and can be used in various contexts throughout a program.

#### Spawn Context Structure

A spawn context in Jac provides a flexible and dynamic syntax for representing a collection of data. At its core, the structure of a spawn context is `{ <expressions, ...>, <keys=values, ...> }`. Let's break down this structure and examine its components.

The first part, `<expressions, ...>`, can contain a list of one or more expressions. An expression in this context can be a variable, a function call, an operation, or any other valid Jac expression that produces a value. These expressions are evaluated and their resulting values are collected in the spawn context.

Here is an example using expressions-only in a spawn context:

```jac
{param1, param2, do_something()}
```

The second part, `<keys=values, ...>`, allows you to specify one or more key-value assignments. These key-value pairs can be used to initialize an object, augment a dictionary (or object), or even set parameters with specific names in function calls.

Here's an example of using key-value pairs in a spawn context:

```jac
{key1=value1, key2=value2}
```

Spawn contexts can flexibly combine both expressions and key-value pairs within the same context as long as all the experssions preceeds the key, value assignments:

```jac
{param1, param2, key1=value1, key2=value2}
```

#### Various Use Cases of Spawn Contexts

In Jac, spawn contexts are not just a feature, but an indispensable tool that supports a variety of use cases. Let's explore some of these practical applications and see how spawn contexts can simplify our code, make it more intuitive and readable.

##### Initializing Object Members with Spawn Contexts

One of the major applications of spawn contexts lies in initializing member fields of an arbitrary object or dictionary. This can be accomplished by "piping" that object into a spawn context.

Consider this example:

```jac
MyObj |> {field1="4", field2="5"};
```

With this succinct and intuitive syntax, we set the member fields `field1` and `field2` of `MyObj` to `4` and `5` respectively. The elegance of this approach becomes more apparent when dealing with larger objects with numerous fields, making the initialization process cleaner and more readable.

##### Simplifying Method Calls with Spawn Contexts

Spawn contexts in Jac also greatly simplify the process of sending parameters to a method. Consider the following example:

```jac
{p1, p2} |> MyObj.process
```

In this example, the parameters `p1` and `p2` are being passed to the `process` method of `MyObj`. This use of spawn contexts makes the method calls much more readable and understandable.

##### Augmenting Dictionaries using Spawn Contexts

Spawn contexts also facilitate the process of adding new keys and values to an existing dictionary or object. Here's how:

```jac
my_dict |> {"k1"=v1, "k2"=v2}
```

In this example, the keys `k1` and `k2` with corresponding values `v1` and `v2` are added to the `my_dict` dictionary. The same operation can be performed on an object as well, demonstrating the flexibility of spawn contexts.

##### Modifying Lists with Spawn Contexts

Spawn contexts also extend their utility to lists. They can be used to overwrite specific items in a list. Consider this example:

```jac
my_list |> {"first", "three", "words"}
```

Here, the first three items of `my_list` are replaced by "first", "three", and "words", respectively. This opens up an intuitive way to manipulate list data in Jac.

Overall, spawn contexts in Jac provide a versatile toolset for handling and transforming data in a variety of scenarios, making them an integral part of the language's design.


##### Another Foundational Construct in Jac

Spawn contexts is another key primitive construct that assists with data spatial programming. In advanced use-cases such as with freestyle abilitys and walkers (to be detailed later), you can leverage spawn contexts to create transient faux objects and nodes.

For now simply note that spawn contexts are functionally intertwined with the use of pipe forwards (`|>`) as demonstrated in all examples above. In addition, spawn contexts also have a tight functional relationship with the `spawn` keyword, which will be introduced in the very next section of this specification.

### Freestyle Abilities

The **freestyle ability** is the simplest data spatial programming construct in Jac and a keystone starting place to introduce Jac's innovative perspective on the treatment of data. An ability is a variation on a typical function that we cover in detail later. A freestyle ability is unattached to any object, node, or walker, resides at the module level, can be called from anywhere in the module, and can return a value. As such they are essentially functions, except unlike conventional functions, which receive data through parameters, a freestyle ability is spawned on an object and directly accesses the data they need from the object. It is conceptually a region of code that jumps to the data in some location, operates on it there, and then may return a value. In this sense, a freestyle ability is dispatched to the data it needs, leaping from one location to another when taking a spatial view of data.

The fundamental aspect of a freestyle ability is its reliance on the `here` reference. `here` allows a freestyle ability to interact with the data present at the "location" (data object) it was spawned from. As mentioned in the Blue Pill section `here` is analogously to the `self` keyword in the context of a class in python, and in this context, it allows the freestyle ability to access and manipulate the data it resides on.

Here is a basic freestyle ability definition:

```jac
can calculate_avg with float {
    sum = 0
    for i in here.array:
        sum += i
    return sum/len(here.array)
}
```
In this example, the ability `calculate_avg` is designed to calculate the average of an array and return a float value. Note that it does not take parameters but uses `here` to reference the object it is currently residing on. This freestyle ability expects the object it's being spawned on to have a field named `array`.

To invoke the freestyle ability, pipe forward is used to indicate shipping the ability to the data. The syntax is `:c:<freestyle ability_name> |> <object/data>`.

Consider the following object:

```jac
object MyObj {
    has array: list[int] = [1, 2, 3, 4, 5];
}

global obj = spawn :o:MyObj;
```

Invoking the freestyle ability on this object would look as follows:

```jac
avg = :c:calculate_avg |> obj;
```

The `calculate_avg` freestyle ability is sent to the `obj` object. The freestyle ability then accesses the fields of the object using the `here` reference, processes them, and returns the result which is assigned to `avg`.

Note that a spawn context can be used here as well,

```jac
avg = :c:calculate_av |> {array = [1, 2, 3, 4, 5]};
```

#### Introducing Duct Typing

A key aspect of the freestyle ability's design is the use of **duct typing**. A freestyle ability does not explicitly require parameters or a data type. Instead, it uses the `here` reference to fetch the data it needs from its current location. Therefore, the success of a freestyle ability invocation largely depends on whether the data it operates on contains the necessary fields and whether they hold the appropriate type of data. (More on the concept of duct typing in the next subsection)

#### A Gentle Introduction to Data Spatial Programming

The freestyle ability construct in Jac provides an introductory yet profound insight into the world of data spatial programming. It emphasizes the shift from sending data to operations to moving operations to data, implementing in-situ data processing. This not only reduces data movement but also creates more cohesive, readable, and intuitive coding style by encouraging operations to stay close to the data they're associated with. We delve deeply into this topic in the Red Pill, however, this is a handy and useful data spatial superpower anyone can wield.

### Understanding Duck Typing in Jac

Duck Typing is a programming concept that emphasizes on the behavior of an object over its actual type. The term 'duck typing' comes from the phrase "If it looks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck," illustrating the idea that an object's suitability for a task is determined by its methods and properties, not its class or type.

In Jac, Duck Typing is employed (particular in its data spatial feature set) to enhance flexibility and readability of code. It allows you to use objects flexibly, based on their capabilities, rather than rigidly checking their types. It promotes writing code that is less concerned about the actual type of the objects and more about what actions (or abilities) can be performed with them.

Here's a simple example to illustrate Duck Typing in Jac:

```jac
can quack {
    duck.quack();
}

with entry {
    goose = spawn Goose;
    quack |> goose;
}
```

In this example, the `quack` ability works on object as long as it has a `quack` method. The function doesn't care about the type of the object; it only cares that the object can perform the `quack` operation.

This concept not only provides flexibility when using objects, but also promotes code reusability and encourages the design of loosely coupled systems. With Duck Typing, you can write more dynamic and adaptable code. It makes the language more expressive and eases the development of complex systems, making Jac an attractive choice for developing robust and flexible software solutions.
Jac's approach to Duck Typing expands on traditional concepts, offering more flexible and dynamic behavior based on object capabilities rather than their types.

### Dict Typing

This principle of duct typing and the way it is leveraged in Jac allows dictionaries and object instances to be used interchangeably for freestyle abilities and walkers, as long as they adhere to the required interface or 'shape'.

Lets look at an example in Jac. A dictionary is a collection of key-value pairs. The key can be any immutable type, typically a string, and the value can be any valid expression. For example:
```jac
dict1 = {'name': 'John', 'age': 30};
```

An object instance in Jac can be a structurally similar entity, but it is created from an object type and can have associated data spatial and method abilities in addition to properties:

```jac
object Person {
    has name: str = 'John';
    has age: int = 30;
    }

    can greet() -> None {
        return `Hello, my name is ${this.name}`;
    }
}

person1 = spawn :o:Person;
```

In Jac's duck typing, these two types can be used interchangeably. For instance, if an ability expects an object with properties 'name' and 'age', both a dictionary with these keys and an instance of `Person` could be passed in:

```jac
can get_age with int {
    return here.age;
}

with entry {
    :c:get_age |> dict1; # returns 30
    :c:get_age |> person1; # returns 30
}
```

In this scenario, `get_age` function is not concerned with the type of entity, only that it has an 'age' property. The same concept will be used for walkers as well.

You can also reference items in a dictionary with as you would an object as per
```jac
with entry {
   dict1.age = 31; # sets age to 31
}
```

However do note, that this feature is only available for string type keys that have no spaces or special characters and are formated as proper identifiers. Otherwise the standard `dict1["some key"]` type format must be used.

### Freestyle Filter Contexts

A filter context in Jac provides a robust and powerful syntax for constraining a dataset. It is represented as a sequence of constraints using the notation `(= <var> <cmp_op> <expr>, ...)`. Let's dissect this structure and look at its components.

The core notation `(= <var> <cmp_op> <expr>, ...)` defines a set of conditions that the data must meet. `<var>` is a variable that represents the data we are comparing. `<cmp_op>` is a comparison operator such as `==`, `!=`, `<`, `<=`, `>`, `>=`. `<expr>` can be a variable, a function call, an operation, or any other valid Jac expression that produces a value. These expressions are evaluated and used for comparisons. The data that meets these conditions will be collected in the filter context.

Here is an example using a single filter constraint:

`(= age >= 18)`

Multiple constraints can be specified in a filter context. The constraints are evaluated independently and the intersection of data that satisfies all conditions is collected in the filter context. It is a powerful tool for specifying complex conditions on the data.

Here's an example of using multiple filter constraints:

`(= age >= 18, income > 50000)`

The order of constraints doesn't matter. The data is filtered in a way that it meets all the conditions, irrespective of the order in which they are specified. So, the above filter context is equivalent to `(= income > 50000, age >= 18)`

Filter contexts provide a way to concisely specify data constraints and open up a wide range of possibilities for data manipulation in Jac programming.

