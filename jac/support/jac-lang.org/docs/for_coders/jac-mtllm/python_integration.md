# MTLLM Interface into Python Programs

As Jaclang is a language that supersets Python, you can easily integrate it into your existing Python application. This guide will show you how to do that by integrating a AI feature into a simple Task Manager application build using Python.

## Python Task Manager Application

Let's start by creating a simple Task Manager application using Python. The application will have the following features:
1. Add a task
2. View all tasks
3. Delete a task

```python
tasks: list[str] = []

def add_task(task: str) - > None:
    tasks.append(task)

def view_tasks() -> None:
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task}")

def delete_task(index: int) -> None:
    del tasks[index]

def main() -> None:
    while True:
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            task = input("Enter task: ")
            add_task(task)
        elif choice == 2:
            view_tasks()
        elif choice == 3:
            index = int(input("Enter task number to delete: ")) - 1
            delete_task(index)
        elif choice == 4:
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
```

You can run the application using the following command:

```bash
python task_manager.py
```

## Integrating Jaclang

Currently the Tasks in the Task Manager are just strings. Let's add a feature where when the user adds a task, the application will decide the priority of the task and the estimated time to complete the task based on the previous tasks.

### Creating the Jac Module

```jac
import:py from mtllm.llms, OpenAI;

glob llm = OpenAI();

obj Task {
    has description: str,
        priority: 'Priority of the Task (0-10)': int,
        time: 'Estimated Time Required to Finish (min)': int;
}

can create_task(description: str, prev_tasks: list[Task]) -> Task
by llm(method="Reason");
```

Just like that with a few lines of code, you have a AI powered Task Manager. The `create_task` function will take the description of the task and the previous tasks and return a Task object with the priority and estimated time to complete the task.

### Integrating the Jac Module

```python
from jaclang import jac_import

# Importing the create_task function
create_task = jac_import("taskman.jac").create_task

tasks: list = []

def add_task(task):
    task = create_task(task, tasks)
    tasks.append(task)

# Rest of the code remains the same
```

Now when the user adds a task, the application will use the MTLLM to decide the priority and estimated time to complete the task based on the previous tasks.

You can run the application using the same command:

```bash
python task_manager.py
```

This is just a simple example of how you can integrate Jaclang into your existing Python application. You can use Jaclang to add AI features to your application without having to write complex AI code.