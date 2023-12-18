#Bitwise_operators.jac
with entry{
    # Bitwise AND
a = 5;    # binary: 0101
b = 3;    # binary: 0011
result_and = a & b;
print(f"Bitwise AND: {result_and}");  # Output: 1 (binary: 0001)

# Bitwise OR
result_or = a | b;
print(f"Bitwise OR: {result_or}") ;   # Output: 7 (binary: 0111)

# Bitwise XOR
result_xor = a ^ b;
print(f"Bitwise XOR: {result_xor}"); # Output: 6 (binary: 0110)

# Bitwise NOT
result_not_a = ~a;
print(f"Bitwise NOT of a: {result_not_a}");  # Output: -6 (binary: 11111010)

# Left shift
result_left_shift = a << 1;
print(f"Left shift of a: {result_left_shift}");  # Output: 10 (binary: 1010)

# Right shift
result_right_shift = a >> 1;
print(f"Right shift of a: {result_right_shift}"); # Output: 2 (binary: 0010)

}
