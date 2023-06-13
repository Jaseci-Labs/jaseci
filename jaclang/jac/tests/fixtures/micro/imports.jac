"""You can import python modules freely."""

import:py random;
import:py from math, sqrt as square_root;
import:py datetime;

with entry {  # code that executes on module load or script run
    random_number = random.randint(1, 10);
    print("Random number:", random_number);
    # or, f"Random Number: {random_number}" |> print;

    s_root = square_root(16);
    print("Square root:", s_root);
    # or, f"Square root: {s_root}" |> print;

    current_time = datetime.datetime.now();
    print("Current time:", current_time);
    # or, f"Current time: {current_time}" |> print;
}