walker test_setup {
    can gen_text.setup;
    report gen_text.setup(
        module_name="gpt2"
    );
}

walker test_generate_text {
    can gen_text.generate_text;
    report gen_text.generate_text(
        prompt="This is a test text.",
        kwargs={
        "max_length":50,
        "min_length":10,
        "num_return_sequences":4
        }
    );
}
