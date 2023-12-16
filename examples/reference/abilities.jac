# #Simple ability_decleration
can add(a :int, b :int) -> int {
    return a+b;
 }

 with entry{
     print(add(2,3));
      #can add(2,3) -> int ;
 }

##################### ##################### ##################### #####################

# #Static Ability_decleration
# obj Calculator{

#     can add(*a :tuple) -> int {
#         return sum(a);
# }
# }

# #point of execution
# with entry{
#     print(Calculator.add(9,-2,5));
# }
# #####################

# can log_function_call(func: int) -> int {
#     can wrapper(*args:int, **kwargs:int) -> str{
#         print(f"Calling {func.__name__} with arguments {args} and keyword arguments {kwargs}");
#         result = func(*args, **kwargs);
#         print(f"{func.__name__} returned {result}");
#         return result;
#     return wrapper;
#         }
#     }

# @log_function_call
# can add(a: int, b: int) -> int {
#     return a + b;
# }

# @log_function_call
# can multiply(x: int, y: int) -> int {
#     return x * y;
# }

# with entry{
# #Using the decorated functions
# print(add(2, 3));
# result_multiply = multiply(4, 5);
# }
 ##################### ##################### ##################### #####################

