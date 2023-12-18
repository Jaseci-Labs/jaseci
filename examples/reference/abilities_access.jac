#Ability with decorators, access_modifiers
"""Calculator object with static method"""
obj Calculator{
    #static ability(function)
    
    static can :priv multiply(a :float, b :float) -> float{
        return a*b;
    }
}
with entry{
    print(Calculator.multiply(9,-2));
}