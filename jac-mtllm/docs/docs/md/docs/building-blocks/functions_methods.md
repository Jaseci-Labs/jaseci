# Functions and Methods

Functions and methods play a crucial role in implementing various functionalities in a traditional GenAI application. In jaclang, we have designed these functions and methods to be highly flexible and powerful. Surprisingly, they don't even require a function or method body thanks to the MTLLM `by <your_llm>` syntax. This section will guide you on how to effectively utilize functions and methods in jaclang using MTLLM.

## Functions

Functions/Abilities in jaclang are defined using the `can` keyword. They can be used to define a set of actions. Normal function looks like this in jaclang:

```python
can <function_name>(<parameter : parameter_type>, ..) -> <return_type> {
    <function_body>;
}
```

In a traditional GenAI application, you would make API calls inside the function body to perform the desired action. However, in jaclang, you can define the function using the `by <your_llm>` syntax. This way, you can define the function without a body and let the MTLLM model handle the implementation. Here is an example:

```python
can greet(name: str) -> str by <your_llm>();
```

In the above example, the `greet` function takes a `name` parameter of type `str` and returns a `str`. The function is defined using the `by <your_llm>` syntax, which means the implementation of the function is handled by the MTLLM.

Below is an example where we define a function `get_expert` that takes a question as input and returns the best expert to answer the question in string format using mtllm with openai model with the method `Reason`. `get_answer` function takes a question and an expert as input and returns the answer to the question using mtllm with openai model without any method. and we can call these function as normal functions.

```python
import from mtllm.llms, OpenAI;

glob llm = OpenAI(model_name="gpt-4o");

can get_expert(question: str) -> 'Best Expert to Answer the Question': str by llm(method='Reason');
can get_answer(question: str, expert: str) -> str by llm();

with entry {
    question = "What are Large Language Models?";
    expert = get_expert(question);
    answer = get_answer(question, expert);
    print(f"{expert} says: '{answer}' ");
}
```

Here's another example,

```python
import from mtllm.llms, OpenAI;

glob llm = OpenAI(model_name="gpt-4o");

can 'Get a Joke with a Punchline'
get_joke() -> tuple[str, str] by llm();

with entry {
    (joke, punchline) = get_joke();
    print(f"{joke}: {punchline}");
}
```

In the above example, the `joke_punchline` function returns a tuple of two strings, which are the joke and its punchline. The function is defined using the `by <your_llm>` syntax, which means the implementation is handled by the MTLLM. You can add semstr to the function to make it more specific.


## Methods

Methods in jaclang are also defined using the `can` keyword. They can be used to define a set of actions that are specific to a class. Normal method looks like this in jaclang:

```python
obj ClassName {
    has parameter: parameter_type;
    can <method_name>(<parameter : parameter_type>, ..) -> <return_type> {
        <method_body>;
    }
}
```

In a traditional GenAI application, you would make API calls inside the method body to perform the desired action while using `self` keyword to get necessary information. However, in jaclang, you can define the method using the `by <your_llm>` syntax. This way, you can define the method without a body and let the MTLLM model handle the implementation. Here is an example:

```python
obj Person {
    has name: str;
    can greet() -> str by <your_llm>(incl_info=(self));
}
```

In the above example, the `greet` method returns a `str`. The method is defined using the `by <your_llm>` syntax, which means the implementation of the method is handled by the MTLLM. The `incl_info=(self.name)` parameter is used to include the `name` attribute of the `Person` object as an information source for the MTLLM.

In the below example, we define a class `Essay` with a method `get_essay_judgement` that takes a criteria as input and returns the judgement for the essay based on the criteria using mtllm with openai model after a step of `Reasoning`. `get_reviewer_summary` method takes a dictionary of judgements as input and returns the summary of the reviewer based on the judgements using mtllm with openai model. `give_grade` method takes the summary as input and returns the grade for the essay using mtllm with openai model. and we can call these methods as normal methods.

```python
import from mtllm.llms, OpenAI;

glob llm = OpenAI(model_name="gpt-4o");

obj Essay {
    has essay: str;

    can get_essay_judgement(criteria: str) -> str by llm(incl_info=(self.essay));
    can get_reviewer_summary(judgements: dict) -> str by llm(incl_info=(self.essay));
    can give_grade(summary: str) -> 'A to D': str by llm();
}

with entry {
    essay = "With a population of approximately 45 million Spaniards and 3.5 million immigrants,"
        "Spain is a country of contrasts where the richness of its culture blends it up with"
        "the variety of languages and dialects used. Being one of the largest economies worldwide,"
        "and the second largest country in Europe, Spain is a very appealing destination for tourists"
        "as well as for immigrants from around the globe. Almost all Spaniards are used to speaking at"
        "least two different languages, but protecting and preserving that right has not been"
        "easy for them.Spaniards have had to struggle with war, ignorance, criticism and the governments,"
        "in order to preserve and defend what identifies them, and deal with the consequences.";
    essay = Essay(essay);
    criterias = ["Clarity", "Originality", "Evidence"];
    judgements = {};
    for criteria in criterias {
        judgement = essay.get_essay_judgement(criteria);
        judgements[criteria] = judgement;
    }
    summary = essay.get_reviewer_summary(judgements);
    grade = essay.give_grade(summary);
    print("Reviewer Notes: ", summary);
    print("Grade: ", grade);
}
```

## Ability to Understand Typed Inputs and Outputs

MTLLM is able to represent typed inputs in a way that is understandable to the model. Sametime, this makes the model to generate outputs in the expected output type without any additional information. Here is an example:

```python
import from mtllm.llms, OpenAI;

glob llm = OpenAI(model_name="gpt-4o");


enum 'Personality of the Person'
Personality {
   INTROVERT: 'Person who is shy and reticent' = "Introvert",
   EXTROVERT: 'Person who is outgoing and socially confident' = "Extrovert"
}

obj 'Person'
Person {
    has full_name: 'Fullname of the Person': str,
        yod: 'Year of Death': int,
        personality: 'Personality of the Person': Personality;
}

can 'Get Person Information use common knowledge'
get_person_info(name: 'Name of the Person': str) -> 'Person': Person by llm();

with entry {
    person_obj = get_person_info('Martin Luther King Jr.');
    print(person_obj);
}
```

```python
# Output
Person(full_name='Martin Luther King Jr.', yod=1968, personality=Personality.INTROVERT)
```

In the above example, the `get_person_info` function takes a `name` parameter of type `str` and returns a `Person` object. The `Person` object has three attributes: `full_name` of type `str`, `yod` of type `int`, and `personality` of type `Personality`. The `Personality` enum has two values: `INTROVERT` and `EXTROVERT`. The function is defined using the `by <your_llm>` syntax, which means the implementation is handled by the MTLLM. The model is able to understand the typed inputs and outputs and generate the output in the expected type.

![magic](https://media1.tenor.com/m/IOEsG9ldvhAAAAAd/mr-bean.gif)

