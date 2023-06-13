"""You can import python modules freely"""

import:py random;
import:py from math, sqrt as square_root;
import:py datetime;

with entry {  # code that executes on module load or script run
    random_number = random.randint(1, 10);
    print("Random number:", random_number);

    s_root = square_root(16);
    print("Square root:", s_root);

    current_time = datetime.datetime.now();
    print("Current time:", current_time);
}