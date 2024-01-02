can square(x:int)-> int {
    return x ** 2;
}
can double(x:int)-> int{
    return x * 2;
}
can add_five(x:int)-> int{
    return x + 5;
}


with entry{
    number  = int(input(("Give a number:")));
# pipe back
    result = add_five <|double <| square <| numbers;

    print(result);
}