"""You can import python modules freely"""

import:py random;
import:py from math, sqrt as square_root;
import:py datetime;

with entry {
    # Generate a random number between 1 and 10
    random_number = random.randint(1, 10);
    print("Random number:", random_number);

    # Calculate the square root of a number
    square_root = math.sqrt(16);
    print("Square root:", square_root);

    # Get the current date and time
    current_time = datetime.datetime.now();
    print("Current time:", current_time);
}