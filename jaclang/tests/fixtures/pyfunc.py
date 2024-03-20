"""Python function."""


def my_print(x: object) -> None:
    """Print function."""
    print(x)


# def my_some_func(a: int, b: int) -> int:
#     for i in range(a):
#         print(i)
#         if i == 5:
#             break
#         print(b)
#     else:
#         print("Loop completed normally{}".format(i))


# numbers = [1, 2, 3, 4, 5]
# squares = [x**2 for x in numbers]
# squares_dict = {x: x**2 for x in numbers}
# squares_generator = (x**2 for x in numbers)
# add = lambda x, y: x + y # noqa


# def my_decorator(func):
#     '''Decorator'''
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper


# x = 5
# print(f"hello {x}")


# s=[]
# a=[1,2,3,4,5]
# b=(1,2,3,4,5)
# x=()
# c={1,2,3,4,5}
# d={1:"one",2:"two",3:"three",4:"four",5:"five"}
# qq={}
# e="hello"
# f=b"hello"


# @my_decorator
# def say_hello():
#     '''Say hello'''
#     print("Hello!")
# x={}
# x = {
#         "name": "John",
#         "age": 30,
#         "city": "New York"
#     }

# class MyClass:
#     '''My class'''
#     def __init__(self, x):
#         self.x = x

#     def my_method(self):
#         print("My method")


# while x < 10:
#     x += 1
#     print("hello")

# try:
#     result = 10 / 0
# except ZeroDivisionError:
#     print("Cannot divide by zero!")
# else:
#     print(result)
# finally:
#     print("This will always execute.")


# def foox():
#     return 9 + 4


# a, b, c = 1, 2, 3
# x = y = z = 0
# first, *rest = [1, 2, 3, 4, 5]


# def greet(name, greeting="Hello")-> None:
#     '''Greet someone.'''
#     print(f"{greeting}, {name}")


# greet("Alice")
# greet("Bob", greeting="Hi")


# class MyClass2:
#     """This is a docstring for MyClass."""

#     def __init__(self):
#         """Constructor docstring."""
#         pass


# def average(*args):
#     '''Average function'''
#     return sum(args) / len(args)


# avg = average(1, 2, 3, 4, 5)


# def greet2(**kwargs):
#     '''Greet someone.'''
#     print(f"Hello, {kwargs['name']}!")


# greet2(name="Alice", age=30)

# name = "Alice"
# age = 30
# # print("Name: {}, Age: {}".format(name, age))

# # path = r'C:\Users\Alice\Documents'
# # hello_world_bytes = b"\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64"
# # print(hello_world_bytes)
# # print(type(hello_world_bytes))

# # ret_str = r"Hello\\nWorld"
# # print(ret_str)

# # br = br"Hello\\nWorld"
# # print(br)
# # print(type(br))

# # rb = rb"Hello\\nWorld"
# # print(rb)
# # print(type(rb))

# x = True
# y = False
# z = x and y


# x = 5
# assert x == 5, "x should be equal to 5"

# uu=9
# if uu==9:
#     print("uu is 9")
# elif uu==10:
#     print("uu is 10")
# else:
#     print("uu is not 9 or 10")
# filename = "semstr.jac"

# with open(filename, "r") as file:
#     content = file.read()
#     print(content)


# def my_functionx():
#     '''My function'''
#     def my_inner_function():
#         '''Inner function'''
#         return 9
#     my_inner_function()
#     for i in range(10):
#         if i == 5:
#             break
#         if i == 3:
#             continue
#     pass


# x=90
# if not isinstance(x, int):
#     raise ValueError("x must be an integer")
# else:
#     print(x)


# my_list = [1, 2, 3, 4, 5]
# del my_list[2]
# print(my_list)


# x = 5
# y = 10
# z = 15

# if not x == y:
#     print("x is not equal to y")

# if x == y or y == z:
#     print("Either x is equal to y or y is equal to z")
# else:
#     print("Neither x is equal to y nor y is equal to z")


# def count_up_to(n: int)-> int:
#     '''Count up to n'''
#     count = 1
#     while count <= n:
#         yield count
#         count += 1


# counter = count_up_to(5)
# for num in counter:
#     print(num)

# x = 0b1010
# x &= 0b1100
# print(bin(x))


# squares = {num: num**2 for num in range(1, 6)}
# even_squares_set = {num**2 for num in range(1, 11) if num % 2 == 0}
# squares_generator = (num**2 for num in range(1, 6))
# squares_list = [num**2 for num in squares_generator]

# print("\n".join([str(squares), str(even_squares_set), str(squares_list)]))
# print(
#     {"a": "b", "c": "d"},  # Dictionary value
#     {"a"},  # Set value
#     ("a",),  # Tuple value
#     ["a"],  # List value
# )
# from abc import ABC, abstractmethod


# class Calculator(ABC):
#     @staticmethod
#     def multiply(a: float, b: float) -> float:
#         return a * b

#     @abstractmethod
#     def substract(self, x: float, y: float) -> float:
#         pass

#     def add(self, number: float, *a: tuple) -> str:
#         return str(number * sum(a))


# class Substractor(Calculator):
#     def substract(self, x: float, y: float) -> float:
#         return x - y


# class Divider:
#     def divide(self, x: float, y: float):
#         return x / y


# sub = Substractor()
# div = Divider()
# print(div.divide(55, 11))
# print(Calculator.multiply(9, -2))
# print(sub.add(5, 20, 34, 56))
# print(sub.substract(9, -2))

# class Car:
#     wheels: int = 4

#     def __init__(self, make: str, model: str, year: int):
#         self.make = make
#         self.model = model
#         self.year = year

#     def display_car_info(self):
#         print(f"Car Info: {self.year} {self.make} {self.model}")

#     @staticmethod
#     def get_wheels():
#         return Car.wheels


# car1 = Car("Toyota", "Camry", 2020)
# car1.display_car_info()
# print("Number of wheels:", Car.get_wheels())

# p = print

# p("Multiply:", 7 * 2)
# p("Division:", 15 / 3)
# p("Floor:", 15 // 3)
# p("Modulo:", 17 % 5)
# p("Expon:", 2**3)
# p("combo:", (9 + 2) * 9 - 2)


# def foo(value: int):
#     assert value > 0, "Value must be positive"


# try:
#     foo(-5)
# except AssertionError as e:
#     print("Asserted:", e)

# a = b = 16
# c = 18
# print(a, b, c)
# a >>= 2
# print(a)
# a <<= 2
# print(a)
# c //= 4
# print(c)


# class X:
#     a_b = 67
#     y = "aaa" + f"b{a_b}bbcc"


# c = (3, 4, 5)
# l_1 = [2, 3, 4, 5]


# def entry():
#     x = X

#     a = "abcde...."
#     b = True
#     c = bin(12)
#     d = hex(78)
#     # e = 0x4E
#     print(l_1, a, b, c, d)
#     print(x.y)


# # Run the entry block
# entry()
# print("Hello world!")
# a = [2, 4, 5, 7, 8]
# b = [4, 8, 9, 13, 20]
# c = len(a) + len(b)
# print(c)

# """A Docstring can be added the head of any module.

# Any element in the module can also have a docstring.
# If there is only one docstring before the first element,
# it is assumed to be a module docstring.
# """

# """A docstring for add function"""


# def add(a: int, b: int) -> int:
#     return a + b


# def subtract(a: int, b: int) -> int:
#     return a - b


# if __name__ == "__main__":
#     print(add(1, subtract(3, 1)))

# p = print
# p("&:", 5 & 3)
# p("|:", 5 | 3)
# p("^:", 5 ^ 3)
# p("~:", ~5)
# p("<<:", 5 << 1)
# p(">>:", 5 >> 1)

# a = 9.2
# b = 44
# c = [2, 4, 6, 10]
# d = {"name": "john", "age": 28}
# e = ("jaseci", 5, 4, 14)
# f = True
# g = "Jaseci"
# h = {5, 8, 12, "unique"}
# print(type(a), "\n", type(b), "\n", type(c), "\n", type(d), "\n", type(e))
# print(type(f), "\n", type(g), "\n", type(h))

# print("Welcome to the world of Jaseci!")


# def add(x: int, y: int) -> int:
#     return x + y


# print(add(10, 89))

# with open(__file__.replace(".py", ".jac"), "r") as file:
#     print(file.read())

# for i in range(9):
#     if i > 2:
#         print("loop is stopped!!")
#         break
#     print(i)
# for i in "WIN":
#     if i == "W":
#         continue
#     print(i)

# from enum import Enum, auto


# class Color(Enum):
#     RED = 1
#     pencil = auto()
#     print("text")


# print(Color.RED.value)
# if 5 / 2 == 1:
#     x = 1
# else:
#     x = 2

# print(x)
# # x = "a"
# # y = 25
# # print(f"Hello {x} {y} {{This is an escaped curly brace}}")
# # person = {"name": "Jane", "age": 25}
# # print(f"Hello, {person['name']}! You're {person['age']} years old.")
# # print("This is the first line.\n This is the second line.")
# # print("This will not print.\r This will be printed")
# # print("This is \t tabbed.")
# # print("Line 1\x0cLine 2")
# # words = ["Hello", "World!", "I", "am", "a", "Jactastic!"]
# # print(
# #     f'''{"""
# # """.join(words)}'''
# # )
# for i in "ban":
#     for j in range(1, 3):
#         for k in range(1, 3, 1):
#             print(i, j, k)

# import math


# class Circle:
#     def __init__(self, radius: float):
#         self.radius = radius

#     def area(self):
#         return math.pi * self.radius * self.radius


# def foo(n_1: float):
#     return n_1**2


# print("Hello World!")
# print(foo(7))
# print(int(Circle(10).area()))

# def foo(x: int, y: int, z: int) -> None:
#     return (x * y, y * z)


# a = 5
# output = foo(x=4, y=4 if a % 3 == 2 else 3, z=9)
# print(output)

# from __future__ import annotations

# x = "Jaclang "


# def foo() -> None:
#     global x
#     x = "Jaclang is "
#     y = "Awesome"

#     def foo2() -> tuple[str, str]:
#         nonlocal y
#         y = "Fantastic"
#         return (x, y)

#     print(x, y)
#     print(foo2())


# foo()

# global a, X, y, z
# a = 5
# X = 10
# y = 15
# z = 20

# print(a, X, y, z)

# x = 15
# if 0 <= x <= 5:
#     print("Not Bad")
# elif 6 <= x <= 10:
#     print("Average")
# else:
#     print("Good Enough")

# from enum import Enum


# def foo() -> None:
#     return "Hello"


# class vehicle:
#     def __init__(self) -> None:
#         self.name = "Car"


# class Size(Enum):
#     Small = 1
#     Medium = 2
#     Large = 3


# car = vehicle()
# print(foo())
# print(car.name)
# print(Size.Medium.value)


# from jaclang import jac_import as __jac_import__
# import os
# from math import sqrt as square_root
# import datetime as dt

# for i in range(int(square_root(dt.datetime.now().year))):
#     print(os.getcwd())

# print("hello ")


# def foo():
#     print("world")


# foo()

# x = lambda a, b: a + b
# print(x(5, 4))

# if 5 > 4:
#     print("True")
# elif "a" != "a":
#     print("'a' is 'a' ")
# else:
#     print("False")
# a = [1, 2, 3]
# b = [1, 2, 3]
# print(a is b)
# print(3 in a)

# print(True or False)
# print(False and False)

# day = " sunday"
# match day:
#     case "monday":
#         print("confirmed")
#     case _:
#         print("other")

# num = 89
# match num:
#     case 89:
#         print("Correct")
#     case 8:
#         print("Nope")

# data = {"key1": 1, "key2": 2, "232": 3453}

# match data:
#     case {"key1": 1, "key2": 2, **rest}:
#         print(f"Matched a mapping with key1 and key2. Rest: {rest}")

# class Point:
#     def __init__(self, x: float, y: float):
#         self.x = x
#         self.y = y


# def match_example(data: any):
#     match data:
#         # MatchValue
#         case 42:
#             print("Matched the value 42.")

#         # MatchSingleton
#         case True:
#             print("Matched the singleton True.")
#         case None:
#             print("Matched the singleton None.")

#         # MatchSequence
#         case [1, 2, 3]:
#             print("Matched a specific sequence [1, 2, 3].")

#         # MatchStar
#         case [1, *rest, 3]:
#             print(
#                 f"Matched a sequence starting with 1 and ending with 3. Middle: {rest}"
#             )

#         # MatchMapping
#         case {"key1": 1, "key2": 2, **rest}:
#             print(f"Matched a mapping with key1 and key2. Rest: {rest}")

#         # MatchClass
#         case Point(x=int(a), y=0):
#             print(f"Point with x={a} and y=0")

#         # MatchAs
#         case [1, 2, rest_val as value]:
#             print(f"Matched a sequence and captured the last value: {value}")

#         # MatchOr
#         case [1, 2] | [3, 4]:
#             print("Matched either the sequence [1, 2] or [3, 4].")

#         case _:
#             print("No match found.")


# match_example(Point(x=9, y=0))

# data = [1, 2, 3]
# match data:
#     case [1, 2, 3]:
#         print("Matched")
#     case _:
#         print("Not Found")
# data = True
# match True:
#     # MatchSingleton
#     case True:
#         print("Matched the singleton True.")
#     case None:
#         print("Matched the singleton None.")
# a = 8
# match a:
#     case 7:
#         print("Doable")
#     case _:
#         print("Undoable")

# class Animal:
#     def __init__(self, animal_type):
#         self.animal_type = animal_type


# class Dog(Animal):
#     def __init__(self, breed):
#         super().__init__("Dog")
#         self.breed = breed
#         self.sound = ""
#         self._post_init()

#     def _post_init(self):
#         self.sound = "woof woof"


# dog1 = Dog(breed="Labrador")
# print(dog1.animal_type, dog1.breed, dog1.sound)
# def double(x: int) -> int:
#     return x * 2


# number = 5
# result = double(number)
# print(result)

# def square(x: int) -> int:
#     return x**2


# number = 5
# result = square(number)
# print(result)


# def foo(value: int):
#     if value < 0:
#         raise ValueError("Value must be non-negative")


# try:
#     foo(-1)
# except ValueError as e:
#     print("Raised:", e)

# def foo():
#     a = 42
#     if a > 0:
#         return
#     return a


# print("Returned:", foo())

# class Sample:
#     def __init__(self):
#         self.my_list = [1, 2, 3]
#         self.my_dict = {"name": "John", "age": 30}


# def main():
#     sample_instance = Sample()
#     first, second = sample_instance.my_list[2], sample_instance.my_dict["name"]

#     print(first, second)


# main()


# import unittest


# class TestCases(unittest.TestCase):
#     def test_test1(self):
#         self.assertAlmostEqual(4.99999, 4.99999)

#     def test_test2(self):
#         self.assertEqual(5, 5)

#     def test_test3(self):
#         self.assertIn("e", "qwerty")


# if __name__ == "__main__":
#     unittest.main()

# def foo(first: int, second: int) -> None:
#     print(first, second)


# val1 = (3,) + (4,)
# val2 = (val1[0] * val1[1], val1[0] + val1[1])
# foo(second=val2[1], first=val2[0])
# foo(first=val2[0], second=val2[1])


# def combine_via_func(a: int, b: int, c: int, d: int) -> int:
#     return a + b + c + d


# first_list = [1, 2, 3, 4, 5]
# second_list = [5, 8, 7, 6, 9]
# combined_list = [*first_list, *second_list]
# print(combined_list)
# first_dict = {"a": 1, "b": 2}
# second_dict = {"c": 3, "d": 4}
# combined_dict = {**first_dict, **second_dict}
# print(combine_via_func(**combined_dict))
# print(combine_via_func(**first_dict, **second_dict))

# def myFunc() -> None:
#     yield "Hello"
#     yield 91
#     yield "Good Bye"


# x = myFunc()

# for z in x:
#     print(z)

# import sys
# import sysconfig


# # Taken from _osx_support _read_output function
# def _read_cmd_output(commandstring, capture_stderr=False):
#     """Output from successful command execution or None"""
#     import os
#     import contextlib
#     fp = open("/tmp/_aix_support.%s"%(
#         os.getpid(),), "w+b")

#     with contextlib.closing(fp) as fp:
#         if capture_stderr:
#             cmd = "%s >'%s' 2>&1" % (commandstring, fp.name)
#         else:
#             cmd = "%s 2>/dev/null >'%s'" % (commandstring, fp.name)
#         return fp.read() if not os.system(cmd) else None


# def _aix_tag(vrtl, bd):
#     _sz = 32 if sys.maxsize == (2**31-1) else 64
#     _bd = bd if bd != 0 else 9988
#     return "aix-{:1x}{:1d}{:02d}-{:04d}-{}".format(vrtl[0], vrtl[1], vrtl[2], _bd, _sz)


# def _aix_vrtl(vrmf):
#     v, r, tl = vrmf.split(".")[:3]
#     return [int(v[-1]), int(r), int(tl)]


# def _aix_bos_rte():
#     try:
#         import subprocess
#         out = subprocess.check_output(["/usr/bin/lslpp", "-Lqc", "bos.rte"])
#     except ImportError:
#         out = _read_cmd_output("/usr/bin/lslpp -Lqc bos.rte")
#     out = out.decode("utf-8")
#     out = out.strip().split(":")  # type: ignore
#     _bd = int(out[-1]) if out[-1] != '' else 9988
#     return (str(out[2]), _bd)


# def aix_platform():
#     """
#     AIX filesets are identified by four decimal values: V.R.M.F."""
#     vrmf, bd = _aix_bos_rte()
#     return _aix_tag(_aix_vrtl(vrmf), bd)


# def _aix_bgt():
#     gnu_type = sysconfig.get_config_var("BUILD_GNU_TYPE")
#     if not gnu_type:
#         raise ValueError("BUILD_GNU_TYPE is not defined")
#     return _aix_vrtl(vrmf=gnu_type)


# def aix_buildtag():
#     """
#     Return the platform_tag of the system Python was built on.
#     """
#     build_date = sysconfig.get_config_var("AIX_BUILDDATE")
#     try:
#         build_date = int(build_date)
#     except (ValueError, TypeError):
#         raise ValueError(f"AIX_BUILDDATE is not defined or invalid: "
#                          f"{build_date!r}")
#     return _aix_tag(_aix_bgt(), build_date)
