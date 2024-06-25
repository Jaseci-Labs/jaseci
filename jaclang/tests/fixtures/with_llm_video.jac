import:py from mtllm.llms, BaseLLM;
import:py from mtllm, Video;
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

can is_aligned(video: Video, text: str) -> bool
by llm(method="Chain-of-Thoughts", context="Mugen is the moving character");

with entry {
    video = Video(os.path.join(os.path.dirname(__file__), "mugen.mp4"), 1);
    text = "Mugen jumps off and collects few coins.";
    print(is_aligned(video, text));
}