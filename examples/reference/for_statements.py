start_range = 1
end_range = 5
for i in range(start_range, end_range + 1):
    number = 1
    while number <= 10:
        product = i * number
        print(f"{i} x {number} = {product}")
        number += 1
    print("\n", end="")
