walker test_kwargs {
    report rand.sentence(max_length=5, sep=".");
    report std.sort_by_col([[1,2],[3,4]], 1, true);
    report std.sort_by_col([[1,2],[3,4]], reverse=true, col_num=1);
    report std.sort_by_col([[1,2],[3,4]], col_num=1);
}

walker multistring {
    report
        "This "
        "is"
        " a multistring";
}