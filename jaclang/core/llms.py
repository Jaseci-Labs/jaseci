"""LLMs (Large Language Models) module for Jaclang."""


class Anthropic:
    """Anthropic API client for Large Language Models (LLMs)."""

    MTLLM_PROMPT: str = ""
    MTLLM_REASON_SUFFIX: str = ""
    MTLLM_WO_REASON_SUFFIX: str = ""

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the Anthropic API client."""
        import anthropic

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


class Huggingface:
    """Huggingface API client for Large Language Models (LLMs)."""

    MTLLM_PROMPT: str = ""
    MTLLM_REASON_SUFFIX: str = ""
    MTLLM_WO_REASON_SUFFIX: str = ""

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the Huggingface API client."""
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

        torch.random.manual_seed(0)
        model = AutoModelForCausalLM.from_pretrained(
            kwargs.get("model_name", "microsoft/Phi-3-mini-128k-instruct"),
            device_map=kwargs.get("device_map", "cuda"),
            torch_dtype="auto",
            trust_remote_code=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            kwargs.get("model_name", "microsoft/Phi-3-mini-128k-instruct")
        )
        self.pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_new_tokens", 1024)

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        messages = [{"role": "user", "content": meaning_in}]
        output = self.pipe(
            messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_length=kwargs.get("max_new_tokens", self.max_tokens),
            **kwargs
        )
        return output[0]["generated_text"][-1]["content"]


class Ollama:
    """Ollama API client for Large Language Models (LLMs)."""

    MTLLM_PROMPT: str = ""
    MTLLM_REASON_SUFFIX: str = ""
    MTLLM_WO_REASON_SUFFIX: str = ""

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the Ollama API client."""
        import ollama

        self.client = ollama.Client(host=kwargs.get("host", "http://localhost:11434"))
        self.model_name = kwargs.get("model_name", "phi3")
        self.default_model_params = {
            k: v for k, v in kwargs.items() if k not in ["model_name", "host"]
        }

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        model = str(kwargs.get("model_name", self.model_name))
        if not self.check_model(model):
            self.download_model(model)
        model_params = {k: v for k, v in kwargs.items() if k not in ["model_name"]}
        messages = [{"role": "user", "content": meaning_in}]
        output = self.client.chat(
            model=model,
            messages=messages,
            options={**self.default_model_params, **model_params},
        )
        return output["message"]["content"]

    def check_model(self, model_name: str) -> bool:
        """Check if the model is available."""
        try:
            self.client.show(model_name)
            return True
        except Exception:
            return False

    def download_model(self, model_name: str) -> None:
        """Download the model."""
        self.client.pull(model_name)
