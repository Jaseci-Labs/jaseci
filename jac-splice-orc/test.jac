with entry{
    # import:py transformers;
    # pipe = transformers.pipeline("text-classification");
    # print(pipe("This is a sample Text classification test."));
    import:py numpy;
    arr = numpy.array([1, 2, 3, 4]);
    print(arr);
    result = numpy.sum(arr);  # Remote method call
    print(result);
    
}   