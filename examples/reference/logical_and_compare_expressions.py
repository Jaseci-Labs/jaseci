apples = 5
oranges = 8

if oranges > apples:
    print("There are more oranges than apples.")
else:
    print("There are fewer oranges than apples.")


city1 = "New York"
city2 = "Los Angeles"

# Check if the cities are the same
if city1 == city2:
    print("Both cities are the same.")
else:
    print("The cities are different.")


list1 = [1, 2, 3]
list2 = [1, 2, 3]

if list1 is list2:
    print("list1 and list2 refer to the same object.")
else:
    print("list1 and list2 are different objects.")


# in
my_list = [1, 2, 3, 4, 5]
result = 3 in my_list
print(result)  # Output: True
