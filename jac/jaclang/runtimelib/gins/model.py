"""Generative AI model integration for GINS
"""


class BaseModel:
    def __init__(self, model_name: str = "gemini-1.5-flash", **kwargs):
        self.model_name = model_name
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.config()

    def config(self):
        raise NotImplementedError

    def generate(self, prompt: str):
        raise NotImplementedError


class Gemini(BaseModel):
    def config(self):
        try:
            import google.generativeai as genai

            if "api_key" in self.__dict__:
                genai.configure(api_key=self.api_key)
            else:
                import os

                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel()
            import os
        except Exception as e:
            print(
                "google.generativeai module not present. Please install using 'pip install google.generativeai'."
            )
            print("Warning:", e)
            return None

    def generate(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text
