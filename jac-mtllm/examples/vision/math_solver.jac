import from mtllm.llms { OpenAI }
import from PIL { Image }

glob llm = OpenAI(verbose=True, model_name="gpt-4o");

can 'Solve the Given Math Question'
solve_math_question(question_img: 'Image of the Question': Image) -> 'Answer to the Question': str by llm(method="Chain-of-Thoughts");

with entry {
    print(
        solve_math_question(Image.open('math_question.jpg'))
    );
}
