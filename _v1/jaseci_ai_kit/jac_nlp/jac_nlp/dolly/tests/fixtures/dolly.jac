walker test_generate_without_context {
    can dolly.generate;
    report dolly.generate(prompt="Explain to me the difference between nuclear fission and fusion.");
}

walker test_generate_with_context {
    can dolly.generate;
    subject = "George Washington (February 22, 1732[b] - December 14, 1799) was an American military officer, statesman, and Founding Father who served as the first president of the United States from 1789 to 1797.";
    report dolly.generate(prompt="When was George Washington president?",subject=subject);
}