import:py wikipedia;
import:py from mtllm.llms, Anthropic;

glob llm = Anthropic(model_name="claude-3-sonnet-20240229");

obj 'Question Answering'
QA {
    has qa_example: 'QA example with Thoughts and Actions': list[dict] = [
        {
            "Question": "What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?",
            "Thoughts and Observations": [
                {
                    "Thought": "I need to search Colorado orogeny, find the area that the eastern sector of the Colorado ...",
                    "Action": "Search: Colorado orogeny",
                    "Observation": "The Colorado orogeny was an episode of mountain building (an orogeny) ..."
                },
                {
                    "Thought": "It does not mention the eastern sector. So I need to look up eastern sector.",
                    "Action": "Search: eastern sector of the Colorado orogeny",
                    "Observation": "The eastern sector of the Colorado orogeny extends into the High Plains."
                },
                {
                    "Thought": "High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft.",
                    "Action": "Finish: 1,800 to 7,000 ft"
                }
            ]
        }
    ];

    can 'Get next Thought and Action. Action should always startswith "Search" or "Finish"'
    get_throught_and_actions(question: 'Question': str, prev_info: 'Previous Thoughts, Actions, and Observations': list[dict]=[]) -> 'Next Thought and Action': dict by llm(incl_info=(self.qa_example));
    can get_answer(question: str) -> str {
        prev_info = [];
        while len(prev_info) < 100 {
            next_info = self.get_throught_and_actions(question, prev_info);
            if next_info["Action"].startswith("Search:") {
                obs = wikipedia.summary(
                    next_info["Action"].replace("Search: ", "")
                );
                next_info["Observation"] = obs;
            } elif next_info["Action"].startswith("Finish:") {
                return next_info["Action"].replace("Finish: ", "");
            }
            prev_info.append(next_info);
        }
        return "I am sorry, I could not find the answer.";
    }
}

with entry {
    qa = QA();
    question = "Where is Apple Headquaters located?";
    answer = qa.get_answer(question);
    print("Question: ", question);
    print("Answer: ", answer);
    question = "Who is Jason Mars?";
    answer = qa.get_answer(question);
    print("Question: ", question);
    print("Answer: ", answer);
    question = input("Ask me a Question: ");
    answer = qa.get_answer(question);
    print("Answer: ", answer);
}
