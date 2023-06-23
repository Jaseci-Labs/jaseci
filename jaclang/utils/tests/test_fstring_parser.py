"""Test Fstring parser."""
from typing import Callable

from jaclang.utils.fstring_parser import FStringLexer, FStringParser
from jaclang.utils.test import TestCase

fstrings = [
    ["The sum of 7 and 3 is {7 + 3}.", "7 + 3"],
    ["The lowercase version of 'HELLO' is {'HELLO'.lower()}.", "'HELLO'.lower()"],
    [
        "My name is {my_dict['name']} and I am {my_dict['age']} years old.",
        "my_dict['name']",
        "my_dict['age']",
    ],
    ["My favorite fruit is {my_list[0]}.", "my_list[0]"],
    [
        "The sum of 5 and 7 is {(lambda x, y: x + y)(5, 7)}.",
        "(lambda x, y: x + y)(5, 7)",
    ],
    ["The person's name is {person.name}.", "person.name"],
    [
        "{'left aligned':<15} | {'center':^10} | {'right aligned':>15}",
        "'left aligned':<15",
        "'center':^10",
        "'right aligned':>15",
    ],
    ["Pi to 2 decimal places is {3.14159:.2f}.", "3.14159:.2f"],
    ["Integer with leading zeros {42:05}.", "42:05"],
    ["Current date is {datetime.now():%Y-%m-%d}.", "datetime.now():%Y-%m-%d"],
]


class TestFstrings(TestCase):
    """Test fstring parser."""

    pass  # Remove existing test case


def make_test_func(example: list[str]) -> Callable:
    """Generate a new test function for each example in fstrings."""

    def test_func(self) -> None:  # noqa: ANN001
        test_string = 'f"' + example[0] + '"'
        tree = FStringParser().parse(FStringLexer().tokenize(test_string))
        for i in example[1:]:
            self.assertTrue(f"'{i}'" in str(tree) or f'"{i}"' in str(tree))
        self.assertEqual(str(tree).count("EXPR_START"), len(example) - 1)

    return test_func


# Generate a new test case for each example in fstrings
for idx, example in enumerate(fstrings):
    # Attach the new test function to the test class
    setattr(TestFstrings, f"test_fstring_lexer_{idx}", make_test_func(example))
