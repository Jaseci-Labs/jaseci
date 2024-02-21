import:py dspy;

glob turbo = dspy.OpenAI(model='gpt-3.5-turbo');
glob colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts');



obj BasicQA:dspy.Signature:{
    """Answer questions with short factoid answers."""
    has question:dspy.InputField = dspy.InputField();
    has answer:dspy.OutputField = dspy.OutputField(desc="often between 1 and 5 words");
}

with entry {
    dspy.settings.configure(lm=turbo, rm=colbertv2_wiki17_abstracts);
    # Define the predictor.
    generate_answer = dspy.Predict(BasicQA);
    pred = generate_answer(question="What is the capital of France?");
    print(pred);
}