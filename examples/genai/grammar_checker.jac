import:py from mtllm.llms, Anthropic;

glob llm = Anthropic(model_name="claude-3-sonnet-20240229");

can "Resolve any grammar errors in the given text"
correct_grammar(text: 'Text with Errors': str) -> 'Grammar Corrected Text': str by llm(temperature=0.9);

with entry {
    #open the file and read the text
    files_path = input("Enter the file path to the text file: ");
    with open(files_path, 'r') as file {
        text = file.read();
    }
    print("Original text:", text);
    corrected_text = correct_grammar(text);
    print("Corrected text:", corrected_text);
}
