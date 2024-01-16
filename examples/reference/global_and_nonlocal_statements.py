x = 5
y = 10
z = 1

def foo():
    global x
    y = 30
    print(x, y)

    def foo2() -> int:
        nonlocal y
        y = 9
        return (x, y)
    print(foo2())
print(foo())
