#Function with decorators, access_modifiers
class Calculator:
    """Calculator object with static method"""
    #static function
    @staticmethod
    def multiply(a, b):
        return a * b
    

print(Calculator.multiply(9, -2))