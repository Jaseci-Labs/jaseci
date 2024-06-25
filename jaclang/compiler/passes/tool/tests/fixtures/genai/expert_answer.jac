import:py from mtllm.llms, Anthropic;

glob llm = Anthropic(model_name="claude-3-sonnet-20240229");

can 'Finds the best professional to answer the given question'
get_expert(question: 'Question': str) -> 'Expert Profession': str by llm(reason=True);
can "Get the answer for the question from expert's perspective"
get_answer(question: 'Question': str, expert: 'Expert': str) -> "Expert's Answer": str by llm(temperature=1.0);

with entry {
    question = "What are Large Language Models?";
    expert = get_expert(question);
    answer = get_answer(question, expert);
    print(
        f"For instance, {expert} would answer '{answer}' for the question '{question}'"
    );
}
