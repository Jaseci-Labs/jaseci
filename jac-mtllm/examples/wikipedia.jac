import from mtllm.llms { OpenAI }
import from mtllm.tools.wikipedia_utils { wikipedia_summary }

glob llm = OpenAI(verbose=True, model_name="gpt-4o-mini");

def get_answer(question: str) -> str by llm(method="ReAct", tools=[wikipedia_summary]);

with entry {
    question = "Who is Jason Mars?";
    answer = get_answer(question);
    print(answer);
}
