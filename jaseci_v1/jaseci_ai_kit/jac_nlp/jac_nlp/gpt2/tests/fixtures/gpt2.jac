walker test_generate {
    can gpt2.generate;
    report gpt2.generate(text= "Hello, my name is", num_return_sequences= 5);
}

walker test_get_embeddings {
    can gpt2.get_embeddings;
    report gpt2.get_embeddings(text= ["Hello, my name is GPT2", "GPT2 is an Text-to-Text Generation Model" ]);
}

walker test_train {
    can gpt2.train;
    can file.load_str;
    text= file.load_str("jac_nlp/jac_nlp/gpt2/tests/german_recipes.txt");
    gpt2.train(text, 1);
}

walker test_generate_trained {
    can gpt2.generate;
    report gpt2.generate(text= "Die Nudeln Kochen, Fleisch anbraten", num_return_sequences= 5);
}