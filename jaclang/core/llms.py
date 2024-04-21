"""LLMs (Large Language Models) module for Jaclang."""

import anthropic


class Anthropic:
    """Anthropic API client for Large Language Models (LLMs)."""

    MTLLM_PROMPT: str = ""
    MTLLM_REASON_SUFFIX: str = ""
    MTLLM_WO_REASON_SUFFIX: str = ""

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the Anthropic API client."""
        self.client = anthropic.Anthropic()
        self.model_name = kwargs.get("model_name", "claude-3-sonnet-20240229")
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1024)

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        messages = [{"role": "user", "content": meaning_in}]
        output = self.client.messages.create(
            model=kwargs.get("model_name", self.model_name),
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            messages=messages,
        )
        return output.content[0].text
