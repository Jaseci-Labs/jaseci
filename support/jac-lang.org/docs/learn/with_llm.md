# Programming with GenAI
<!-- TODO: Guide for coders to use by_llm @kugesan1105 Put the one in the chatgpt -->
GenAI Ability is a powerful feature that enhances interaction with Large Language Models (LLM) by utilizing the keyword <span style="color:orange;">by &lt;model&gt;</span>. Developers can customize the behavior of functions or methods by modifying associated
[Semstrings](#introducing-semstrings).
 This new feature eliminates the need for explicit prompting and allows for a more streamlined coding experience.

### Model Initialization

To incorporate a Large Language Model (LLM) into code, initialize it by importing from the ```mtllm.llms``` module built into the langauge.

To download jac-lang with all required python dependencies to use llms:
    ```bash
    pip install jaclang[llms]
    ```

Here are the list of models/ model providers which are available to use out of the box with jac-lang.

_Cloud Hosted LLMs (API Clients)_

 - [OpenAI](https://openai.com/index/openai-api/)
 - [Anthropic (Claud models)](https://www.anthropic.com/)
 - [Groq](https://groq.com/)
 - [Together AI](https://www.together.ai/)

> Note:
>
> - Theses LLMs require an API Key and the relevent python libraries to be installed.

<!-- === "OpenAI"
    ```bash
    pip install openai
    ```
=== "Anthropic"
    ```bash
    pip install anthropic
    ```
=== "Groq"
    ```bash
    pip install groq
    ```
=== "Together AI"
    ```bash
    pip install together
    ``` -->

_Running Local LLMs_

 - [Ollama](https://ollama.com/library)

    Downlad Ollama from their website, install and run the server by running ```ollama serve```. Pull and install your model of choice by bashing ```ollama run <model_name>``` on a new terminal.

 - [Hugging Face](https://huggingface.co/)

    Download and run opensource LLMs from the plethora of models available on the Hugging Face website.

> **Note:**
>
> - Running Local LLMs would be demanding for your PC setup where it will either simply not run the model or inference performance will take a hit. Check whether you have sufficient system requirements to run local LLMs.

In the jac program that you require to inference an LLM, please code as following template code snippets.

=== "OpenAI"
    ```jac linenums="1"
    import:py from mtllm.llms, OpenAI;

    glob llm = OpenAI(
                model_name = "gpt-4"
                );
    ```
=== "Anthropic"
    ```jac linenums="1"
    import:py from mtllm.llms, Anthropic;

    glob llm = Anthropic(
                model_name = "claude-3-sonnet-20240229"
                );
    ```
=== "Groq"
    ```jac linenums="1"
    import:py from mtllm.llms, Groq;

    glob llm = Groq(
                model_name = "llama3-8b-8192", # Go through available models in website
                );
    ```
=== "Together AI"
    ```jac linenums="1"
    import:py from mtllm.llms, TogetherAI;

    glob llm = TogetherAI(
                model_name = "meta-llama/Llama-2-70b-chat-hf" # Go through available models in website
                );
    ```
=== "Ollama"
    ```jac linenums="1"
    import:py from mtllm.llms, Ollama;

    glob llm = Ollama(
                model_name = "llama3:8b" # Will pull model if does not exists
                );
    ```
=== "Hugging Face"
    ```jac linenums="1"
    import:py from mtllm.llms, Huggingface;

    glob llm = Huggingface(
                model_name = "mistralai/Mistral-7B-v0.3" # Will pull model if does not exists
                );
    ```

The llm model is defined in these examples which can be intialized with specific attributes.

> **Note:**
>
> - If the coder wants to visualize the prompts during inference, enable verbose by adding ```verbose = True``` as an argument when defining the LLM.

This approach allows for the initialization of the desired model as a model code construct with a specific name (in this case, `llm`), facilitating its integration into code.

**Example Usage**
You can directly access some of our full code examples here for using the by_llm feature. We will break down the functional components later on.

=== "Translator"
    ```jac linenums="1"
    --8<-- "examples/genai/translator.jac"
    ```
=== "Personality Finder"
    ```jac linenums="1"
    --8<-- "examples/genai/personality_finder.jac"
    ```
=== "Essay Reviewer"
    ```jac linenums="1"
    --8<-- "examples/genai/essay_review.jac"
    ```
=== "Expert Answer"
    ```jac linenums="1"
    --8<-- "examples/genai/expert_answer.jac"
    ```
=== "Grammar Checker"
    ```jac linenums="1"
    --8<-- "examples/genai/grammar_checker.jac"
    ```
=== "Joke Generator"
    ```jac linenums="1"
    --8<-- "examples/genai/joke_gen.jac"
    ```
=== "Odd Word Out"
    ```jac linenums="1"
    --8<-- "examples/genai/odd_word_out.jac"
    ```
=== "Text to Type"
    ```jac linenums="1"
    --8<-- "examples/genai/text_to_type.jac"
    ```
=== "Wikipedia"
    ```jac linenums="1"
    --8<-- "examples/genai/wikipedia.jac"
    ```

**1. Function Usage**
```jac linenums="1"
can 'Summarize the Life of the Individual'
summarize(name: 'Name of the Person': str, age: 'Age of the Person': int)
    -> 'Summary': str by llm(temperature=0.7, method='Reason');
with entry {
    print(summarize('Albert Einstein', 89));
}
```
In this example, the summarize function leverages GenAI Ability to provide a summary of an individual's life. The associated Semstring ('Name of the Person', 'Age of the Person') guides the function's behavior. The `by llm` feature allows customization of the interaction, with parameters like temperature and reason influencing the model's response.

**2. Method Usage**
```jac linenums="1"
obj 'Person'
Person {
    has name: 'Name': str,
        dob: 'Date of Birth': str,
        age: 'Age': int = None;
    can 'Calculate the Age of a Person'
    calculate (cur_year: 'Current Year': int) -> 'Calculated Age': int by llm();
}
with entry {
    einstein: 'Einstein Object': Person = Person(name="Einstein", dob="1879-03-14");
    age = einstein.calculate(cur_year=2024);
    einstein.age = age;
    print(einstein.age);
}
```
In this example, the calculate method of the 'Person' object utilizes GenAI Ability to determine the age of an individual.

**3.Object Creation**

Simplify object creation with attributes automatically populated by LLM.
```jac linenums="1"
obj 'Person'
Person {
    has name: 'Name': str,
        dob: 'date of birth': str,
        accomplishments: 'Accomplishments': list[str];
}
with entry {
    einstein: 'Einstein Object': Person = Person(name="Albert Einstein" by llm());
    print(f"{einstein.name} was born on {einstein.dob}. His accomplishments include {einstein.accomplishments}.");
}
```
In this example, the 'Person' object is created with GenAI Ability, interacting with LLM during attribute initialization.


Automatic Attribute Population: GenAI Ability streamlines object creation by automatically filling attributes using LLM.

### GenAI Ability Parameters

When using `by <model>` in code, we have the ability to provide additional parameters for fine-tuning the interaction and to customize the interaction.

```jac linenums="1"
by <model>(temperature=0.7, top_k = 3, method='Reason', incl_info=(xxx), context=[])
```

Here,

 - `incl_info` :  A tuple specifying details to be passed to the LLM during prompt creation.

- `excl_info` :  A tuple specifying information to be excluded from prompts. By default, all variables/objects in scope are included.

- `model hyperparameters`: Key-value pairs specifying hyperparameters for the model during inference, e.g., temperature=0.7, top_k=3, top_p=0.51.

 - `method`: A dictionary key for using different prompting style hints such as Reasoning and Chain-of-Through etc..

- `context`: List of information to give external information to llm for our use cases.

`by <model>(temperature=0.7, top_k = 3, top_p =0.51, incl_info=(xxx), context=[""],reason=true) ` <!--TODO : This line needs to be modified  with a working example code snippet later  -->

|    Parameters    |          Type              |
|    --------      |         -------            |
|   model_params   |   kw_pair \| None          |
|     method       |    kw_pair \| None         |
|    incl_info     |    tuple \| None           |
|    excl_info     |    tuple   \| None         |
|    context       |    List                    |

## Introducing Semstrings

In the dynamic landscape of programming languages, the advent of Jac introduces a novel concept called "**Semstrings**," offering a powerful and expressive way to interact with LLM. Semstrings, short for semantic strings, serve as a bridge between the traditional code structure and the capabilities of language models.They play a pivotal role in shaping the way we communicate with models and generate prompts.

Utilizing Semstrings in Various Cases

- [Architype Declaration](#architype-declaration).
- [Enum and Enum Items Declaration](#enum-declaration)
- [Global variables Declaration](#global-variables-declaration)
- [Ability/Method Declaration](#ability-method-declaration)
- [Ability/Method Parameter Declaration](#ability-method-parameter-declaration)
- [Attributes of Architypes](#attributes-of-architypes)
- [Return Type Specification](#return-type-specification)


<span style="color:orange;">
</span>

<h3 id="architype-declaration">Architype Declaration</h3>

```jac linenums="1"
obj 'A collection of dad jokes with punchlines'
JokeList {
    has jokes: list[tuple[str, str]];
}
```

In this architype(Object) declaration, the semstring <span style="color:orange;"> "A collection of dad jokes with punchlines"</span> provides a clear and concise description of the purpose of the JokeList architype. It guide the LLM that this JpkeList is designed to store a collection of dad jokes, each consisting of a joke and its corresponding punchline.


<h3 id="enum-declaration">Enum and Enum Items Declaration</h3>

```jac linenums="1"
enum 'Personality of the Person'
Personality {
   INTROVERT: 'Person who is shy and reticent',
   EXTROVERT: 'Person who is outgoing and socially confident'
}
```
In this enum declaration, the semstring <span style="color:orange;">'Personality of the Person'</span> provides a descriptive label for the purpose of the Personality enumeration. Additionally, the semstrings <span style="color:orange;">'Person who is shy and reticent'</span> and <span style="color:orange;"> 'Person who is outgoing and socially confident'</span> serve as meaningful explanations for the INTROVERT and EXTROVERT enum items, respectively.


<h3 id="global-variables-declaration">Global variables Declaration</h3>

```jac linenums="1"
glob personality_examples: 'Personality Information of Famous People': dict[str, Personality|None] = {
    'Albert Einstein': Personality.INTROVERT,
    'Barack Obama': Personality.EXTROVERT
}
```
In this global variable declaration, the semstring <span style="color:orange;">'Personality Information of Famous People'</span> provides a clear and concise description of the purpose and content of the personality_examples variable.


<h3 id="ability-method-declaration">Ability/Method Declaration</h3>

 Semstrings play a pivotal role in method and ability declarations, offering a clear and concise description of their intended purpose—essentially defining the action each ability or method is designed to perform.

```jac linenums="1"
can 'Translate English to French'
translate(english_word: 'English Word': str) -> 'French Word' : str by llm();
```

In this instance, the semstring <span style="color:orange;">'Translate English to French'</span> serves as a descriptive label, clarifying the intended action when invoking the function. For example, calling the function with translate("cheese") leverages the semstring to guide the model, ensuring a contextually informed response.


<h3 id="ability-method-parameter-declaration">Ability/Method Parameter Declaration</h3>

 Semstrings shine prominently in method signatures, serving as guides to define parameters with explicit meanings. By providing meaningful labels, developers ensure that LLM comprehends the purpose and expected inputs clearly. These semstrings also contribute to explaining the input with meaningful context.
```jac linenums="1"
can 'Provide the Answer for the Given Question (A-F)'
get_answer(question: 'Question' str, choices: 'Answer Choices': dict) -> 'Answer (A-F)' str by llm(method='Reason');
```
In this instance, the semstrings for parameters (<span style="color:orange;">'Question'</span> and <span style="color:orange;">'Answer Choices'</span>) act as informative labels, offering a clear understanding of what each parameter represents. The labels provide context to LLM, guiding it to interpret and respond to the function's inputs appropriately.

<h3 id="attributes-of-architypes">Attributes of Architypes</h3>

Semstrings play a vital role in describing attributes within architypes, providing a succinct and clear explanation of the purpose and nature of each attribute. This practice makes it easier to convey the respective meanings to prompts.
```jac linenums="1"
obj 'Singer'
Singer {
    has name: 'Name of the Singer': str,
        age: 'Age': int,
        top_songs: "His/Her's Top 2 Songs": list[str];
}
```
In this architype example, the semstrings associated with attributes (<span style="color:orange;">'Name of the Singer'</span>, <span style="color:orange;">'Age,'</span> and <span style="color:orange;">"His/Her's Top 2 Songs"</span>) serve as concise descriptors. These semstrings effectively communicate the significance of each attribute, facilitating a more straightforward understanding of the architype's structure.

<h3 id="return-type-specification">Return Type Specification</h3>

Utilizing Semstring in return type specifications provides a meaningful way to explain the expected outputs of a function.
```jac linenums="1"
can 'Summarize the Accomplishments'
summarize (a: 'Accomplishments': list[str]) -> 'Summary of the Accomplishments' : str by llm();
```
In this example, the semstring <span style="color:orange;">'Summary of the Accomplishments' </span> precisely communicates the nature of the expected output. This clarity ensures that developers, as well as LLM, comprehend the type of information that will be returned by invoking the 'Summarize the Accomplishments' function.
<!-- how ? -->
