def divide_numbers(a, b):
    try:
        result = a / b
        print("Result of division:", result)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    except TypeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        print("Division operation completed successfully.")
    finally:
        print("This block always executes, regardless of success or failure.")

# Example usage
try:
    divide_numbers(10, 2)   # Normal division
    divide_numbers(10, 0)   # Division by zero (ZeroDivisionError)
    divide_numbers(10, '2') # Type error (TypeError)
except Exception as e:
    print(f"Exception caught in the outer try-except block: {e}")
