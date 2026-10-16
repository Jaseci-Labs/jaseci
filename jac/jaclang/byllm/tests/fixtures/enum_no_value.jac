"""A bare enum, whose members carry no values, as a `by llm()` return type."""


enum Tell { YES, NO }

glob llm = Model(model_name="gemini/gemini-1.5-flash", config={"verbose": True});

"""Yes/No answering Bot"""
def yes_or_no(question: str) -> Tell by llm();
