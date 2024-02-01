from abc import ABC, abstractmethod


class Calculator:
    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @abstractmethod
    def substract(self, x: float, y: float) -> float:
        pass

    def add(self, number: float, *a: tuple) -> str:
        return str(number * sum(a))


class Substractor(Calculator):
    def substract(self, x: float, y: float) -> float:
        return x - y


cal = Calculator()
sub = Substractor()

print(Calculator.multiply(9, -2))
print(cal.add(5, 20, 34, 56))
print(sub.substract(9, -2))
