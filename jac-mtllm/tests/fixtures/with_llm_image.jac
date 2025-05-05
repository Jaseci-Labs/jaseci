import from mtllm.llms { BaseLLM }
import from mtllm { Image }
import os;

obj model :BaseLLM: {
    can init {
        super.__init__();
    }

    can __infer__(meaning_in: str, **kwargs: dict) {
        print(kwargs);
        print(meaning_in);
        return "[Output] Something";
    }
}

glob llm = model();

can 'Solve the Given Math Question'
solve_math_question(question_img: 'Image of the Question': Image) -> 'Answer to the Question': str by llm(method="Chain-of-Thoughts");

with entry {
    question_img = Image(
        os.path.join(
            os.path.dirname(__file__),
            'math_question.jpg'
        )
    );
    print(solve_math_question(question_img));
}
