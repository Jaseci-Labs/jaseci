class X:
    a_b = 67
    y = "aaa" + f"b{a_b}bbcc"


c = (3, 4, 5)


def entry():
    x = X
    print(x.y)


# Run the entry block
entry()
