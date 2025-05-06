import from mtllm.llms { BaseLLM }
import from mtllm { Video }
import os;

obj model(BaseLLM) {
    def init {
        super.__init__();
    }

    def __infer__(meaning_in: str, **kwargs: dict) {
        print(kwargs);
        print(meaning_in);
        return "[Output] Something";
    }
}

glob llm = model();

def is_aligned(video: Video, text: str) -> bool by llm(
    method="Chain-of-Thoughts",
    context="Mugen is the moving character"
);

with entry {
    video = Video(
        os.path.join(os.path.dirname(__file__), "mugen.mp4"),
        1
    );
    text = "Mugen jumps off and collects few coins.";
    print(is_aligned(video, text));
}
