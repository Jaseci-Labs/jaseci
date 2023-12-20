x = "a"
y = 25

tokens = f"Hello {x} {y} {{This is an escaped curly brace}}"
print(tokens)

person = {"name": "Jane", "age": 25}
print(
    f"Hello, {person['name']}! You're {person['age']} years old."
)  # This is a comment

# Whitespace comment still did not write yet
# This is comment in multiline

print("This is the first line.\n This is the second line.")
print("This will not print.\r This will be printed")
print("This is \t tabbed.")
print("Line 1\fLine 2")

# words = ["Hello", "World!", "I", "am", "a", "‘Jactastic’ !"]
# print(f"{'\n'.join(words)}")
