# #Simple fun_decleration
# def add(a , b):
#     return a+b

# print(add(2,3))

# import math

# #####################
# class Calculator:
#     @staticmethod
#     def add(*a):
#         return sum(a)


# print(Calculator.add(9,-2,5))
# ##################### ##################### ##################### #####################


# def log_function_call(func):
#     def wrapper(*args, **kwargs):
#         print(f"Calling {func.__name__} with arguments {args} and keyword arguments {kwargs}")
#         result = func(*args, **kwargs)
#         print(f"{func.__name__} returned {result}")
#         return result
#     return wrapper

# @log_function_call
# def add(a, b):
#     return a + b

# @log_function_call
# def multiply(x, y):
#     return x * y

# # Using the decorated functions
# result_add = add(2, 3)
# result_multiply = multiply(4, 5)



# class Calculator:

#     def add(*a: tuple) -> int:
#         return sum(a)
    

# print(Calculator.add(9, -2, 5))
 ##################### ##################### ##################### #####################

