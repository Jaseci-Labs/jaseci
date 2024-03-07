<!-- TODO: Guide for coders to use with_llm @kugesan1105 Put the one in the chatgpt -->
## Programming with GenAI
GenAI Ability is a powerful feature that enhances interaction with Large Language Models (LLM) by utilizing the keyword `with <model>`. Developers can customize the behavior of functions or methods by modifying associated.
[Semstrings](#introducing-semstrings)

**Example Usage**

**1. Function Usage**
```
can 'Summarize the Life of the Individual'
summarize(name: 'Name of the Person': str, age: 'Age of the Person': int)
    -> 'Summary': str with llm(temperature=0.7, reason=True);
with entry {
    print(summarize('Albert Einstein', 89));
}
```
In this example, the summarize function leverages GenAI Ability to provide a summary of an individual's life. The associated Semstring ('Name of the Person', 'Age of the Person') guides the function's behavior. The `with llm` feature allows customization of the interaction, with parameters like temperature and reason influencing the model's response.

**2. Method Usage**
```
obj 'Person'
Person {
    has name: 'Name' str,
        dob: 'Date of Birth' str,
        age: 'Age' int = None;
    can 'Calculate the Age of a Person'
    calculate (cur_year: 'Current Year' int) -> 'Calculated Age' int with llm;
}
with entry {
    Einstein = Person(name="Einstein", dob="1879-03-14");
    age = Einstein.calculate(cur_year=2024);
    Einstein.age = age;
    print(Einstein.age);
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
        accomplishments: 'Accomplishments' list[str];
}
with entry {
    Einstein = Person(name="Einstein") with llm;
    print(f"{Einstein.name} was born on {Einstein.dob}. His accomplishments include {Einstein.accomplishments}.");
}
```
In this example, the 'Person' object is created with GenAI Ability, interacting with LLM during attribute initialization.

```
Automatic Attribute Population: GenAI Ability streamlines object creation by automatically filling attributes using LLM.
```
### GenAI Ability Parameters

When using `with <model>` in code, we have the ability to provide additional parameters for fine-tuning the interaction and to customize the interaction.

`with <model>(temperature=0.7, top_k = 3, reason=true,excl_info=(xxx)>`

Here,

 - `incl_info` : This parameter, represented as a tuple, allows us to explicitly specify the details to be passed to the Language Model (LLM) during prompt creation. If `incl_info` is not specified, the default behavior of the Jac engine is to include all variables or objects available within its scope.

- `excl_info` : Similarly represented as a tuple, this parameter enables us to specify information to be excluded from prompts. By default, if not explicitly defined, all variables and objects within the scope will be included in the interaction.

- `model hyperparameters`: It serves as a key-value pair, specifying the hyperparameters for the model during inference. For instance, `with <model>(temperature=0.7, top_k=3, top_p=0.51)` allows us to set specific parameters for the model.

 - `reason`:A boolean parameter, reason provides the option to specify whether reasoning should be included in the interaction. If set to True, it allows for a more detailed explanation or justification in the model's responses.

`with <model>(temperature=0.7, top_k = 3, top_p =0.51, incl_info=(xxx), reson=true) ` <!--TODO : This line needs to be modified  with a working example code snippet later  -->

|    Parameters    |          Type              |
|    --------      |         -------            |
|   model_params   |   kw_pair \| None          |
|     reason       |    bool \| None            |
|    incl_info     |    tuple \| None           |
|    excl_info     |    tuple   \| None         |


## Introducing Semstrings

In the dynamic landscape of programming languages, the advent of Jac introduces a novel concept called "**Semstrings**," offering a powerful and expressive way to interact with LLM. Semstrings, short for semantic strings, serve as a bridge between the traditional code structure and the capabilities of language models.They play a pivotal role in shaping the way we communicate with models and generate prompts.

Utilizing Semstrings in Various Cases
- Ability/Method Declaration
- Ability/Method Parameter Declaration
- Attributes of Architypes
- Return Type Specification

<span style="color:orange;">
</span>


**Ability/Method Declaration**

 Semstrings play a pivotal role in method and ability declarations, offering a clear and concise description of their intended purpose—essentially defining the action each ability or method is designed to perform.

```
can 'Translate English to French'
translate(english_word: 'English Word' str) -> 'French Word' str with llm;
```

In this instance, the semstring <span style="color:orange;">'Translate English to French'</span> serves as a descriptive label, clarifying the intended action when invoking the function. For example, calling the function with translate("cheese") leverages the semstring to guide the model, ensuring a contextually informed response.


**Ability/Method Parameter Declaration**

 Semstrings shine prominently in method signatures, serving as guides to define parameters with explicit meanings. By providing meaningful labels, developers ensure that LLM comprehends the purpose and expected inputs clearly. These semstrings also contribute to explaining the input with meaningful context.
```
can 'Provide the Answer for the Given Question (A-F)'
get_answer(question: 'Question' str, choices: 'Answer Choices': dict) -> 'Answer (A-F)' str with llm(reason=True);
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
summarize (a: 'Accomplishments' list[str]) -> 'Summary of the Accomplishments' str with llm;
```
In this example, the semstring <span style="color:orange;">'Summary of the Accomplishments' </span> precisely communicates the nature of the expected output. This clarity ensures that developers, as well as LLM, comprehend the type of information that will be returned by invoking the 'Summarize the Accomplishments' function.
