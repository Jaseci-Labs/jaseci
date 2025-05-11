# Enhancing Semantic Meaning in Code for LLM Inference

The core idea behind MT-LLM is that if the program has been written in a readable manner, with type-safety, an LLM would be able to understand the task required to be performed using _meaning_ embedded within the code.

However, there can be instances where this is not the case when the programmer needs to use less semantically rich code. Hence, a new _meaning_ insertion code abstraction called "**semstrings**" has been introduced in MT-LLM.

## Where code is not meaningful enough!

Lets look into an instance where the existing code constructs are not sufficient to describe the meaning of the code for an LLM.

```jac
import from mtllm.llms, OpenAI;

glob llm = OpenAI();

obj item {
    has name : str,
        category : str = '';
}

obj shop {
    has item_dir:dict[str,item];

    can categorize(name:str) -> str by llm();
}

with entry {
    shop_inv = shop();
    apple = item(name=apple);
    apple.category = categorize(apple.name);
    shop_inv.item_dir[apple.name] = apple.category;
}
```

This is a partial code that can be used as a shopkeeping app where each item name is tagged with its category. However, in this example, you can observe in line 16 that the item name is passed in as 'apple' which can be ambiguous for an LLM as apple can mean the fruit, as well as a tech product. To resolve this problem we can use much more descriptive variable names. For instance, instead of ```item``` we can use ```tech_item```. How ever, adding more descriptive names for objects, variables and functions will hinder the reusability of object fields as the reference names are too long.

## Semstrings to uplift 'meaning'


As the existing code abstractions does not fully allow the programmer to express their meaning we have added an extra feature you can use to embed meaning directly as text, into your code. We call these text annotations as **semstrings**.

Lets see how we can add semstring to the existing program above.

```jac
import from mtllm.llms, OpenAI;

glob llm = OpenAI();

obj 'An edible product'
item {
    has name : str,
        category : str = '';
}

obj 'Food store inventory'
shop {
    has item_dir:'Inventory of shop':dict[str,item];

    can 'categorize the edible as fruit, vegetables, sweets etc'
    categorize(name: str) -> 'Item category': str by llm();
}

with entry {
    shop_inv = shop();
    apple = item(name=apple);
    apple.category = categorize(apple.name);
    shop_inv.item_dir["ID_876837"] = apple;
}
```
In this example we add semstrings that add semantic meaning to existing code constructs such as variables, objects and functions. The semstring of each item is linked with its signature which are called when generating the prompt for the LLM. These small descriptions adds more context for the LLM to give a much more accurate response.

## How to add semstrings?

The below examples show different instances where semstrings can be inserted.

### Variables / Object Fields Declaration

```jac
glob name: 'semstring': str = 'sample value'
```
### Function / Method Declaration

```jac
can 'semstring'
function_name(arg_1: 'semstring': type ...) {
    #function body
}
```

### Object / Class Declaration

```jac
obj 'semstring' object_name {
    # Object fields
    # Object methods
}
```

### With ```by llm()```

```jac
can 'semstring_for_action'
function_name (arg_1:'semstring_input': type ...)
-> 'semstring_output': type
by llm();
```