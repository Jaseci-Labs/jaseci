import:py from mtllm.llms { OpenAI }

glob llm = OpenAI();

can get_expert(question: str) -> 'Best Expert to Answer the Question': str by llm(method='Reason');
can get_answer(question: str, expert: str) -> str by llm();

with entry {
    question = "What are Large Language Models?";
    expert = get_expert(question);
    answer = get_answer(question, expert);
    print(f"{expert} says: '{answer}' ");
}
