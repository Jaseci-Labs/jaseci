def square(x:int):
    return x ** 2

def double(x:int):
    return x * 2

def add_five(x:int):
    return x + 5

number  = int(input(("Give a number:")))

result = add_five(double(square(number)))
print(result)

