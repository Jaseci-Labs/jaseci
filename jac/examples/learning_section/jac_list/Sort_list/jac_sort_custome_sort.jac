can myfunc(n:int) -> int {
    return abs(n-50);
}

with entry{
    fruits = [100, 50, 65, 82, 23];
    fruits.sort(key = myfunc);
    print(fruits);
}