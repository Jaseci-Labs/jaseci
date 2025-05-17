with entry{
    import transformers;
    pipe = transformers.pipeline("text-classification");
    print(pipe("This is a sample Text classification test."));

}