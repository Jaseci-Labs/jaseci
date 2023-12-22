def foo(value: int):
    assert value > 0, "Value must be positive"


try:
    foo(-5)
except AssertionError as e:
    print("Asserted:", e)
