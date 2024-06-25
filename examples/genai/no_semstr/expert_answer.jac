import:py from jaclang.core.llms, Anthropic;

glob llm = Anthropic(model_name="claude-3-sonnet-20240229");


can get_expert(question: str)-> 'Expert Suitable to Answer the Question': str by llm(method="Reason"); #semstring is needed here
can get_answer(question: str, expert: str)-> 'Answer to the Question from Expert': str by llm(temperature=1.0); #semstring is needed here

with entry{
    question = "What are Large Language Models?";
    expert = get_expert(question);
    answer = get_answer(question, expert);
    print(f"For instance, {expert} would answer '{answer}' for the question '{question}'");
}