x, y, z = 5, 10, 1


def foo():
    y = 30
    print(x, y)

    def foo2():
        print(y)
        y = 9
        return (x, y)

    return foo2()


print(foo())
