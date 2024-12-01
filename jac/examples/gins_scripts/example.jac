# with entry { 
#     x:int = 0;
#     y:int = 3;
#     z:int = x + y;
#     i:int = 0;

#     while (i < 3) {
#         # if i % 2 {
#         #     print("d");
#         # }
#         x = 4;
#         y = y + x;
#         i += 1;
#     }
#     print(y/0);
#     print(y);
#     print("hello");
# }
with entry { 
    x:int = 0;
    y:int = 3;
    z:int = x + y;
    for i in range(49) {
        x = 4 * i + y * (z);
        if x % 2 {
            y= 0;
        }
        else {
          y = 4;
        }
    }
    z = x/y;
    print(y);
    print("hello");
}
