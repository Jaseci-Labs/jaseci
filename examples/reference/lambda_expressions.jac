with entry{
# Example usage of the lambda function
calculate_rectangle_area = with length: float, width: float can length * width;
rectangle_area = calculate_rectangle_area(5.0, 8.0);

print(f"The area of the rectangle is: {rectangle_area}");

}