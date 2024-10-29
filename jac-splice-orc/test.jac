with entry{
    import:py transformers;
    pipe = transformers.pipeline("text-classification");
    print(pipe("This is a sample Text classification"));
}   