#Simple Ability
"""Ability(Function) to calculate the numbers"""
can add(*a :tuple) -> int {
    return sum(a);
}

with entry{
    #ability calling
     print(add(9,-3,4));
    
}

