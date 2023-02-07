walker test_generate {
    can gpt2.generate;
    report gpt2.generate(text= "Hello, my name is", num_return_sequences= 5);
}

walker test_get_embeddings {
    can gpt2.get_embeddings;
    report gpt2.get_embeddings(text= ["Hello, my name is GPT2", "GPT2 is an Text-to-Text Generation Model" ]);
}
