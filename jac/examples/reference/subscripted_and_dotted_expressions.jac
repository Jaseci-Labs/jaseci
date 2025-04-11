obj Sample {
    has my_list: list = with can [1, 2, 3],
        my_dict: dict = with can {"name":"John", "age": 30};
}

glob (first, second) = (Sample().my_list[2], Sample().my_dict["name"]);

with entry {
    print(first, second);
}
