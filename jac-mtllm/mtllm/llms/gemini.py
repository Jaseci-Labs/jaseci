"""Google GEN API client for MTLLM."""

from mtllm.llms.base import BaseLLM


REASON_SUFFIX = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>
"""

NORMAL_SUFFIX = """Generate and return the output result(s) only, adhering to the provided Type in the following format

[Output] <result>
"""  # noqa E501

CHAIN_OF_THOUGHT_SUFFIX = """
Generate and return the output result(s) only, adhering to the provided Type in the following format. Perform the operation in a chain of thoughts.(Think Step by Step)

[Chain of Thoughts] <Chain of Thoughts>
[Output] <Result>
"""  # noqa E501

REACT_SUFFIX = """
You are given with a list of tools you can use to do different things. To achieve the given [Action], incrementally think and provide tool_usage necessary to achieve what is thought.
Provide your answer adhering in the following format. tool_usage is a function call with the necessary arguments. Only provide one [THOUGHT] and [TOOL USAGE] at a time.

[Thought] <Thought>
[Tool Usage] <tool_usage>
"""  # noqa E501


class Gemini(BaseLLM):
    """Gemini API client for MTLLM."""

    MTLLM_METHOD_PROMPTS: dict[str, str] = {
        "Normal": NORMAL_SUFFIX,
        "Reason": REASON_SUFFIX,
        "Chain-of-Thoughts": CHAIN_OF_THOUGHT_SUFFIX,
        "ReAct": REACT_SUFFIX,
    }

    def __init__(
        self,
        verbose: bool = False,
        max_tries: int = 10,
        type_check: bool = False,
        api_key: str = None,
        **kwargs: dict,
    ) -> None:
        """Initialize the Gemini API client."""
        from google import genai
        from google.genai import types  
        import os

        super().__init__(verbose, max_tries, type_check)
        self.model_name = str(kwargs.get("model_name", "gemini-1.5-flash"))
        self.client = genai.Client(api_key=(api_key or os.environ["GEMINI_API_KEY"]))
        self.types = types
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1024)
        self.top_k = kwargs.get("top_k", 2)
        self.top_p = kwargs.get("top_p", 0.5)
        self.system_instruction = kwargs.get("system_instruction", None)
        self.stop_sequences = kwargs.get("stop_sequences", ['\n'])
        self.seed = kwargs.get("seed", 42)
    
    def __infer__(self, meaning_in: str | list[dict], **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        if not isinstance(meaning_in, str):
            assert self.model_name.startswith(
                ("gemini")
            ), f"Model {self.model_name} is not multimodal, use a multimodal model instead."

        messages = meaning_in

        output = self.client.models.generate_content(
            model=self.model_name,
            contents=messages,
            config=self.types.GenerateContentConfig(
                tools=[self.types.Tool(code_execution=self.types.CodeExecution())],
                system_instruction=self.system_instruction,
                max_output_tokens= self.max_tokens,
                top_k= self.top_k,
                top_p= self.top_p,
                temperature= self.temperature,
                # response_mime_type= 'application/json',
                stop_sequences= self.stop_sequences,
                seed=self.seed,
                safety_settings= [
                self.types.SafetySetting(
                    category='HARM_CATEGORY_HATE_SPEECH',
                    threshold='BLOCK_ONLY_HIGH'
                ),
            ]
            ),
        )
        return output.text