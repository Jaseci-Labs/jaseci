# list_compr: LSQUARE expression inner_compr RSQUARE
# gen_compr: LPAREN expression inner_compr RPAREN
# set_compr: LBRACE expression inner_compr RBRACE
# dict_compr: LBRACE kv_pair inner_compr RBRACE
# inner_compr: KW_ASYNC? KW_FOR atomic_chain KW_IN walrus_assign (KW_IF expression)?
with entry{
  cities = ["Vancouver", "Oslo", "Houston", "Warsaw", "Graz", "Holguín"];
  witnesses = [city for city in cities if city.startswith("H")];
  print(witnesses);

# Example: Squaring numbers greater than 5 using the walrus operator
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

squared_numbers = [num_squared for num in numbers if (num_squared := num ** 2) > 5];


print(squared_numbers);



   #list comprehension
    numbers=[1,2,3,4];
    a=[i+1 for i in numbers];   
    print(a);

    #Generator_expression
    t=(x*3 for x in range(10));
    print(t);
    print(list(t));

    #set_compr
    s1={"sun",90,"kill",887,"moon"};
    s2={s for s in s1};
    print(s2);

    #dict_compr
    dict={"d":78,"jhj":898,"dfsds":887,"kdkdk":989};
    y={ k for k in dict };
    print(y);





    #dict_val
    student_info = {'name': 'Alice', 'age': 20, 'grade': 'A'};
    print(student_info);

    #list_val
    numbers = [1, 2, 3, 4,[5,6,7] ,5];
    print(numbers);

    #tuple_val
    coordinates = (3.14, [6,7,8],2.71);
    print(coordinates);

    ##set_value
    unique_numbers = {1, 2, 3, 4, 5};
    print(unique_numbers);


}
