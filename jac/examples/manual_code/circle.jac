with entry{
    aaaaaaaaaaa = 1; #1    0-4
    jkjkj=898; ioio=89; # 2 3  5-9 10-14
    oioi=8; uiui=90; # 4 5  15-19 20-24
    oioi=8; uiuiwewweweweweweew=90; # 6 7  25-29 30-34
    bbb = 1;  iiii = 1; opopo=9; # 8 9 10  35-39 40-44 45-49
    oioi=8; uiui=90; # 11 12  50-54 55-59


        # ljklllk
    #   /lklklklklk  
# klklklkl
# klklklkl

        # ljklllk
        # ljklllk

# jjkjkjkjk        # 

        # ljklllk
        # ljjlkjkjkjkj
    ccccccaaaaa = 3;    opop=8; uuuuuuuuuuuuuuuu= 1; # 13 14 15  60-64 65-69 70-74
    fffoooooooooooo = 1;   kkkkkk=8; oo=9; ppppppppppppppppp= 1; # 16 17 18 19  75-79 80-84 85-89 90-94
        # ljklllk
#  w 
    d = 2;    oopopo=9;  oooooooooooooooooooooooooooooooooooooooo= 1;  # 20 21 22  95-99 100-104 105-109
    # kl
        # jjlljljll
    ee = 4; # 23 24  110-114
    hj = 1;  # 25 26  115-119
}

# """
# This module demonstrates a simple circle class and a function to calculate
# the area of a circle in all of Jac's glory.
# """

# import:py math;
# # Module-level global var

# glob RAD = 5;

# """Function to calculate the area of a circle."""
# can calculate_area(radius: float) -> float {
#     return math.pi * radius * radius;
# }
# #* (This is multiline comments in Jac)
# Above we have the demonstration of a function to calculate the area of a circle.
# Below we have the demonstration of a class to calculate the area of a circle.
# *#

# """Enum for shape types"""
# enum ShapeType {
#     CIRCLE = "Circle",
#     UNKNOWN = "Unknown"
# }

# """Base class for a shape."""
# obj Shape {
#     has shape_type: ShapeType;

#     """Abstract method to calculate the area of a shape."""
#     can area -> float abs;
# }

# """Circle class inherits from Shape."""
# obj Circle :Shape: {
#     can init(radius: float) {
#         super.init(ShapeType.CIRCLE);
#         self.radius = radius;
#         self.radius = radius;
#     }

#     """Overridden method to calculate the area of the circle."""
#     override can area -> float {
#         return math.pi * self.radius * self.radius;
#     }
# }

# with entry {
#     c = Circle(RAD);
# }
# # Global also works here

# with entry:__main__ {
#     # To run the program functionality
#     print(
#         f"Area of a circle with radius {RAD} using function: {calculate_area(RAD)}"
#     );
#     print(
#         f"Area of a {c.shape_type.value} with radius {RAD} using class: {c.area()}"
#     );
# }
# # Unit Tests!

# glob expected_area = 78.53981633974483;

# test calc_area {
#     check almostEqual(calculate_area(RAD), expected_area);
# }

# test circle_area {
#     c = Circle(RAD);
#     check almostEqual(c.area(), expected_area);
# }

# test circle_type {
#     c = Circle(RAD);
#     check c.shape_type == ShapeType.CIRCLE;
# }
