# Example: Printing the squares of numbers in a range
with entry{
# Range from 1 to 5 (excluding 5)
for number in range(1, 5){
    square = number ** 2;
    print(f"The square of {number} is: {square}");
    }
}

with entry{

    for i=1 to i<10 by i+=2 {    # Loop from 1 to 10 with a step of 2
         print(i * 5);  # Print multiples of 5
        }
    else{
        print("Loop completed.");}
    }


