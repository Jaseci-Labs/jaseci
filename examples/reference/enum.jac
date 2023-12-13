# Define an enumeration class called Color
enum Color{
    RED = 1,
    GREEN = 2,
    BLUE = 3
}

# Enum as a function argument
can print_color(color: string ) {
    if color == Color.RED{
        print("It's red!");}
    elif color == Color.GREEN{
        print("It's green!");}
    elif color == Color.BLUE{
        print("It's blue!");}
}

with entry{
       # Accessing enum members
       print(Color.RED);      # Output: Color.RED
       print(Color.RED.value); # Output: 1
       # Iterating over enum members
       for color in Color{
          print(color);
        }
        
       # Comparing enum members
        if Color.RED == Color.BLUE{
                print("Colors are the same");
                }
        else{
                print("Colors are different");
                }
        
        # Using the enum in a function
        print_color(Color.GREEN);
}


with entry{
#list comprehension
numbers=[1,2,3,4];
a=[i+1 for i in numbers];    #????? why walrus assign????
print(a);}
