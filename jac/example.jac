with entry { 
    x:int = 0;
    y:int = 3;
    z:int = x + y;
    
    for i in range(z) {
        x = 4;
        y = y + x;
    }
    print(y/0);
    print(y);
    print("hello");
}
# with entry { 
#     x:int = 0;
#     y:int = 3;
#     z:int = x + y;
#     for i in range(100000) {
#         x = 4 * i + y * (z);
#         if x % 2 {
#             y = y + x;
#             z = x + y;
#         }
#     }
#     z = x/0;
#     print(y);
#     print("hello");
# }
