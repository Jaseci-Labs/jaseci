# Programming with GenAI
<!-- TODO: Guide for coders to use by_llm @kugesan1105 Put the one in the chatgpt -->
GenAI Ability is a powerful feature that enhances interaction with Large Language Models (LLM) by utilizing the keyword `by <model>`. Developers can customize the behavior of functions or methods by modifying associated
[Semstrings](#introducing-semstrings).
Jaclang will be extended to support a new abstraction that simplifies the development of llm applications. With the introduction of the `with <language_model>` syntax, developers can easily activate this abstraction by placing it after any ability. This new feature eliminates the need for explicit prompting and allows for a more streamlined coding experience. It's important to note that when using this ability, the return will be handled by the abstraction itself, removing the need for an explicit ability body.
**Model Initialization**

<!--To incorporate a Large Language Model (LLM) into code, initialize it as a model code construct.

```
model llm {
    model_name: "gpt-4";
    temperature: 0.7;
    do_sample: true;
}
```
The llm model is defined in this example with specific attributes, such as utilizing the GPT-4 model, setting a temperature of 0.7 for sampling, and enabling text sampling.

This approach allows for the initialization of the desired model as a model code construct with a specific name (in this case, `llm`), facilitating its integration into code. -->


**Example Usage**

**1. Function Usage**
```
can 'Summarize the Life of the Individual'
summarize(name: 'Name of the Person': str, age: 'Age of the Person': int)
    -> 'Summary': str by llm(temperature=0.7, reason=True);
with entry {
    print(summarize('Albert Einstein', 89));
}
```
In this example, the summarize function leverages GenAI Ability to provide a summary of an individual's life. The associated Semstring ('Name of the Person', 'Age of the Person') guides the function's behavior. The `by llm` feature allows customization of the interaction, with parameters like temperature and reason influencing the model's response.

**2. Method Usage**
```
obj 'Person'
Person {
    has name: 'Name' str,
        dob: 'Date of Birth' str,
        age: 'Age' int = None;
    can 'Calculate the Age of a Person'
    calculate (cur_year: 'Current Year': int) -> 'Calculated Age': int by llm();
}
with entry {
    einstein 'Einstein Object': Person = Person(name="Einstein", dob="1879-03-14");
    age = einstein.calculate(cur_year=2024);
    einstein.age = age;
    print(einstein.age);
}
```
In this example, the calculate method of the 'Person' object utilizes GenAI Ability to determine the age of an individual.

**3.Object Creation**

Simplify object creation with attributes automatically populated by LLM.
```
obj 'Person'
Person {
    has name: 'Name' str,
        dob: 'date of birth' str,
        accomplishments: 'Accomplishments': list[str];
}
with entry {
    einstein: 'Einstein Object': Person = Person(name="Albert Einstein") by llm1();
    print(f"{einstein.name} was born on {einstein.dob}. His accomplishments include {einstein.accomplishments}.");
}
```
In this example, the 'Person' object is created with GenAI Ability, interacting with LLM during attribute initialization.


Automatic Attribute Population: GenAI Ability streamlines object creation by automatically filling attributes using LLM.

### GenAI Ability Parameters

When using `by <model>` in code, we have the ability to provide additional parameters for fine-tuning the interaction and to customize the interaction.

```
by <model>(temperature=0.7, top_k = 3, reason=true, incl_info=(xxx), context=[])
```

Here,

 - `incl_info` :  A tuple specifying details to be passed to the LLM during prompt creation.

- `excl_info` :  A tuple specifying information to be excluded from prompts. By default, all variables/objects in scope are included.

- `model hyperparameters`: Key-value pairs specifying hyperparameters for the model during inference, e.g., temperature=0.7, top_k=3, top_p=0.51.

 - `reason`:A boolean indicating whether to include reasoning/explanation in the model's responses.

- `context`: List of information to gie external information to llm for our use cases

`by <model>(temperature=0.7, top_k = 3, top_p =0.51, incl_info=(xxx), context=[""],reason=true) ` <!--TODO : This line needs to be modified  with a working example code snippet later  -->

|    Parameters    |          Type              |
|    --------      |         -------            |
|   model_params   |   kw_pair \| None          |
|     reason       |    bool \| None            |
|    incl_info     |    tuple \| None           |
|    excl_info     |    tuple   \| None         |
|    context       |    List                    |


## Introducing Semstrings

In the dynamic landscape of programming languages, the advent of Jac introduces a novel concept called "**Semstrings**," offering a powerful and expressive way to interact with LLM. Semstrings, short for semantic strings, serve as a bridge between the traditional code structure and the capabilities of language models.They play a pivotal role in shaping the way we communicate with models and generate prompts.

Utilizing Semstrings in Various Cases
- Ability/Method Declaration
- Ability/Method Parameter Declaration
- Attributes of Architypes
- Return Type Specification
-

<span style="color:orange;">
</span>


**Ability/Method Declaration**

 Semstrings play a pivotal role in method and ability declarations, offering a clear and concise description of their intended purpose—essentially defining the action each ability or method is designed to perform.

```
can 'Translate English to French'
translate(english_word: 'English Word': str) -> 'French Word' : str by llm();
```

In this instance, the semstring <span style="color:orange;">'Translate English to French'</span> serves as a descriptive label, clarifying the intended action when invoking the function. For example, calling the function with translate("cheese") leverages the semstring to guide the model, ensuring a contextually informed response.


**Ability/Method Parameter Declaration**

 Semstrings shine prominently in method signatures, serving as guides to define parameters with explicit meanings. By providing meaningful labels, developers ensure that LLM comprehends the purpose and expected inputs clearly. These semstrings also contribute to explaining the input with meaningful context.
```
can 'Provide the Answer for the Given Question (A-F)'
get_answer(question: 'Question' str, choices: 'Answer Choices': dict) -> 'Answer (A-F)' str by llm(reason=True);
```
In this instance, the semstrings for parameters (<span style="color:orange;">'Question'</span> and <span style="color:orange;">'Answer Choices'</span>) act as informative labels, offering a clear understanding of what each parameter represents. The labels provide context to LLM, guiding it to interpret and respond to the function's inputs appropriately.

**Attributes of Architypes**

Semstrings play a vital role in describing attributes within architypes, providing a succinct and clear explanation of the purpose and nature of each attribute. This practice makes it easier to convey the respective meanings to prompts.
```
obj 'Singer'
Singer {
    has name: 'Name of the Singer' str,
        age: 'Age' int,
        top_songs: "His/Her's Top 2 Songs" list[str];
}
```
In this architype example, the semstrings associated with attributes (<span style="color:orange;">'Name of the Singer'</span>, <span style="color:orange;">'Age,'</span> and <span style="color:orange;">"His/Her's Top 2 Songs"</span>) serve as concise descriptors. These semstrings effectively communicate the significance of each attribute, facilitating a more straightforward understanding of the architype's structure.

**Return Type Specification**

Utilizing Semstring in return type specifications provides a meaningful way to explain the expected outputs of a function.
```
can 'Summarize the Accomplishments'
summarize (a: 'Accomplishments': list[str]) -> 'Summary of the Accomplishments' : str by llm;
```
In this example, the semstring <span style="color:orange;">'Summary of the Accomplishments' </span> precisely communicates the nature of the expected output. This clarity ensures that developers, as well as LLM, comprehend the type of information that will be returned by invoking the 'Summarize the Accomplishments' function.
