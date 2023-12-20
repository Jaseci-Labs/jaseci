def foo():
    for i in range(3):
        yield i


for i in foo():
    print("Yielded:", i)
