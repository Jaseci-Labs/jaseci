# Object Initialization

As MTLLM is really great at handling typed outputs, we have added the ability to initialize a new object with only providing few of the required fields. MTLLM will automatically fill the rest of the fields based on the given context.

This behavior is very hard to achieve in other languages, but with MTLLM, it is as simple as providing the required fields and letting the MTLLM do the rest.

In the following example, we are initializing a new object of type `Task` with only providing the `description` field. The `time_in_min` and `priority_out_of_10` fields are automatically filled by the MTLLM based on the given context after a step of reasoning.

```python
import from mtllm.llms, OpenAI, Ollama;

glob llm = OpenAI(model_name="gpt-4o");

obj Task {
    has description: str;
    has time_in_min: int,
        priority_out_of_10: int;
}

with entry {
    task_contents = [
        "Have some sleep",
        "Enjoy a better weekend with my girlfriend",
        "Work on Jaseci Project",
        "Teach EECS 281 Students",
        "Enjoy family time with my parents"
    ];
    tasks = [];
    for task_content in task_contents {
        task_info = Task(description = task_content by llm(method="Reason"));
        tasks.append(task_info);
    }
    print(tasks);
}
```
```python
# Output
[
    Task(description='Have some sleep', time_in_min=30, priority_out_of_10=5),
    Task(description='Enjoy a better weekend with my girlfriend', time_in_min=60, priority_out_of_10=7),
    Task(description='Work on Jaseci Project', time_in_min=120, priority_out_of_10=8),
    Task(description='Teach EECS 281 Students', time_in_min=90, priority_out_of_10=9),
    Task(description='Enjoy family time with my parents', time_in_min=60, priority_out_of_10=7)
]
```

Here is another example with nested custom types,

```python
import from jaclang.core.llms, OpenAI;

glob llm = OpenAI(model_name="gpt-4o");

obj Employer {
    has name: 'Employer Name': str,
        location: str;
}

obj 'Person'
Person {
    has name: str,
        age: int,
        employer: Employer,
        job: str;
}

with entry {
    info: "Person's Information": str = "Alice is a 21 years old and works as an engineer at LMQL Inc in Zurich, Switzerland.";
    person = Person(by llm(incl_info=(info)));
    print(person);
}
```
```python
# Output
Person(name='Alice', age=21, employer=Employer(name='LMQL Inc', location='Zurich, Switzerland'), job='engineer')
```

In the above example, we have initialized a new object of type `Person` with only providing `info` as additional context. The `name`, `age`, `employer`, and `job` fields are automatically filled by the MTLLM based on the given context.