import from mtllm.llms { OpenAI }
import from mtllm { Video }

glob llm = OpenAI(model_name="gpt-4o");

def is_aligned(video: Video, text: str) -> bool by llm(
    method="Chain-of-Thoughts",
    context="Mugen is the moving character"
);

with entry {
    video = Video("mugen.mp4", 1);
    text = "Mugen jumps off and collects few coins.";
    print(is_aligned(video, text));
}
