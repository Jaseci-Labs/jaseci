import:py from mtllm.llms, BaseLLM;
import:py from PIL, Image;
import:py os;

obj model:BaseLLM: {
    can init {
        self.verbose = False;
        self.max_tries = 1;
    }
    can __infer__(meaning_in: str, **kwargs: dict) {
        print(kwargs);
        print(meaning_in);
        return "[Output] Something";
    }
}
glob llm = model();

can 'Solve the Given Math Question'
solve_math_question(question_img: 'Image of the Question': Image) -> 'Answer to the Question': str
by llm(method="Chain-of-Thoughts");

with entry {
    question_img = Image.open(os.path.join(os.path.dirname(__file__), 'math_question.jpg'));
    print(solve_math_question(question_img));
}